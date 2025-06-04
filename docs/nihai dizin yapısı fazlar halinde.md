EVCİL HAYVAN SAHİPLENME PLATFORMU - OPTİMAL GELİŞTİRME SIRASI
FAZ 1 (T1): TEMEL ALTYAPI VE ORTAK MODÜLLER

=================================================================================
Proje Temeli ve Genel Yapılandırma
Code

[T-001] README.md                           # Proje tanıtım ve kurulum kılavuzu
[T-002] .gitignore                          # Git versiyonlama hariç tutulacaklar
[T-003] .env.example                        # Çevre değişkenleri şablonu
[T-004] requirements.txt                    # Python temel bağımlılıkları
[T-005] requirements-dev.txt                # Geliştirme ortamı bağımlılıkları
[T-006] pyproject.toml                      # Python proje metadata yapılandırması
[T-007] setup.cfg                           # Python paket yapılandırması
[T-008] pytest.ini                          # Test framework yapılandırması

Django Temel Konfigürasyon
Code

[T-009] manage.py                           # Django yönetim betiği
[T-010] config/__init__.py                  # Konfigürasyon paket tanımı
[T-011] config/settings/__init__.py         # Ayarlar paket tanımı
[T-012] config/settings/base.py             # Temel Django ayarları
[T-013] config/settings/development.py      # Geliştirme ortamı ayarları
[T-014] config/settings/testing.py          # Test ortamı ayarları
[T-015] config/wsgi.py                      # Web sunucu ağ geçidi arayüzü
[T-016] config/asgi.py                      # Asenkron sunucu ağ geçidi arayüzü (temel)
[T-017] config/urls.py                      # Ana URL yönlendirme yapılandırması

Ortak Modüller (Tüm Uygulamalar İçin Temel)
Code

[T-018] apps/__init__.py                    # Uygulamalar ana paket tanımı
[T-019] apps/ortak/__init__.py              # Ortak modül paket tanımı
[T-020] apps/ortak/models.py                # Temel model sınıfları (TimestampedModel, AbstractBaseModel)
[T-021] apps/ortak/validators.py            # Veri doğrulama kuralları
[T-022] apps/ortak/permissions.py           # İzin kontrol sınıfları
[T-023] apps/ortak/exceptions.py            # Özel hata sınıfları
[T-024] apps/ortak/constants.py             # Sabit değerler tanımları
[T-025] apps/ortak/managers.py              # Veritabanı yöneticisi sınıfları
[T-026] apps/ortak/filters.py               # Filtreleme sınıfları
[T-027] apps/ortak/pagination.py            # Sayfalama yardımcı sınıfları

API Temel Yapısı
Code

[T-028] apps/api/__init__.py                # API paket tanımı
[T-029] apps/api/v1/__init__.py             # API v1 paket tanımı
[T-030] apps/api/v1/permissions.py          # API izin kontrolleri
[T-031] apps/api/v1/urls.py                 # API v1 URL yapılandırması (boş, includes eklenecek)
[T-032] apps/api/v1/serializers.py          # API v1 ortak serializerlar

Yardımcı Modüller (Utils)
Code

[T-033] utils/__init__.py                   # Yardımcı modüller paket tanımı
[T-034] utils/helpers.py                    # Genel yardımcı fonksiyonlar
[T-035] utils/validators.py                 # Veri doğrulama yardımcıları
[T-036] utils/permissions.py                # İzin kontrol yardımcıları
[T-037] utils/email.py                      # E-posta işlem yardımcıları
[T-038] utils/storage.py                    # Dosya depolama yardımcıları
[T-039] utils/image_processing.py           # Görüntü işleme yardımcıları

Docker Temel Yapı
Code

[T-040] Dockerfile                          # Temel Docker container tanımı
[T-041] docker-compose.yml                  # Geliştirme ortamı compose yapılandırması

FAZ 2 (K1): KULLANICI SİSTEMİ (TÜM SİSTEMİN TEMELİ)

=================================================================================
Kullanıcı Uygulaması Core
Code

[K-001] apps/kullanicilar/__init__.py       # Kullanıcı uygulaması paket tanımı
[K-002] apps/kullanicilar/apps.py           # Django uygulama yapılandırması
[K-003] apps/kullanicilar/models.py         # Kullanıcı modeli ve profil modelleri
[K-004] apps/kullanicilar/managers.py       # Kullanıcı yöneticisi sınıfları
[K-005] apps/kullanicilar/permissions.py    # Kullanıcı özel izinleri
[K-006] apps/kullanicilar/validators.py     # Kullanıcı veri doğrulama kuralları
[K-007] apps/kullanicilar/signals.py        # Kullanıcı olayları (kayıt sonrası işlemler)
[K-008] apps/kullanicilar/admin.py          # Django admin panel ayarları
[K-009] apps/kullanicilar/migrations/__init__.py  # Veritabanı migrasyon paket tanımı

Kullanıcı API Katmanı
Code

[K-010] apps/kullanicilar/serializers.py    # API veri serileştirme sınıfları
[K-011] apps/kullanicilar/views.py          # API endpoint görünümleri
[K-012] apps/kullanicilar/urls.py           # Kullanıcı URL yönlendirmeleri
[K-013] apps/kullanicilar/servisler.py      # İş mantığı hizmet sınıfları
[K-014] apps/kullanicilar/filters.py        # Kullanıcı filtreleme sınıfları

API Entegrasyonu
Code

[K-015] apps/api/v1/urls.py                 # kullanicilar include eklenmesi

FAZ 3 (KT1): KATEGORİ SİSTEMİ (HAYVAN MODELİNDEN ÖNCE GELMELİ)

=================================================================================
Kategori Uygulaması
Code

[KT-001] apps/kategoriler/__init__.py       # Kategori uygulaması paket tanımı
[KT-002] apps/kategoriler/apps.py           # Django uygulama yapılandırması
[KT-003] apps/kategoriler/models.py         # Kategori modeli (hiyerarşik yapı)
[KT-004] apps/kategoriler/managers.py       # Kategori yöneticisi sınıfları
[KT-005] apps/kategoriler/admin.py          # Django admin panel ayarları
[KT-006] apps/kategoriler/serializers.py    # API veri serileştirme sınıfları
[KT-007] apps/kategoriler/views.py          # API endpoint görünümleri
[KT-008] apps/kategoriler/urls.py           # Kategori URL yönlendirmeleri
[KT-009] apps/kategoriler/servisler.py      # İş mantığı hizmet sınıfları
[KT-010] apps/kategoriler/migrations/__init__.py  # Veritabanı migrasyon paket tanımı

FAZ 4 (E1): ETİKET SİSTEMİ (HAYVAN VE İLAN MODELLERİNDE KULLANILACAK)

=================================================================================
Etiket Uygulaması
Code

[E-001] apps/etiketler/__init__.py          # Etiket uygulaması paket tanımı
[E-002] apps/etiketler/apps.py              # Django uygulama yapılandırması
[E-003] apps/etiketler/models.py            # Etiket modeli ve Many-to-Many ilişkiler
[E-004] apps/etiketler/managers.py          # Etiket yöneticisi sınıfları
[E-005] apps/etiketler/admin.py             # Django admin panel ayarları
[E-006] apps/etiketler/serializers.py       # API veri serileştirme sınıfları
[E-007] apps/etiketler/views.py             # API endpoint görünümleri
[E-008] apps/etiketler/urls.py              # Etiket URL yönlendirmeleri
[E-009] apps/etiketler/servisler.py         # İş mantığı hizmet sınıfları
[E-010] apps/etiketler/filters.py           # Etiket filtreleme sınıfları
[E-011] apps/etiketler/migrations/__init__.py  # Veritabanı migrasyon paket tanımı

FAZ 5 (H1): HAYVAN MODELİ (KATEGORİ VE ETİKET BAĞIMLILIĞI VAR)

=================================================================================
Hayvan Uygulaması Core
Code

[H-001] apps/hayvanlar/__init__.py          # Hayvan uygulaması paket tanımı
[H-002] apps/hayvanlar/apps.py              # Django uygulama yapılandırması
[H-003] apps/hayvanlar/models.py            # Hayvan modeli (kategori FK, etiket M2M kullanır)
[H-004] apps/hayvanlar/managers.py          # Hayvan yöneticisi sınıfları
[H-005] apps/hayvanlar/utils.py             # Hayvan özel yardımcı fonksiyonlar
[H-006] apps/hayvanlar/signals.py           # Hayvan olayları (kayıt/güncelleme sonrası)
[H-007] apps/hayvanlar/admin.py             # Django admin panel ayarları
[H-008] apps/hayvanlar/migrations/__init__.py  # Veritabanı migrasyon paket tanımı

Hayvan API Katmanı
Code

[H-009] apps/hayvanlar/serializers.py       # API veri serileştirme sınıfları
[H-010] apps/hayvanlar/views.py             # API endpoint görünümleri
[H-011] apps/hayvanlar/urls.py              # Hayvan URL yönlendirmeleri
[H-012] apps/hayvanlar/servisler.py         # İş mantığı hizmet sınıfları
[H-013] apps/hayvanlar/filters.py           # Hayvan filtreleme sınıfları

FAZ 6 (I1): İLAN SİSTEMİ (MVP - HAYVAN BAĞIMLILIĞI VAR)

=================================================================================
İlan Uygulaması Core
Code

[I-001] apps/ilanlar/__init__.py            # İlan uygulaması paket tanımı
[I-002] apps/ilanlar/apps.py                # Django uygulama yapılandırması
[I-003] apps/ilanlar/models.py              # İlan modeli (hayvan FK, etiket M2M kullanır)
[I-004] apps/ilanlar/managers.py            # İlan yöneticisi sınıfları
[I-005] apps/ilanlar/permissions.py         # İlan özel izinleri
[I-006] apps/ilanlar/signals.py             # İlan olayları
[I-007] apps/ilanlar/admin.py               # Django admin panel ayarları
[I-008] apps/ilanlar/migrations/__init__.py # Veritabanı migrasyon paket tanımı

İlan API Katmanı
Code

[I-009] apps/ilanlar/serializers.py         # API veri serileştirme sınıfları
[I-010] apps/ilanlar/views.py               # API endpoint görünümleri
[I-011] apps/ilanlar/urls.py                # İlan URL yönlendirmeleri
[I-012] apps/ilanlar/servisler.py           # İş mantığı hizmet sınıfları
[I-013] apps/ilanlar/filters.py             # İlan filtreleme sınıfları

API Core Güncellemesi (MVP Tamamlandı)
Code

[I-014] apps/api/v1/urls.py                 # kategoriler, etiketler, hayvanlar, ilanlar include

FAZ 7 (B1): BAŞVURU SİSTEMİ (MVP - İLAN BAĞIMLILIĞI VAR)

=================================================================================
Başvuru Uygulaması
Code

[B-001] apps/basvurular/__init__.py         # Başvuru uygulaması paket tanımı
[B-002] apps/basvurular/apps.py             # Django uygulama yapılandırması
[B-003] apps/basvurular/models.py           # Başvuru modeli (ilan FK kullanır)
[B-004] apps/basvurular/managers.py         # Başvuru yöneticisi sınıfları
[B-005] apps/basvurular/permissions.py      # Başvuru özel izinleri
[B-006] apps/basvurular/signals.py          # Başvuru olayları
[B-007] apps/basvurular/admin.py            # Django admin panel ayarları
[B-008] apps/basvurular/serializers.py      # API veri serileştirme sınıfları
[B-009] apps/basvurular/views.py            # API endpoint görünümleri
[B-010] apps/basvurular/urls.py             # Başvuru URL yönlendirmeleri
[B-011] apps/basvurular/servisler.py        # İş mantığı hizmet sınıfları
[B-012] apps/basvurular/filters.py          # Başvuru filtreleme sınıfları
[B-013] apps/basvurular/migrations/__init__.py  # Veritabanı migrasyon paket tanımı

FAZ 8 (F1): FRONTEND TEMEL KURULUM VE ALTYAPI

=================================================================================
React Temel Kurulum
Code

[F-001] frontend/package.json               # NPM paket bağımlılıkları ve betikler
[F-002] frontend/tsconfig.json              # TypeScript yapılandırması
[F-003] frontend/webpack.config.js          # Webpack yapılandırması
[F-004] frontend/public/index.html          # Ana HTML şablonu
[F-005] frontend/public/favicon.ico         # Site ikonu
[F-006] frontend/src/index.js               # React uygulaması giriş noktası
[F-007] frontend/src/App.js                 # Ana React bileşeni

Frontend Temel Hizmetler
Code

[F-008] frontend/src/hizmetler/api.js       # Temel API iletişim katmanı
[F-009] frontend/src/hizmetler/auth.js      # Kimlik doğrulama hizmetleri
[F-010] frontend/src/yonlendirme/Rotalar.js # React Router yapılandırması
[F-011] frontend/src/stiller/global.css     # Global CSS stilleri
[F-012] frontend/src/stiller/degiskenler.css # CSS değişkenleri
[F-013] frontend/src/stiller/tema.css       # Tema stilleri

FAZ 9 (F2): FRONTEND TEMEL BİLEŞENLER VE KULLANICI SİSTEMİ

=================================================================================
Ortak Bileşenler
Code

[F-014] frontend/src/bilesenler/ortak/Dugme.js        # Yeniden kullanılabilir buton bileşeni
[F-015] frontend/src/bilesenler/ortak/YuklemeDurumu.js # Yükleme durumu göstergesi
[F-016] frontend/src/bilesenler/ortak/HataMesaji.js   # Hata mesajı bileşeni
[F-017] frontend/src/bilesenler/ortak/ModalPencere.js # Modal pencere bileşeni
[F-018] frontend/src/bilesenler/ortak/Pagination.js   # Sayfalama bileşeni

Kullanıcı Sistemi Frontend
Code

[F-019] frontend/src/hizmetler/kullaniciService.js # Kullanıcı API çağrıları
[F-020] frontend/src/baglamlar/AuthContext.js      # Kimlik doğrulama bağlamı
[F-021] frontend/src/bilesenler/form/GirisFormu.js # Giriş formu bileşeni
[F-022] frontend/src/bilesenler/form/KayitFormu.js # Kayıt formu bileşeni
[F-023] frontend/src/sayfalar/GirisSayfasi.js      # Giriş sayfası
[F-024] frontend/src/sayfalar/KayitSayfasi.js      # Kayıt sayfası

Navigation ve Layout
Code

[F-025] frontend/src/bilesenler/header/NavBar.js     # Navigasyon çubuğu
[F-026] frontend/src/bilesenler/header/KullaniciMenu.js # Kullanıcı menü bileşeni
[F-027] frontend/src/bilesenler/footer/Footer.js     # Footer bileşeni
[F-028] frontend/src/yonlendirme/OzelRotalar.js     # Korumalı rotalar

Custom Hooks
Code

[F-029] frontend/src/kancalar/useForm.js       # Form yönetimi hook'u
[F-030] frontend/src/kancalar/usePagination.js # Sayfalama hook'u
[F-031] frontend/src/kancalar/useAuth.js       # Kimlik doğrulama hook'u

FAZ 10 (F3): FRONTEND ANA İŞLEVSELLİK (MVP)

=================================================================================
Hayvan ve Kategori Sistemi
Code

[F-032] frontend/src/hizmetler/hayvanService.js    # Hayvan API çağrıları
[F-033] frontend/src/hizmetler/kategoriService.js  # Kategori API çağrıları
[F-034] frontend/src/hizmetler/etiketService.js    # Etiket API çağrıları
[F-035] frontend/src/bilesenler/kartlar/HayvanKarti.js    # Hayvan kart bileşeni
[F-036] frontend/src/bilesenler/kartlar/KategoriKarti.js  # Kategori kart bileşeni
[F-037] frontend/src/paneller/HayvanListesiPaneli.js      # Hayvan listesi paneli
[F-038] frontend/src/sayfalar/HayvanlarSayfasi.js         # Hayvanlar sayfası

İlan Sistemi
Code

[F-039] frontend/src/hizmetler/ilanService.js      # İlan API çağrıları
[F-040] frontend/src/bilesenler/kartlar/IlanKarti.js      # İlan kart bileşeni
[F-041] frontend/src/bilesenler/form/IlanFormu.js         # İlan oluşturma formu
[F-042] frontend/src/sayfalar/AnaSayfa.js                 # Ana sayfa (ilanlar listesi)
[F-043] frontend/src/sayfalar/IlanOlusturSayfasi.js       # İlan oluştur sayfası

FAZ 11 (F4): FRONTEND DETAY SAYFALARI VE BAŞVURU SİSTEMİ

=================================================================================
Detay Sayfaları
Code

[F-044] frontend/src/paneller/HayvanDetayPaneli.js    # Hayvan detay paneli
[F-045] frontend/src/sayfalar/HayvanDetaySayfasi.js   # Hayvan detay sayfası
[F-046] frontend/src/sayfalar/IlanDetaySayfasi.js     # İlan detay sayfası

Başvuru Sistemi
Code

[F-047] frontend/src/hizmetler/basvuruService.js      # Başvuru API çağrıları
[F-048] frontend/src/bilesenler/form/BasvuruFormu.js  # Başvuru formu bileşeni
[F-049] frontend/src/sayfalar/SahiplenmeBasvuruSayfasi.js # Başvuru sayfası
[F-050] frontend/src/sayfalar/BasvurularimSayfasi.js   # Kullanıcı başvuruları

FAZ 12 (BL1): BİLDİRİM SİSTEMİ (MESAJLAŞMA ÖNCESİ TEMEL)

=================================================================================
Bildirim Uygulaması
Code

[BL-001] apps/bildirimler/__init__.py       # Bildirim uygulaması paket tanımı
[BL-002] apps/bildirimler/apps.py           # Django uygulama yapılandırması
[BL-003] apps/bildirimler/models.py         # Bildirim modeli
[BL-004] apps/bildirimler/managers.py       # Bildirim yöneticisi sınıfları
[BL-005] apps/bildirimler/permissions.py    # Bildirim özel izinleri
[BL-006] apps/bildirimler/signals.py        # Bildirim olayları
[BL-007] apps/bildirimler/admin.py          # Django admin panel ayarları
[BL-008] apps/bildirimler/serializers.py    # API veri serileştirme sınıfları
[BL-009] apps/bildirimler/views.py          # API endpoint görünümleri
[BL-010] apps/bildirimler/urls.py           # Bildirim URL yönlendirmeleri
[BL-011] apps/bildirimler/servisler.py      # İş mantığı hizmet sınıfları
[BL-012] apps/bildirimler/migrations/__init__.py # Veritabanı migrasyon paket tanımı

FAZ 13 (M1): MESAJLAŞMA SİSTEMİ (BİLDİRİM BAĞIMLILIĞI VAR)

=================================================================================
Mesajlaşma Uygulaması Core
Code

[M-001] apps/mesajlasma/__init__.py         # Mesajlaşma uygulaması paket tanımı
[M-002] apps/mesajlasma/apps.py             # Django uygulama yapılandırması
[M-003] apps/mesajlasma/models.py           # Mesaj ve sohbet modelleri
[M-004] apps/mesajlasma/managers.py         # Mesajlaşma yöneticisi sınıfları
[M-005] apps/mesajlasma/permissions.py      # Mesajlaşma özel izinleri
[M-006] apps/mesajlasma/signals.py          # Mesajlaşma olayları
[M-007] apps/mesajlasma/admin.py            # Django admin panel ayarları
[M-008] apps/mesajlasma/migrations/__init__.py # Veritabanı migrasyon paket tanımı

WebSocket ve Real-time
Code

[M-009] apps/mesajlasma/consumers.py        # WebSocket consumer sınıfları
[M-010] apps/mesajlasma/routing.py          # WebSocket URL yönlendirmeleri  
[M-011] config/asgi.py                      # ASGI WebSocket routing güncellemesi

Mesajlaşma API
Code

[M-012] apps/mesajlasma/serializers.py      # API veri serileştirme sınıfları
[M-013] apps/mesajlasma/views.py            # API endpoint görünümleri
[M-014] apps/mesajlasma/urls.py             # Mesajlaşma URL yönlendirmeleri
[M-015] apps/mesajlasma/servisler.py        # İş mantığı hizmet sınıfları

FAZ 14 (FV1): FAVORİLER SİSTEMİ

=================================================================================
Favoriler Uygulaması
Code

[FV-001] apps/favoriler/__init__.py         # Favoriler uygulaması paket tanımı
[FV-002] apps/favoriler/apps.py             # Django uygulama yapılandırması
[FV-003] apps/favoriler/models.py           # Favori modeli
[FV-004] apps/favoriler/managers.py         # Favori yöneticisi sınıfları
[FV-005] apps/favoriler/permissions.py      # Favori özel izinleri
[FV-006] apps/favoriler/admin.py            # Django admin panel ayarları
[FV-007] apps/favoriler/serializers.py      # API veri serileştirme sınıfları
[FV-008] apps/favoriler/views.py            # API endpoint görünümleri
[FV-009] apps/favoriler/urls.py             # Favori URL yönlendirmeleri
[FV-010] apps/favoriler/servisler.py        # İş mantığı hizmet sınıfları
[FV-011] apps/favoriler/migrations/__init__.py # Veritabanı migrasyon paket tanımı

FAZ 15 (F5): FRONTEND İKİNCİL ÖZELLİKLER

=================================================================================
Bildirim ve Mesajlaşma Frontend
Code

[F-051] frontend/src/hizmetler/bildirimService.js  # Bildirim API çağrıları
[F-052] frontend/src/baglamlar/BildirimBaglami.js  # Bildirim bağlamı
[F-053] frontend/src/bilesenler/ortak/BildirimToast.js # Toast bildirim bileşeni
[F-054] frontend/src/hizmetler/mesajService.js     # Mesaj API çağrıları
[F-055] frontend/src/paneller/MesajlarPaneli.js    # Mesajlar paneli
[F-056] frontend/src/sayfalar/MesajlarSayfasi.js   # Mesajlar sayfası

Favoriler Frontend
Code

[F-057] frontend/src/hizmetler/favoriService.js    # Favori API çağrıları
[F-058] frontend/src/kancalar/useFavoriler.js      # Favoriler hook'u
[F-059] frontend/src/bilesenler/ozel/FavoriButonu.js # Favori buton bileşeni
[F-060] frontend/src/sayfalar/FavorilerSayfasi.js  # Favoriler sayfası

Profil ve Tema
Code

[F-061] frontend/src/sayfalar/ProfilSayfasi.js     # Profil sayfası
[F-062] frontend/src/baglamlar/TemaBaglami.js      # Tema bağlamı
[F-063] frontend/src/bilesenler/form/ProfilFormu.js # Profil düzenleme formu

FAZ 16 (C1): CELERY VE ASENKRON GÖREVLER

=================================================================================
Celery Temel Kurulum
Code

[C-001] celery/__init__.py                  # Celery paket tanımı
[C-002] celery/celery.py                    # Celery yapılandırması
[C-003] celery/schedules.py                 # Zamanlanmış görevler
[C-004] config/celery.py                    # Django-Celery entegrasyonu

Asenkron Görevler
Code

[C-005] celery/tasks/__init__.py            # Görevler paket tanımı
[C-006] celery/tasks/email_tasks.py         # E-posta gönderim görevleri
[C-007] celery/tasks/notification_tasks.py  # Bildirim gönderim görevleri
[C-008] celery/tasks/image_tasks.py         # Görüntü işleme görevleri
[C-009] celery/tasks/cleanup_tasks.py       # Temizlik görevleri

Uygulama Entegrasyonları
Code

[C-010] apps/basvurular/tasks.py            # Başvuru ile ilgili görevler
[C-011] apps/bildirimler/tasks.py           # Bildirim ile ilgili görevler
[C-012] apps/ilanlar/tasks.py               # İlan ile ilgili görevler
[C-013] apps/kullanicilar/tasks.py          # Kullanıcı ile ilgili görevler

FAZ 17 (BG1): BLOG SİSTEMİ (BAĞIMSIZ MODÜL)

=================================================================================
Blog Uygulaması
Code

[BG-001] apps/blog/__init__.py              # Blog uygulaması paket tanımı
[BG-002] apps/blog/apps.py                  # Django uygulama yapılandırması
[BG-003] apps/blog/models.py                # Blog yazısı ve kategori modelleri
[BG-004] apps/blog/managers.py              # Blog yöneticisi sınıfları
[BG-005] apps/blog/filters.py               # Blog filtreleme sınıfları
[BG-006] apps/blog/permissions.py           # Blog özel izinleri
[BG-007] apps/blog/admin.py                 # Django admin panel ayarları
[BG-008] apps/blog/serializers.py           # API veri serileştirme sınıfları
[BG-009] apps/blog/views.py                 # API endpoint görünümleri
[BG-010] apps/blog/urls.py                  # Blog URL yönlendirmeleri
[BG-011] apps/blog/servisler.py             # İş mantığı hizmet sınıfları
[BG-012] apps/blog/migrations/__init__.py   # Veritabanı migrasyon paket tanımı

Blog Frontend
Code

[BG-013] frontend/src/hizmetler/blogService.js    # Blog API çağrıları
[BG-014] frontend/src/bilesenler/kartlar/BlogKarti.js    # Blog kart bileşeni
[BG-015] frontend/src/sayfalar/BlogSayfasi.js     # Blog ana sayfası
[BG-016] frontend/src/sayfalar/BlogDetaySayfasi.js # Blog detay sayfası

FAZ 18 (R1): RAPOR VE İSTATİSTİK SİSTEMİ

=================================================================================
Raporlar Uygulaması
Code

[R-001] apps/raporlar/__init__.py           # Raporlar uygulaması paket tanımı
[R-002] apps/raporlar/apps.py               # Django uygulama yapılandırması
[R-003] apps/raporlar/models.py             # Rapor modelleri
[R-004] apps/raporlar/managers.py           # Rapor yöneticisi sınıfları
[R-005] apps/raporlar/permissions.py        # Rapor özel izinleri
[R-006] apps/raporlar/admin.py              # Django admin panel ayarları
[R-007] apps/raporlar/serializers.py        # API veri serileştirme sınıfları
[R-008] apps/raporlar/views.py              # API endpoint görünümleri
[R-009] apps/raporlar/urls.py               # Rapor URL yönlendirmeleri
[R-010] apps/raporlar/servisler.py          # İş mantığı hizmet sınıfları
[R-011] apps/raporlar/tasks.py              # Rapor ile ilgili görevler
[R-012] apps/raporlar/migrations/__init__.py # Veritabanı migrasyon paket tanımı

Raporlar Frontend
Code

[R-013] frontend/src/hizmetler/raporService.js    # Rapor API çağrıları
[R-014] frontend/src/paneller/IstatistikPaneli.js # İstatistik paneli
[R-015] frontend/src/sayfalar/RaporlarSayfasi.js  # Raporlar sayfası

FAZ 19 (P1): PRODÜKSİYON AYARLARI VE DOCKER

=================================================================================
Prodüksiyon Konfigürasyonu
Code

[P-001] config/settings/production.py       # Prodüksiyon Django ayarları
[P-002] docker/Dockerfile.prod              # Prodüksiyon Docker container
[P-003] docker/Dockerfile.dev               # Geliştirme Docker container
[P-004] docker-compose.prod.yml             # Prodüksiyon compose yapılandırması

Deployment Konfigürasyonu
Code

[P-005] deployment/nginx/nginx.conf         # Nginx web sunucu yapılandırması
[P-006] deployment/nginx/ssl.conf           # SSL sertifika yapılandırması
[P-007] deployment/docker/docker-compose.prod.yml # Prodüksiyon compose
[P-008] scripts/deployment/deploy.sh        # Deployment betiği
[P-009] scripts/deployment/backup.sh        # Yedekleme betiği

FAZ 20 (T2): TEST ALTYAPISI VE TEST YAZIMI

=================================================================================
Test Temel Kurulum
Code

[T2-001] tests/__init__.py                  # Test paket tanımı
[T2-002] tests/conftest.py                  # PyTest yapılandırması
[T2-003] tests/fixtures/__init__.py         # Test fixture paket tanımı
[T2-004] tests/fixtures/kullanici_fixtures.py # Kullanıcı test verileri
[T2-005] tests/fixtures/hayvan_fixtures.py  # Hayvan test verileri
[T2-006] tests/fixtures/ilan_fixtures.py    # İlan test verileri

Unit Testler (Her Uygulama İçin)
Code

[T2-007] apps/kullanicilar/tests/__init__.py     # Kullanıcı testleri paket tanımı
[T2-008] apps/kullanicilar/tests/test_models.py  # Kullanıcı model testleri
[T2-009] apps/kullanicilar/tests/test_views.py   # Kullanıcı view testleri
[T2-010] apps/kullanicilar/tests/test_serializers.py # Kullanıcı serializer testleri

Integration ve E2E Testler
Code

[T2-011] tests/integration/__init__.py      # Entegrasyon testleri paket tanımı
[T2-012] tests/integration/test_api.py      # API entegrasyon testleri
[T2-013] tests/e2e/__init__.py              # E2E testleri paket tanımı
[T2-014] tests/e2e/test_user_journey.py     # Kullanıcı yolculuğu testleri

FAZ 21 (S1): STATİK VE MEDYA DOSYALARI

=================================================================================
Statik Dosya Yapısı
Code

[S-001] static/css/                         # CSS dosyaları dizini
[S-002] static/js/                          # JavaScript dosyaları dizini
[S-003] static/images/                      # Resim dosyaları dizini
[S-004] static/admin/                       # Django admin statik dosyaları
[S-005] staticfiles/                        # Toplanan statik dosyalar dizini

Medya ve Şablon Dosyaları
Code

[S-006] media/                              # Kullanıcı yüklenen dosyalar
[S-007] templates/base.html                 # Temel HTML şablonu
[S-008] templates/emails/                   # E-posta şablonları dizini
[S-009] templates/admin/                    # Django admin şablonları

FAZ 22 (M2): MONİTORİNG VE LOGLAMA

=================================================================================
Monitoring Yapısı
Code

[M2-001] monitoring/__init__.py             # Monitoring paket tanımı
[M2-002] monitoring/prometheus/prometheus.yml # Prometheus yapılandırması
[M2-003] monitoring/grafana/dashboards/     # Grafana dashboard'ları
[M2-004] logs/                              # Log dosyaları dizini

Dokümantasyon
Code

[M2-005] docs/README.md                     # Proje ana dokümantasyonu
[M2-006] docs/api/endpoints.md              # API endpoint dokümantasyonu
[M2-007] docs/development/setup.md          # Geliştirme ortamı kurulum kılavuzu
[M2-008] docs/deployment/production.md      # Prodüksiyon deployment kılavuzu
[M2-009] docs/models/                       # Model dokümantasyonları dizini

=================================================================================
BAĞIMLILIK HAR­İTASI:

    FAZ 1 (T1): Hiçbir bağımlılığı yok - İlk başlanmalı
    FAZ 2 (K1): T1'e bağımlı - Kullanıcı sistemi temel
    FAZ 3 (KT1): T1'e bağımlı - Kategori sistemi bağımsız
    FAZ 4 (E1): T1'e bağımlı - Etiket sistemi bağımsız
    FAZ 5 (H1): K1, KT1, E1'e bağımlı - Hayvan modeli
    FAZ 6 (I1): H1'e bağımlı - İlan sistemi (MVP Core)
    FAZ 7 (B1): I1'e bağımlı - Başvuru sistemi (MVP Complete)
    FAZ 8-11 (F1-F4): B1 tamamlandıktan sonra - Frontend MVP
    FAZ 12 (BL1): K1'e bağımlı - Bildirim sistemi
    FAZ 13 (M1): BL1'e bağımlı - Mesajlaşma sistemi
    FAZ 14 (FV1): K1, I1'e bağımlı - Favoriler sistemi
    FAZ 15 (F5): BL1, M1, FV1'e bağımlı - Frontend ikincil özellikler
    FAZ 16 (C1): Tüm backend uygulamalarına bağımlı - Celery görevleri
    FAZ 17 (BG1): K1'e bağımlı - Blog sistemi (bağımsız)
    FAZ 18 (R1): Tüm uygulamalara bağımlı - Raporlama sistemi
    FAZ 19-22: Son aşama - Prodüksiyon, test, monitoring

Bu sıralama, her fazın bir öncekine bağımlı olduğu optimal bir geliştirme akışı sağlar ve MVP'yi mümkün olan en erken aşamada tamamlar.