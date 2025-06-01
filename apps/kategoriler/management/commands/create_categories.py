"""
🐾 Kategori Oluşturma Komutu
==============================================================================
Temel kategori yapısını oluşturan yönetim komutu 
==============================================================================
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.kategoriler.models import Kategori, KategoriOzellik
from apps.ortak.constants import PetTypes

class Command(BaseCommand):
    """
    Temel hayvan kategorilerini oluşturan komut
    
    Kullanım:
        python manage.py create_categories
        python manage.py create_categories --with-features
    """
    
    help = 'Temel hayvan kategorilerini ve özelliklerini oluşturur'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--with-features',
            action='store_true',
            dest='features',
            help='Kategori özelliklerini de oluştur',
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            help='Var olan kategorileri zorla güncelle',
        )
    
    def handle(self, *args, **options):
        """Komut çalıştırıldığında"""
        self.stdout.write(
            self.style.HTTP_INFO('🏷️ Temel hayvan kategorilerini oluşturma...')
        )
        
        # Ana kategoriler
        ana_kategoriler = {
            'dog': {
                'ad': 'Köpekler',
                'aciklama': 'Sadakat ve dostluğun temsilcileri',
                'ikon_adi': 'fa-dog',
                'renk_kodu': '#f59e0b',
                'sira': 1,
                'alt_kategoriler': [
                    "Golden Retriever", "Labrador", "Terrier", "Bulldog", 
                    "Pug", "Husky", "German Shepherd", "Poodle", "Beagle", 
                    "Boxer", "Diğer"
                ],
                'ozellikler': [
                    {
                        'ad': 'Irk',
                        'alan_tipi': 'select',
                        'secenekler': [
                            "Golden Retriever", "Labrador", "Terrier", "Bulldog", 
                            "Pug", "Husky", "German Shepherd", "Poodle", "Beagle", 
                            "Boxer", "Diğer"
                        ],
                        'zorunlu': True,
                        'sira': 1
                    },
                    {
                        'ad': 'Yaş',
                        'alan_tipi': 'range',
                        'zorunlu': True,
                        'sira': 2
                    },
                    {
                        'ad': 'Cinsiyet',
                        'alan_tipi': 'select',
                        'secenekler': ["Erkek", "Dişi"],
                        'zorunlu': True,
                        'sira': 3
                    },
                    {
                        'ad': 'Boy',
                        'alan_tipi': 'select',
                        'secenekler': ["Küçük", "Orta", "Büyük"],
                        'zorunlu': False,
                        'sira': 4
                    },
                    {
                        'ad': 'Kıl Tipi',
                        'alan_tipi': 'select',
                        'secenekler': ["Kısa", "Orta", "Uzun"],
                        'zorunlu': False,
                        'sira': 5
                    },
                    {
                        'ad': 'Karakter',
                        'alan_tipi': 'select',
                        'secenekler': ["Uysal", "Aktif", "Oyuncu", "Korumacı", "Sakin", "Eğitilebilir"],
                        'zorunlu': False,
                        'sira': 6
                    },
                    {
                        'ad': 'Sağlık',
                        'alan_tipi': 'select',
                        'secenekler': ["Aşıları Tam", "Kısırlaştırılmış", "Özel Bakım Gerekli"],
                        'zorunlu': False,
                        'sira': 7
                    },
                    {
                        'ad': 'Çocuklarla',
                        'alan_tipi': 'boolean',
                        'zorunlu': False,
                        'sira': 8
                    }
                ]
            },
            'cat': {
                'ad': 'Kediler',
                'aciklama': 'Bağımsızlık ve zarafetin ustası',
                'ikon_adi': 'fa-cat',
                'renk_kodu': '#8b5cf6',
                'sira': 2,
                'alt_kategoriler': [
                    "British Shorthair", "Scottish Fold", "Siyam", "Persian", 
                    "Maine Coon", "Bengal", "Ragdoll", "Turkish Angora", 
                    "Van", "Sphynx", "Diğer"
                ],
                'ozellikler': [
                    {
                        'ad': 'Irk',
                        'alan_tipi': 'select',
                        'secenekler': [
                            "British Shorthair", "Scottish Fold", "Siyam", "Persian", 
                            "Maine Coon", "Bengal", "Ragdoll", "Turkish Angora", 
                            "Van", "Sphynx", "Diğer"
                        ],
                        'zorunlu': True,
                        'sira': 1
                    },
                    {
                        'ad': 'Yaş',
                        'alan_tipi': 'range',
                        'zorunlu': True,
                        'sira': 2
                    },
                    {
                        'ad': 'Cinsiyet',
                        'alan_tipi': 'select',
                        'secenekler': ["Erkek", "Dişi"],
                        'zorunlu': True,
                        'sira': 3
                    },
                    {
                        'ad': 'Kıl Tipi',
                        'alan_tipi': 'select',
                        'secenekler': ["Kısa", "Orta", "Uzun"],
                        'zorunlu': False,
                        'sira': 4
                    },
                    {
                        'ad': 'Karakter',
                        'alan_tipi': 'select',
                        'secenekler': ["Bağımsız", "Oyuncu", "Sevecen", "Sakin", "Aktif"],
                        'zorunlu': False,
                        'sira': 5
                    },
                    {
                        'ad': 'Sağlık',
                        'alan_tipi': 'select',
                        'secenekler': ["Aşıları Tam", "Kısırlaştırılmış", "Özel Bakım Gerekli"],
                        'zorunlu': False,
                        'sira': 6
                    },
                    {
                        'ad': 'Ev Kedisi',
                        'alan_tipi': 'boolean',
                        'zorunlu': False,
                        'sira': 7
                    }
                ]
            },
            'bird': {
                'ad': 'Kuşlar',
                'aciklama': 'Özgürlüğün renkli elçileri',
                'ikon_adi': 'fa-dove',
                'renk_kodu': '#06b6d4',
                'sira': 3,
                'alt_kategoriler': [
                    "Papağan", "Kanarya", "Muhabbet Kuşu", "Bülbül", "Sevda Kuşu", "Diğer"
                ],
                'ozellikler': [
                    {
                        'ad': 'Tür',
                        'alan_tipi': 'select',
                        'secenekler': [
                            "Papağan", "Kanarya", "Muhabbet Kuşu", "Bülbül", "Sevda Kuşu", "Diğer"
                        ],
                        'zorunlu': True,
                        'sira': 1
                    },
                    {
                        'ad': 'Yaş',
                        'alan_tipi': 'range',
                        'zorunlu': False,
                        'sira': 2
                    },
                    {
                        'ad': 'Cinsiyet',
                        'alan_tipi': 'select',
                        'secenekler': ["Erkek", "Dişi", "Bilinmiyor"],
                        'zorunlu': False,
                        'sira': 3
                    },
                    {
                        'ad': 'Eğitim',
                        'alan_tipi': 'select',
                        'secenekler': ["Konuşabiliyor", "Eğitilebilir", "Eğitimsiz"],
                        'zorunlu': False,
                        'sira': 4
                    },
                    {
                        'ad': 'Kafes Dahil',
                        'alan_tipi': 'boolean',
                        'zorunlu': False,
                        'sira': 5
                    }
                ]
            },
            'fish': {
                'ad': 'Balıklar',
                'aciklama': 'Sessiz güzelliğin temsilcileri',
                'ikon_adi': 'fa-fish',
                'renk_kodu': '#3b82f6',
                'sira': 4,
                'alt_kategoriler': [
                    "Japon Balığı", "Beta", "Melek", "Diskus", "Ciklet", "Tetra", "Diğer"
                ],
                'ozellikler': [
                    {
                        'ad': 'Tür',
                        'alan_tipi': 'select',
                        'secenekler': [
                            "Japon Balığı", "Beta", "Melek", "Diskus", "Ciklet", "Tetra", "Diğer"
                        ],
                        'zorunlu': True,
                        'sira': 1
                    },
                    {
                        'ad': 'Boy',
                        'alan_tipi': 'select',
                        'secenekler': ["Küçük", "Orta", "Büyük"],
                        'zorunlu': False,
                        'sira': 2
                    },
                    {
                        'ad': 'Akvaryum Tipi',
                        'alan_tipi': 'select',
                        'secenekler': ["Tatlı Su", "Tuzlu Su"],
                        'zorunlu': False,
                        'sira': 3
                    },
                    {
                        'ad': 'Akvaryum Dahil',
                        'alan_tipi': 'boolean',
                        'zorunlu': False,
                        'sira': 4
                    }
                ]
            },
            'rabbit': {
                'ad': 'Kemirgenler',
                'aciklama': 'Minik dostların büyük kalpleri',
                'ikon_adi': 'fa-rabbit',
                'renk_kodu': '#f97316',
                'sira': 5,
                'alt_kategoriler': [
                    "Tavşan", "Hamster", "Guinea Pig", "Sincap", "Fare", "Diğer"
                ],
                'ozellikler': [
                    {
                        'ad': 'Tür',
                        'alan_tipi': 'select',
                        'secenekler': [
                            "Tavşan", "Hamster", "Guinea Pig", "Sincap", "Fare", "Diğer"
                        ],
                        'zorunlu': True,
                        'sira': 1
                    },
                    {
                        'ad': 'Yaş',
                        'alan_tipi': 'range',
                        'zorunlu': False,
                        'sira': 2
                    },
                    {
                        'ad': 'Cinsiyet',
                        'alan_tipi': 'select',
                        'secenekler': ["Erkek", "Dişi", "Bilinmiyor"],
                        'zorunlu': False,
                        'sira': 3
                    },
                    {
                        'ad': 'Karakter',
                        'alan_tipi': 'select',
                        'secenekler': ["Çekingen", "Oyuncu", "Sevecen", "Aktif"],
                        'zorunlu': False,
                        'sira': 4
                    },
                    {
                        'ad': 'Kafes Dahil',
                        'alan_tipi': 'boolean',
                        'zorunlu': False,
                        'sira': 5
                    }
                ]
            },
            'reptile': {
                'ad': 'Sürüngenler',
                'aciklama': 'Antik dünyanın gizemli temsilcileri',
                'ikon_adi': 'fa-turtle',
                'renk_kodu': '#059669',
                'sira': 6,
                'alt_kategoriler': [
                    "Kaplumbağa", "Yılan", "Kertenkele", "İguana", "Bukalemun", "Diğer"
                ],
                'ozellikler': [
                    {
                        'ad': 'Tür',
                        'alan_tipi': 'select',
                        'secenekler': [
                            "Kaplumbağa", "Yılan", "Kertenkele", "İguana", "Bukalemun", "Diğer"
                        ],
                        'zorunlu': True,
                        'sira': 1
                    },
                    {
                        'ad': 'Boy',
                        'alan_tipi': 'select',
                        'secenekler': ["Küçük", "Orta", "Büyük"],
                        'zorunlu': False,
                        'sira': 2
                    },
                    {
                        'ad': 'Yaş',
                        'alan_tipi': 'range',
                        'zorunlu': False,
                        'sira': 3
                    },
                    {
                        'ad': 'Cinsiyet',
                        'alan_tipi': 'select',
                        'secenekler': ["Erkek", "Dişi", "Bilinmiyor"],
                        'zorunlu': False,
                        'sira': 4
                    },
                    {
                        'ad': 'Terraryum Dahil',
                        'alan_tipi': 'boolean',
                        'zorunlu': False,
                        'sira': 5
                    },
                    {
                        'ad': 'Özel Bakım',
                        'alan_tipi': 'text',
                        'zorunlu': False,
                        'sira': 6
                    }
                ]
            },
            'other': {
                'ad': 'Egzotik Hayvanlar',
                'aciklama': 'Farklılığın renkli dünyası',
                'ikon_adi': 'fa-paw',
                'renk_kodu': '#dc2626',
                'sira': 7,
                'alt_kategoriler': [
                    "Papağan (Büyük)", "Maymun", "Kirpi", "Gelincik", "Diğer"
                ],
                'ozellikler': [
                    {
                        'ad': 'Tür',
                        'alan_tipi': 'select',
                        'secenekler': [
                            "Papağan (Büyük)", "Maymun", "Kirpi", "Gelincik", "Diğer"
                        ],
                        'zorunlu': True,
                        'sira': 1
                    },
                    {
                        'ad': 'Yaş',
                        'alan_tipi': 'range',
                        'zorunlu': False,
                        'sira': 2
                    },
                    {
                        'ad': 'Cinsiyet',
                        'alan_tipi': 'select',
                        'secenekler': ["Erkek", "Dişi", "Bilinmiyor"],
                        'zorunlu': False,
                        'sira': 3
                    },
                    {
                        'ad': 'Boy',
                        'alan_tipi': 'select',
                        'secenekler': ["Küçük", "Orta", "Büyük"],
                        'zorunlu': False,
                        'sira': 4
                    },
                    {
                        'ad': 'Özel İhtiyaçlar',
                        'alan_tipi': 'text',
                        'zorunlu': False,
                        'sira': 5
                    },
                    {
                        'ad': 'Ekipman Dahil',
                        'alan_tipi': 'boolean',
                        'zorunlu': False,
                        'sira': 6
                    }
                ]
            },
        }
        
        # Ana kategorileri oluştur
        created_categories = 0
        updated_categories = 0
        
        for pet_type, kategori_data in ana_kategoriler.items():
            # Ana kategoriyi oluştur veya güncelle
            kategori, created = self._create_or_update_category(
                ad=kategori_data['ad'],
                defaults={
                    'aciklama': kategori_data['aciklama'],
                    'pet_type': pet_type,
                    'ikon_adi': kategori_data['ikon_adi'],
                    'renk_kodu': kategori_data['renk_kodu'],
                    'sira': kategori_data['sira']
                },
                force=options['force']
            )
            
            if created:
                created_categories += 1
                self.stdout.write(self.style.SUCCESS(f'✅ {kategori.ad} kategorisi oluşturuldu'))
            else:
                updated_categories += 1
                self.stdout.write(f'🔄 {kategori.ad} kategorisi güncellendi')
            
            # Alt kategorileri ekle
            if 'alt_kategoriler' in kategori_data:
                for i, alt_ad in enumerate(kategori_data['alt_kategoriler']):
                    alt_slug = slugify(f"{kategori.ad}-{alt_ad}")
                    alt, alt_created = self._create_or_update_category(
                        ad=alt_ad,
                        defaults={
                            'parent': kategori, 
                            'pet_type': pet_type,
                            'slug': alt_slug,
                            'sira': i+1
                        }, 
                        force=options['force']
                    )
                    
                    if alt_created:
                        created_categories += 1
                        self.stdout.write(f'  ↳ ✅ {alt.ad} alt kategorisi oluşturuldu')
                    else:
                        updated_categories += 1
                        self.stdout.write(f'  ↳ 🔄 {alt.ad} alt kategorisi güncellendi')
            
            # Özellikleri ekle (opsiyonel)
            if options['features'] and 'ozellikler' in kategori_data:
                for i, ozellik_data in enumerate(kategori_data['ozellikler']):
                    self._create_or_update_feature(kategori, ozellik_data)
        
        # Sonuç raporu
        self.stdout.write(self.style.SUCCESS(
            f'✅ Toplam {created_categories} kategori oluşturuldu, {updated_categories} kategori güncellendi'
        ))
        
        if options['features']:
            self.stdout.write(self.style.SUCCESS('✅ Kategori özellikleri de oluşturuldu'))
    
    def _create_or_update_category(self, ad, defaults, force=False):
        """Kategori oluştur veya güncelle"""
        kategori = None
        created = False
        
        # Önce ad ile bul
        try:
            kategori = Kategori.objects.get(ad=ad)
            
            # Force güncelleme isteniyorsa
            if force:
                for key, value in defaults.items():
                    if key != 'slug':  # slug'ı güncellemiyoruz
                        setattr(kategori, key, value)
                kategori.save()
        except Kategori.DoesNotExist:
            # Yoksa oluştur
            if 'slug' not in defaults:
                defaults['slug'] = slugify(ad)
            
            kategori = Kategori.objects.create(
                ad=ad,
                **defaults
            )
            created = True
        
        return kategori, created
    
    def _create_or_update_feature(self, kategori, ozellik_data):
        """Kategori özelliği oluştur veya güncelle"""
        ozellik, created = KategoriOzellik.objects.update_or_create(
            kategori=kategori,
            ad=ozellik_data['ad'],
            defaults={
                'alan_tipi': ozellik_data['alan_tipi'],
                'secenekler': ozellik_data.get('secenekler', None),
                'zorunlu': ozellik_data['zorunlu'],
                'sira': ozellik_data['sira'],
                'aktif': True
            }
        )
        
        if created:
            self.stdout.write(f'    ↳ ✅ "{ozellik.ad}" özelliği oluşturuldu')
        else:
            self.stdout.write(f'    ↳ 🔄 "{ozellik.ad}" özelliği güncellendi')

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu komut, platformun kategori yapısını inşa eder.
# Her hayvan türü için dijital bir ev, her özellik için bir veri noktası.
# 🐾 Bu komutla, kategorilerin hikayesi başlar!
