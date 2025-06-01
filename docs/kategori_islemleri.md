# 🏷️ KATEGORİ SİSTEMİ ADIM ADIM UYGULAMA KILAVUZU

## 1️⃣ VERİTABANINDA ANA KATEGORİLERİ OLUŞTURMA

Django admin üzerinden veya komut satırı aracılığıyla ana kategorileri oluşturun:

```python
python manage.py shell

# Shell içinde:
from apps.kategoriler.models import Kategori

# Köpekler kategorisi
Kategori.objects.create(
    ad="Köpekler",
    aciklama="Sadakat ve dostluğun temsilcileri",
    pet_type="dog",
    ikon_adi="fa-dog",
    renk_kodu="#f59e0b",
    sira=1
)

# Kediler kategorisi
Kategori.objects.create(
    ad="Kediler",
    aciklama="Bağımsızlık ve zarafetin ustası",
    pet_type="cat",
    ikon_adi="fa-cat",
    renk_kodu="#8b5cf6",
    sira=2
)

# Diğer ana kategoriler...
```

## 2️⃣ KATEGORİLER İÇİN YÖNETİM KOMUTU OLUŞTURMA

Kategorileri otomatik oluşturan bir yönetim komutu ekleyelim:

### `/home/akn/Genel/pet/apps/kategoriler/management/commands/create_categories.py` dosyası oluşturun:

```python
from django.core.management.base import BaseCommand
from apps.kategoriler.models import Kategori, KategoriOzellik
from apps.ortak.constants import PetTypes

class Command(BaseCommand):
    help = 'Temel hayvan kategorilerini ve özelliklerini oluşturur'
    
    def handle(self, *args, **options):
        self.stdout.write('🏷️ Temel hayvan kategorilerini oluşturma...')
        
        # Ana kategoriler
        ana_kategoriler = {
            'dog': {
                'ad': 'Köpekler',
                'aciklama': 'Sadakat ve dostluğun temsilcileri',
                'ikon_adi': 'fa-dog',
                'renk_kodu': '#f59e0b',
                'sira': 1
            },
            'cat': {
                'ad': 'Kediler',
                'aciklama': 'Bağımsızlık ve zarafetin ustası',
                'ikon_adi': 'fa-cat',
                'renk_kodu': '#8b5cf6',
                'sira': 2
            },
            # Diğer kategoriler...
        }
        
        created_count = 0
        updated_count = 0
        
        for pet_type, kategori_data in ana_kategoriler.items():
            kategori, created = Kategori.objects.update_or_create(
                ad=kategori_data['ad'],
                defaults={
                    'aciklama': kategori_data['aciklama'],
                    'pet_type': pet_type,
                    'ikon_adi': kategori_data['ikon_adi'],
                    'renk_kodu': kategori_data['renk_kodu'],
                    'sira': kategori_data['sira']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ {kategori.ad} kategorisi oluşturuldu'))
            else:
                updated_count += 1
                self.stdout.write(f'🔄 {kategori.ad} kategorisi güncellendi')
        
        self.stdout.write(self.style.SUCCESS(
            f'✅ Toplam {created_count} kategori oluşturuldu, {updated_count} kategori güncellendi'
        ))
```

## 3️⃣ KATEGORİ ÖZELLİKLERİNİ EKLEME

Her kategori için gerekli özellikleri ekleyin:

```python
python manage.py shell

# Shell içinde:
from apps.kategoriler.models import Kategori, KategoriOzellik

# Köpek kategorisi için özellikler
kopek = Kategori.objects.get(ad='Köpekler')

KategoriOzellik.objects.create(
    kategori=kopek,
    ad="Irk",
    alan_tipi="select",
    secenekler=["Golden Retriever", "Labrador", "Terrier", "Bulldog", "Pug", "Husky", "German Shepherd", "Diğer"],
    zorunlu=True,
    sira=1
)

KategoriOzellik.objects.create(
    kategori=kopek,
    ad="Yaş",
    alan_tipi="range",
    zorunlu=True,
    sira=2
)

# Diğer özellikler...
```

## 4️⃣ ALT KATEGORİLER OLUŞTURMA

Ana kategorilerin altına alt kategoriler ekleyin:

```python
python manage.py shell

# Shell içinde:
from apps.kategoriler.models import Kategori

kopek = Kategori.objects.get(ad='Köpekler')

# Alt kategoriler
alt_kategoriler = [
    "Golden Retriever", "Labrador", "Terrier", "Bulldog", "Pug", 
    "Husky", "German Shepherd", "Poodle", "Beagle", "Boxer"
]

for i, alt in enumerate(alt_kategoriler):
    Kategori.objects.create(
        ad=alt,
        parent=kopek,
        pet_type="dog",
        aciklama=f"{alt} köpek ırkı",
        sira=i+1
    )
```

## 5️⃣ KATEGORİ GÖRSELLERİ VE TEMA

**Ana Kategori Görselleri:**

Ana kategori temsili fotoğraflarını `/static/images/categories/` dizinine ekleyin:
- dog-category.jpg
- cat-category.jpg
- bird-category.jpg
- vb.

**CSS Stilleri:**

`/static/css/categories.css` dosyasında kategori kartları için stiller tanımlayın:

```css
.category-card {
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.category-card:hover {
    transform: translateY(-5px);
}

.category-icon {
    font-size: 2rem;
    margin-bottom: 15px;
}

/* Her kategori için özel renkler */
.category-dog { background-color: #f59e0b; color: white; }
.category-cat { background-color: #8b5cf6; color: white; }
/* diğer kategoriler... */
```

## 6️⃣ API TEST ETME

Kategori API'larını test edin:

```bash
# Ana kategorileri listele
curl http://localhost:8000/api/v1/kategoriler/ana_kategoriler/

# Kategori ağacını al
curl http://localhost:8000/api/v1/kategoriler/kategori_agaci/

# Popüler kategoriler
curl http://localhost:8000/api/v1/kategoriler/populer/
```

## 7️⃣ KATEGORİ İSTATİSTİKLERİ OLUŞTURMA

```bash
python manage.py shell

# Shell içinde:
from apps.kategoriler.models import Kategori
from django.db.models import F

# Kullanımı rastgele güncelle (test için)
kategoriler = Kategori.objects.all()
for i, kat in enumerate(kategoriler):
    kat.kullanim_sayisi = i * 10  # Rastgele sayı
    kat.save(update_fields=['kullanim_sayisi'])

# İstatistikleri kontrol et
from apps.kategoriler.servisler import KategoriService
print(KategoriService.kategori_istatistikleri())
```

## 8️⃣ KATEGORİ YÖNETİM SAYFASI (ADMİN)

Django admin panel üzerinden kategori yönetim sayfalarını ziyaret edin:

```
http://localhost:8000/admin/kategoriler/kategori/
```

Kategorileri düzenleyin, yeni kategoriler ekleyin ve mevcut kategorileri yönetin.

