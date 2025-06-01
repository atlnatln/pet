"""
🐾 Köpek Irkları ve Kategorileri Senkronizasyon Komutu
==============================================================================
Köpek ırkları ve kategoriler arasındaki ilişkiyi senkronize eden yönetim komutu
==============================================================================
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import transaction

from apps.hayvanlar.models import KopekIrk
from apps.kategoriler.models import Kategori


class Command(BaseCommand):
    help = 'Köpek ırkları ve kategorileri senkronize eder'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Tüm ırkları (popüler olmayanlar dahil) senkronize et',
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Mevcut kategorileri bile güncelle',
        )
    
    def handle(self, *args, **options):
        all_breeds = options['all']
        force = options['force']
        
        self.stdout.write('Köpek ırkları ve kategorileri senkronize ediliyor...')
        
        # Ana köpek kategorisini bul
        kopekler_kategori = Kategori.objects.filter(
            ad__iexact='Köpekler',
            parent__isnull=True
        ).first()
        
        if not kopekler_kategori:
            self.stderr.write('Hata: Köpekler ana kategorisi bulunamadı!')
            return
            
        # Senkronize edilecek ırkları belirle
        if all_breeds:
            irklar = KopekIrk.objects.filter(aktif=True)
            self.stdout.write(f'Tüm aktif köpek ırkları ({irklar.count()}) senkronize ediliyor...')
        else:
            irklar = KopekIrk.objects.filter(aktif=True, populer=True)
            self.stdout.write(f'Sadece popüler köpek ırkları ({irklar.count()}) senkronize ediliyor...')
        
        # Mevcut alt kategorileri al
        mevcut_kategoriler = {
            k.ad.lower(): k for k in Kategori.objects.filter(parent=kopekler_kategori)
        }
        
        added = 0
        updated = 0
        errors = 0
        
        with transaction.atomic():
            # Her ırk için kategori oluştur veya güncelle
            for irk in irklar:
                try:
                    # Bu ırk için bir kategori var mı?
                    alt_kategori = mevcut_kategoriler.get(irk.ad.lower())
                    
                    if alt_kategori:
                        if force:
                            # Mevcut kategoriyi güncelle
                            alt_kategori.ad = irk.ad
                            alt_kategori.aciklama = irk.aciklama or f"{irk.ad} ırkı köpekler"
                            alt_kategori.aktif = True
                            alt_kategori.save()
                            updated += 1
                    else:
                        # Yoksa yeni kategori oluştur
                        slug = f"kopekler-{slugify(irk.ad)}"
                        
                        # Aynı slug varsa sayı ekle
                        counter = 1
                        test_slug = slug
                        while Kategori.objects.filter(slug=test_slug).exists():
                            test_slug = f"{slug}-{counter}"
                            counter += 1
                        
                        Kategori.objects.create(
                            ad=irk.ad,
                            slug=test_slug,
                            parent=kopekler_kategori,
                            pet_type='dog',
                            renk_kodu=kopekler_kategori.renk_kodu or '#f59e0b',
                            aciklama=irk.aciklama or f"{irk.ad} ırkı köpekler",
                            aktif=True,
                            sira=Kategori.objects.filter(parent=kopekler_kategori).count() + 1
                        )
                        added += 1
                        
                except Exception as e:
                    self.stderr.write(f'Hata: {irk.ad} ırkını senkronize ederken: {str(e)}')
                    errors += 1
        
        # Sıralamayı düzeltme
        self.stdout.write('Kategori sıralaması düzeltiliyor...')
        alt_kategoriler = Kategori.objects.filter(parent=kopekler_kategori).order_by('ad')
        for index, kategori in enumerate(alt_kategoriler, start=1):
            kategori.sira = index
            kategori.save(update_fields=['sira'])
        
        self.stdout.write(self.style.SUCCESS(
            f'\nTamamlandı!\n'
            f'- {added} yeni kategori eklendi\n'
            f'- {updated} mevcut kategori güncellendi\n'
            f'- {errors} hata oluştu\n'
            f'- Toplam {alt_kategoriler.count()} köpek alt kategorisi bulunuyor'
        ))
