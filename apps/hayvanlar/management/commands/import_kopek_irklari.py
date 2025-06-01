"""
Köpek ırklarını veritabanına eklemek için komut
"""

from django.core.management.base import BaseCommand
from apps.hayvanlar.models import KopekIrk
from apps.ortak.constants import KopekIrklari

class Command(BaseCommand):
    help = 'Köpek ırklarını veritabanına ekler'

    def handle(self, *args, **options):
        self.stdout.write('Köpek ırkları ekleniyor...')
        
        # Kayıtlı ırk sayısı
        existing_count = KopekIrk.objects.count()
        self.stdout.write(f'Mevcut ırk sayısı: {existing_count}')
        
        # Yeni kayıt sayısı
        created_count = 0
        
        # Yerli ırklar listesi
        yerli_irklar = KopekIrklari.YERLI_IRKLAR
        
        # Popüler ırklar listesi
        populer_irklar = KopekIrklari.POPULER_IRKLAR
        
        # Her bir ırkı ekle
        for irk_id, irk_ad in KopekIrklari.choices:
            # Eğer zaten varsa güncelle, yoksa oluştur
            irk, created = KopekIrk.objects.update_or_create(
                id=irk_id,
                defaults={
                    'ad': irk_ad,
                    'yerli': irk_id in yerli_irklar,
                    'populer': irk_id in populer_irklar
                }
            )
            
            if created:
                created_count += 1
                if created_count % 50 == 0:
                    self.stdout.write(f'Şu ana kadar {created_count} ırk eklendi...')
        
        self.stdout.write(self.style.SUCCESS(f'{created_count} yeni ırk eklendi.'))
        self.stdout.write(self.style.SUCCESS('İşlem tamamlandı! Toplam: {}'.format(existing_count + created_count)))
