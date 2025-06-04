# Pet Projesi Dizin Yapısı

## Ana Dizin Yapısı
```
/
├── apps/                   # Django uygulamalarının bulunduğu ana dizin
├── celery/                 # Celery asenkron görev yönetimi konfigürasyonu
├── config/                 # Django proje konfigürasyonu
├── deployment/             # Deployment ile ilgili konfigürasyon dosyaları
├── docker/                 # Docker konfigürasyon dosyaları
├── docs/                   # Proje dokümantasyonu
├── frontend/              # React tabanlı frontend uygulaması
├── logs/                  # Log dosyaları
├── media/                 # Kullanıcı yüklenen dosyalar
├── monitoring/            # Prometheus monitoring konfigürasyonu
├── scripts/               # Yardımcı scriptler
├── static/                # Statik dosyalar
├── staticfiles/           # Toplanan statik dosyalar
├── templates/             # Django HTML şablonları
├── tests/                 # Test dosyaları
└── utils/                 # Yardımcı Python modülleri

## Django Uygulamaları (apps/)
```
├── api/                   # API endpoint'leri (v1, v2)
├── basvurular/           # Başvuru yönetimi
├── bildirimler/          # Bildirim sistemi
├── blog/                 # Blog sistemi
├── etiketler/            # Etiket sistemi
├── favoriler/            # Favori işlemleri
├── hayvanlar/            # Hayvan kayıtları
├── ilanlar/              # İlan yönetimi
├── kategoriler/          # Kategori sistemi
├── kullanicilar/         # Kullanıcı yönetimi
├── mesajlasma/           # Mesajlaşma sistemi
├── ortak/                # Ortak kullanılan kodlar
└── raporlar/             # Raporlama sistemi
```

## Celery Yapısı
```
celery/
├── tasks/                # Asenkron görevler
│   ├── cleanup_tasks.py
│   ├── email_tasks.py
│   ├── image_tasks.py
│   └── notification_tasks.py
├── celery.py            # Celery konfigürasyonu
└── schedules.py         # Zamanlanmış görevler
```

## Frontend Yapısı
```
frontend/
├── public/              # Statik dosyalar
├── src/                 # Kaynak kodlar
├── package.json         # NPM paket konfigürasyonu
├── tsconfig.json        # TypeScript konfigürasyonu
└── webpack.config.js    # Webpack yapılandırması
```

## Test Yapısı
```
tests/
├── e2e/                # End-to-end testler
├── integration/        # Entegrasyon testleri
├── fixtures/           # Test fixture'ları
└── conftest.py         # Pytest konfigürasyonu
```

## Utility Modülleri
```
utils/
├── email.py            # Email işlemleri
├── helpers.py          # Yardımcı fonksiyonlar
├── image_processing.py # Görüntü işleme
├── pagination.py       # Sayfalama yardımcıları
├── permissions.py      # İzin kontrolleri
├── storage.py          # Depolama işlemleri
└── validators.py       # Veri doğrulama
```

## Konfigürasyon Dosyaları
- `requirements.txt`: Python bağımlılıkları
- `requirements-dev.txt`: Geliştirme ortamı bağımlılıkları
- `docker-compose.yml`: Docker compose konfigürasyonu
- `docker-compose.prod.yml`: Prodüksiyon Docker compose konfigürasyonu
- `Dockerfile`: Docker container yapılandırması
- `pytest.ini`: PyTest konfigürasyonu
- `setup.cfg`: Python paket konfigürasyonu
- `pyproject.toml`: Python proje metadata

## Dokümantasyon
`docs/` dizini altında:
- API dokümantasyonu
- Deployment kılavuzları
- Geliştirici dokümantasyonu
- Model açıklamaları
- Proje planları ve raporlar
