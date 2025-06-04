# Pet Projesi Dokümantasyonu

Bu dokümantasyon, Pet projesinin teknik detaylarını ve geliştirme süreçlerini açıklar.

## 1. Veritabanı Modeli ve İlişkiler

### Tablolar ve İlişkileri

```
Kullanıcı (apps.kullanicilar.models.Kullanici)
│
├── SahiplendirmeProfili (apps.kullanicilar.models.SahiplendirmeProfili)
│   └── kullanici (OneToOne) → Kullanıcı
│
Kategori (apps.kategoriler.models.Kategori)
│
├── FormAlanı (apps.kategoriler.models.FormAlanı)
│   └── kategori (ForeignKey) → Kategori
│
Hayvan (apps.hayvanlar.models.Hayvan)
│
├── HayvanFotograf (apps.hayvanlar.models.HayvanFotograf)
│   └── hayvan (ForeignKey) → Hayvan
│
├── tur (ForeignKey) → Kategori
│
├── sahiplendiren (ForeignKey) → Kullanıcı
```

### Önemli Model Alanları

- **Kullanıcı**: email, first_name, last_name, telefon, sehir, rol, durum
- **Kategori**: ad, slug, aciklama, pet_type, ikon_adi, renk_kodu
- **Hayvan**: ad, slug, tur, yas, cinsiyet, boyut, renk, aciklama, il, ilce, aktif, sahiplenildi

### Frontend İçin Model Şemaları

Frontend geliştirme için aşağıdaki TypeScript/JavaScript model tanımları kullanılabilir:

```typescript
// Kullanıcı modeli
interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  telefon?: string;
  sehir?: string;
  rol: string; // USER, ADMIN, vb.
  durum: string; // ACTIVE, INACTIVE, vb.
  profileImgUrl?: string;
}

// Hayvan modeli
interface Pet {
  id: number;
  ad: string;
  slug: string;
  tur: number; // Kategori ID referansı
  turAdi: string; // Kategori adı
  yas: string; // BABY, YOUNG, ADULT, SENIOR
  cinsiyet: string; // MALE, FEMALE, UNKNOWN
  boyut: string; // SMALL, MEDIUM, LARGE, vb.
  renk: string;
  kisirlastirilmis: boolean;
  asilarTamam: boolean;
  mikrocipli: boolean;
  karakterOzellikleri: string[];
  aciklama: string;
  il: string;
  ilce: string;
  aktif: boolean;
  sahiplenildi: boolean;
  fotograflar: string[]; // URL dizisi
  createdAt: string; // ISO tarih formatı
  updatedAt: string; // ISO tarih formatı
}
```

## 2. API Endpointleri

### Kullanıcı API

- `POST /api/kullanicilar/kayit/`: Yeni kullanıcı kaydı
  ```json
  // Girdi
  {
    "email": "ornek@example.com",
    "password": "guclu_sifre123",
    "first_name": "Ali",
    "last_name": "Veli"
  }
  
  // Çıktı
  {
    "id": 1,
    "email": "ornek@example.com",
    "first_name": "Ali",
    "last_name": "Veli"
  }
  ```

- `POST /api/kullanicilar/giris/`: Kullanıcı girişi (Token alımı)
  ```json
  // Girdi
  {
    "email": "ornek@example.com",
    "password": "guclu_sifre123"
  }
  
  // Çıktı
  {
    "token": "a3fce1d5c9b8e7..."
  }
  ```

- `GET /api/kullanicilar/profil/`: Mevcut kullanıcının profili
  - Authentication: Token gerektirir
  - Header: `Authorization: Token a3fce1d5c9b8e7...`

### Hayvan API

- `GET /api/hayvanlar/`: Hayvanları listele
  - Filtreler: tur, cinsiyet, boyut, il
  - Örnek: `GET /api/hayvanlar/?tur=1&cinsiyet=MALE&il=ISTANBUL`
  - Sayfalama: `GET /api/hayvanlar/?page=2&page_size=10`

- `GET /api/hayvanlar/{id}/`: Hayvan detayı

- `POST /api/hayvanlar/`: Yeni hayvan ekle
  - Authentication: Token gerektirir
  - Yetki: Kullanıcı rolü kontrol edilir
  - Multipart form için frontend örneği:
  ```javascript
  const formData = new FormData();
  formData.append('ad', 'Pamuk');
  formData.append('tur', '1');
  formData.append('cinsiyet', 'FEMALE');
  formData.append('fotograf', fotoFile);
  
  axios.post('/api/hayvanlar/', formData, {
    headers: {
      'Authorization': `Token ${userToken}`,
      'Content-Type': 'multipart/form-data'
    }
  });
  ```

### Kategori API

- `GET /api/kategoriler/`: Tüm kategorileri listele
- `GET /api/kategoriler/{id}/`: Kategori detayı
- `GET /api/kategoriler/{id}/formlar/`: Kategori için özel form alanları

## 3. Kullanıcı Rolleri ve Yetkilendirme

### Roller

- **USER**: Standart kullanıcı - ilanları görüntüleyebilir, başvuru yapabilir
- **SHELTER_STAFF**: Barınak personeli - hayvan ilanı ekleyebilir, başvuruları değerlendirebilir
- **VETERINARY**: Veteriner - hayvan sağlığı bilgilerini onaylayabilir
- **VOLUNTEER**: Gönüllü - özel erişim hakları vardır
- **MODERATOR**: Moderatör - içeriği denetleyebilir
- **ADMIN**: Yönetici - tam yetkiye sahiptir

### Yetkilendirme Mekanizması

- Token tabanlı kimlik doğrulama (Django REST Framework)
- Özel izin sınıfları (`permissions.py` dosyalarında tanımlanmıştır)
- Dekoratörler ile görünüm bazlı yetkilendirme

### Frontend İçin Kimlik Doğrulama

```javascript
// Login işlemi
const login = async (email, password) => {
  try {
    const response = await axios.post('/api/kullanicilar/giris/', {
      email,
      password
    });
    const { token } = response.data;
    
    // Token'ı localStorage'a kaydet
    localStorage.setItem('authToken', token);
    
    // Axios için default header ayarla
    axios.defaults.headers.common['Authorization'] = `Token ${token}`;
    
    return true;
  } catch (error) {
    console.error('Giriş hatası:', error);
    return false;
  }
};

// Yetkilendirme kontrolü
const checkPermission = (userRole, requiredRoles = []) => {
  const roleHierarchy = {
    'ADMIN': 50,
    'MODERATOR': 40,
    'VETERINARY': 30,
    'SHELTER_STAFF': 20,
    'VOLUNTEER': 10,
    'USER': 1
  };
  
  const userRoleValue = roleHierarchy[userRole] || 0;
  
  return requiredRoles.some(role => 
    userRoleValue >= (roleHierarchy[role] || 999)
  );
};
```

## 4. Ortak Fonksiyonlar ve Yardımcılar

### Yardımcı Fonksiyonlar

- `utils.validators`: Özel doğrulama fonksiyonları
  - `validate_turkish_phone`: Türkiye telefon numarası doğrulaması
  - `validate_forbidden_words`: Yasaklı kelimeleri kontrol eder

### Mixinler

- `BaseModelMixin`: Tüm modeller için ortak alanlar sağlar
  - created_at, updated_at, is_active gibi ortak alanlar içerir

### Managerlar

- `KullaniciManager`: Özel kullanıcı oluşturma metodları içerir

## 5. Ayarlar ve Ortam Değişkenleri

### Ortam Değişkenleri (.env)

```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=petdb
DB_USER=petuser
DB_PASSWORD=password
DB_HOST=localhost
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Ayarlar Modülleri

- `settings/base.py`: Temel ayarlar
- `settings/development.py`: Geliştirme ortamı ayarları
- `settings/production.py`: Canlı ortam ayarları

### Harici Servisler

- E-posta: SMTP üzerinden bildirimler
- Dosya Depolama: AWS S3 veya yerel depolama
- Ödeme: [Varsa ödeme servisi]

## 6. Kurulum ve Çalıştırma Talimatları

### Geliştirme Ortamı Kurulumu

```bash
# Sanal ortam oluşturma
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Bağımlılıkları yükleme
pip install -r requirements.txt

# Veritabanı migrasyonları
python manage.py migrate

# Test verileri yükleme
python manage.py loaddata initial_data

# Geliştirme sunucusu çalıştırma
python manage.py runserver
```

### Üretim Ortamı Kurulumu

- Gunicorn ve Nginx ile deployment
- PostgreSQL veritabanı konfigürasyonu
- Media dosyaları için statik dosya sunucusu

### Frontend Kurulumu

```bash
# Frontend dizinine git
cd frontend

# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm start

# Üretim için build
npm run build
```

## 7. Veri Akışı ve İş Süreçleri

### Kullanıcı Kaydı ve Doğrulama

1. Kullanıcı kayıt formunu doldurur
2. E-posta adresine doğrulama bağlantısı gönderilir
3. Kullanıcı bağlantıya tıklar ve e-posta doğrulanır
4. Kullanıcı profilini tamamlar

### Hayvan İlanı Oluşturma

1. Kullanıcı hayvan bilgilerini girer
2. Fotoğraflar yüklenir
3. İlan onay için bekletilir (DRAFT durumu)
4. Moderatör onayından sonra ilan yayınlanır (ACTIVE durumu)

### Sahiplenme Süreci

1. İlgilenen kullanıcı başvuru yapar
2. Sahiplendiren kullanıcı başvuruları değerlendirir
3. Kabul edilen başvuru sonrası iletişim bilgileri paylaşılır
4. Sahiplenme gerçekleştiğinde ilan durumu güncellenir (ADOPTED)

## 8. Testler ve Kod Standartları

### Test Yaklaşımı

- Unit testler: Modeller ve yardımcı fonksiyonlar için
- Entegrasyon testleri: API endpointleri için
- End-to-end testler: Kullanıcı akışları için

### Kod Standartları

- PEP 8 uyumlu kod yazımı
- Docstring standardı: Google stili
- Kod formatlaması için Black
- Kod analizi için Flake8

### CI/CD

- GitHub Actions ile otomatik testler
- Test coverage raporu oluşturma

## 9. Önemli Sabitler ve Enumlar

[Ayrıntılı bilgi için `degiskenler.md` dosyasına bakınız]

### Önemli Sabitler

- Hayvan türleri (KEDI, KOPEK, KUS, vb.)
- Boyut sabitleri (SMALL, MEDIUM, LARGE, vb.)
- İlan durumları (DRAFT, ACTIVE, ADOPTED, vb.)

### Choices Yapıları

- Cinsiyet seçenekleri (MALE, FEMALE, UNKNOWN)
- Kullanıcı durumları (ACTIVE, INACTIVE, SUSPENDED, BANNED)
- Bildirim türleri (APPLICATION_RECEIVED, NEW_MESSAGE, vb.)

## 10. Bağımlılıklar ve Harici Paketler

### Ana Bağımlılıklar

- **Django**: Web framework
- **Django REST Framework**: API geliştirme
- **Pillow**: Görüntü işleme
- **Celery**: Asenkron görevler
- **Redis**: Önbellek ve Celery broker'ı
- **PostgreSQL**: Veritabanı

### Frontend Kütüphaneleri

- **React**: Kullanıcı arayüzü
- **Axios**: HTTP istekleri
- **TailwindCSS**: UI tasarımı

## 11. Frontend Mimarisi

### Proje Yapısı

```
frontend/
├── public/              # Statik dosyalar
├── src/
│   ├── api/             # API servis fonksiyonları
│   ├── assets/          # Görseller, fontlar ve diğer statik varlıklar
│   ├── components/      # Ortak kullanılan bileşenler
│   │   ├── common/      # Header, Footer, Button gibi temel bileşenler
│   │   └── forms/       # Form bileşenleri
│   ├── contexts/        # React Context'leri (Auth, Theme, vb.)
│   ├── hooks/           # Özel React hook'ları
│   ├── pages/           # Sayfa bazlı bileşenler
│   ├── routes/          # Rota tanımları
│   ├── store/           # Global durum yönetimi (Redux/Zustand)
│   ├── styles/          # Global ve tema stilleri
│   ├── types/           # TypeScript için tip tanımları
│   └── utils/           # Yardımcı fonksiyonlar
├── .env                 # Ortam değişkenleri
├── package.json         # Bağımlılıklar ve script'ler
└── tsconfig.json        # TypeScript yapılandırması
```

### Önemli Bileşen Yapısı

```jsx
// Örnek hayvan listesi bileşeni
const PetList = () => {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ tur: '', cinsiyet: '' });
  
  useEffect(() => {
    const fetchPets = async () => {
      try {
        const queryString = new URLSearchParams(filters).toString();
        const response = await axios.get(`/api/hayvanlar/?${queryString}`);
        setPets(response.data.results);
      } catch (error) {
        console.error('Hayvanlar yüklenirken hata:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchPets();
  }, [filters]);
  
  // Render kodları...
};
```

### API Entegrasyonu

API istekleri için `api` klasörü altında servis fonksiyonları oluşturun:

```javascript
// src/api/petService.js
import axios from 'axios';

export const getPets = async (filters = {}) => {
  try {
    const queryString = new URLSearchParams(filters).toString();
    const response = await axios.get(`/api/hayvanlar/?${queryString}`);
    return response.data;
  } catch (error) {
    console.error('API hatası:', error);
    throw error;
  }
};

export const getPetById = async (id) => {
  try {
    const response = await axios.get(`/api/hayvanlar/${id}/`);
    return response.data;
  } catch (error) {
    console.error('API hatası:', error);
    throw error;
  }
};
```

## 12. Yeni Uygulama Entegrasyonu Rehberi

### Yeni Django Uygulaması Ekleme

1. Uygulama oluşturma
   ```bash
   python manage.py startapp yeniuygulama
   
   # veya apps dizini içine
   mkdir -p apps/yeniuygulama
   python manage.py startapp yeniuygulama apps/yeniuygulama
   ```

2. Uygulama yapılandırması (apps.py):
   ```python
   # apps/yeniuygulama/apps.py
   from django.apps import AppConfig

   class YeniUygulamaConfig(AppConfig):
       default_auto_field = 'django.db.models.BigAutoField'
       name = 'apps.yeniuygulama'
       verbose_name = 'Yeni Uygulama'
   ```

3. Uygulamayı settings.py'a ekle:
   ```python
   # settings.py
   INSTALLED_APPS = [
       # ...mevcut uygulamalar...
       'apps.yeniuygulama',
   ]
   ```

4. URL yapılandırması:
   ```python
   # urls.py (ana proje)
   urlpatterns = [
       # ...mevcut URL'ler...
       path('api/yeniuygulama/', include('apps.yeniuygulama.urls')),
   ]
   
   # apps/yeniuygulama/urls.py
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.YeniViewSet.as_view({'get': 'list', 'post': 'create'})),
       path('<int:pk>/', views.YeniViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
   ]
   ```

5. Model örneği:
   ```python
   # apps/yeniuygulama/models.py
   from django.db import models
   from apps.ortak.models import BaseModelMixin
   
   class YeniModel(BaseModelMixin):
       baslik = models.CharField(max_length=100)
       aciklama = models.TextField()
       
       class Meta:
           verbose_name = "Yeni Model"
           verbose_name_plural = "Yeni Modeller"
   ```

6. Serializer örneği:
   ```python
   # apps/yeniuygulama/serializers.py
   from rest_framework import serializers
   from .models import YeniModel
   
   class YeniModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = YeniModel
           fields = ['id', 'baslik', 'aciklama', 'created_at', 'updated_at']
   ```

7. View örneği:
   ```python
   # apps/yeniuygulama/views.py
   from rest_framework import viewsets
   from .models import YeniModel
   from .serializers import YeniModelSerializer
   
   class YeniViewSet(viewsets.ModelViewSet):
       queryset = YeniModel.objects.all()
       serializer_class = YeniModelSerializer
   ```

8. Veritabanı migrasyonu:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Frontend ile Yeni Uygulama Entegrasyonu

1. API servis dosyası oluşturma:
   ```javascript
   // frontend/src/api/yeniService.js
   import axios from 'axios';

   export const getYeniItems = async () => {
     try {
       const response = await axios.get('/api/yeniuygulama/');
       return response.data;
     } catch (error) {
       console.error('API hatası:', error);
       throw error;
     }
   };
   ```

2. React bileşenleri oluşturma:
   ```jsx
   // frontend/src/pages/YeniListe.jsx
   import { useState, useEffect } from 'react';
   import { getYeniItems } from '../api/yeniService';

   const YeniListe = () => {
     const [items, setItems] = useState([]);
     const [loading, setLoading] = useState(true);

     useEffect(() => {
       const loadItems = async () => {
         try {
           const data = await getYeniItems();
           setItems(data);
         } catch (error) {
           console.error(error);
         } finally {
           setLoading(false);
         }
       };

       loadItems();
     }, []);

     if (loading) return <div>Yükleniyor...</div>;

     return (
       <div>
         <h1>Yeni Öğeler</h1>
         <ul>
           {items.map(item => (
             <li key={item.id}>{item.baslik}</li>
           ))}
         </ul>
       </div>
     );
   };

   export default YeniListe;
   ```

3. Router'a yeni sayfayı ekle:
   ```jsx
   // frontend/src/routes/index.jsx
   import { BrowserRouter, Routes, Route } from 'react-router-dom';
   import YeniListe from '../pages/YeniListe';

   const AppRoutes = () => {
     return (
       <BrowserRouter>
         <Routes>
           {/* ...mevcut rotalar... */}
           <Route path="/yeni" element={<YeniListe />} />
         </Routes>
       </BrowserRouter>
     );
   };

   export default AppRoutes;
   ```

### Ortak State Kullanımı

1. Context API kullanarak yeni uygulama için veri sağlayıcı:
   ```jsx
   // frontend/src/contexts/YeniContext.jsx
   import { createContext, useState, useContext, useEffect } from 'react';
   import { getYeniItems } from '../api/yeniService';

   const YeniContext = createContext();

   export const YeniProvider = ({ children }) => {
     const [items, setItems] = useState([]);
     const [loading, setLoading] = useState(true);

     useEffect(() => {
       fetchItems();
     }, []);

     const fetchItems = async () => {
       try {
         setLoading(true);
         const data = await getYeniItems();
         setItems(data);
       } catch (error) {
         console.error(error);
       } finally {
         setLoading(false);
       }
     };

     return (
       <YeniContext.Provider value={{ items, loading, refreshItems: fetchItems }}>
         {children}
       </YeniContext.Provider>
     );
   };

   export const useYeni = () => useContext(YeniContext);
   ```

2. Context'i uygulamanıza ekleyin:
   ```jsx
   // frontend/src/App.jsx
   import { YeniProvider } from './contexts/YeniContext';
   import AppRoutes from './routes';

   const App = () => {
     return (
       <YeniProvider>
         <AppRoutes />
       </YeniProvider>
     );
   };

   export default App;
   ```
