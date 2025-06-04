# Proje Değişkenleri ve Açıklamaları

Bu doküman, Pet uygulamasında kullanılan önemli değişkenleri, sabitleri ve model alanlarını içerir. Yeni uygulama geliştirirken veya mevcut kodu anlamak için referans olarak kullanılabilir.

## 1. apps.ortak

### constants.py

#### Hayvan Türleri
- `KEDI` (apps/ortak/constants.py): Kedi türü için sabit değer
- `KOPEK` (apps/ortak/constants.py): Köpek türü için sabit değer
- `KUS` (apps/ortak/constants.py): Kuş türü için sabit değer
- `BALIK` (apps/ortak/constants.py): Balık türü için sabit değer
- `KEMIRGEN` (apps/ortak/constants.py): Kemirgen türü için sabit değer
- `SURUNGEN` (apps/ortak/constants.py): Sürüngen türü için sabit değer
- `DIGER` (apps/ortak/constants.py): Diğer hayvan türleri için sabit değer

#### Boyut Sabitleri
- `EXTRA_SMALL` (apps/ortak/constants.py): Çok küçük boyut
- `SMALL` (apps/ortak/constants.py): Küçük boyut
- `MEDIUM` (apps/ortak/constants.py): Orta boyut
- `LARGE` (apps/ortak/constants.py): Büyük boyut
- `EXTRA_LARGE` (apps/ortak/constants.py): Çok büyük boyut
- `CHOICES` (apps/ortak/constants.py): Boyut seçenekleri listesi

#### Yaş Grupları
- `BABY` (apps/ortak/constants.py): Yavru/bebek hayvan
- `YOUNG` (apps/ortak/constants.py): Genç hayvan
- `ADULT` (apps/ortak/constants.py): Yetişkin hayvan
- `SENIOR` (apps/ortak/constants.py): Yaşlı hayvan
- `CHOICES` (apps/ortak/constants.py): Yaş grubu seçenekleri listesi

#### Cinsiyet Sabitleri
- `MALE` (apps/ortak/constants.py): Erkek
- `FEMALE` (apps/ortak/constants.py): Dişi
- `UNKNOWN` (apps/ortak/constants.py): Bilinmeyen
- `CHOICES` (apps/ortak/constants.py): Cinsiyet seçenekleri listesi

#### İlan Durumları
- `DRAFT` (apps/ortak/constants.py): Taslak
- `ACTIVE` (apps/ortak/constants.py): Aktif
- `ADOPTED` (apps/ortak/constants.py): Sahiplendirilmiş
- `INACTIVE` (apps/ortak/constants.py): Pasif
- `EXPIRED` (apps/ortak/constants.py): Süresi dolmuş
- `CHOICES` (apps/ortak/constants.py): İlan durumu seçenekleri listesi

#### Başvuru Durumları
- `PENDING` (apps/ortak/constants.py): Beklemede
- `UNDER_REVIEW` (apps/ortak/constants.py): İnceleniyor
- `APPROVED` (apps/ortak/constants.py): Onaylandı
- `REJECTED` (apps/ortak/constants.py): Reddedildi
- `WITHDRAWN` (apps/ortak/constants.py): Geri çekildi
- `CHOICES` (apps/ortak/constants.py): Başvuru durumu seçenekleri listesi

#### Sahiplenme Türleri
- `ADOPTION` (apps/ortak/constants.py): Kalıcı sahiplenme
- `FOSTERING` (apps/ortak/constants.py): Geçici yuva
- `TEMPORARY_CARE` (apps/ortak/constants.py): Geçici bakım
- `CHOICES` (apps/ortak/constants.py): Sahiplenme türü seçenekleri listesi

#### Kullanıcı Rolleri
- `USER` (apps/ortak/constants.py): Normal kullanıcı
- `SHELTER_STAFF` (apps/ortak/constants.py): Barınak görevlisi
- `VETERINARY` (apps/ortak/constants.py): Veteriner
- `VOLUNTEER` (apps/ortak/constants.py): Gönüllü
- `MODERATOR` (apps/ortak/constants.py): Moderatör
- `ADMIN` (apps/ortak/constants.py): Yönetici
- `CHOICES` (apps/ortak/constants.py): Kullanıcı rolü seçenekleri listesi

#### Kullanıcı Durumları
- `ACTIVE` (apps/ortak/constants.py): Aktif
- `INACTIVE` (apps/ortak/constants.py): Pasif
- `SUSPENDED` (apps/ortak/constants.py): Askıya alınmış
- `BANNED` (apps/ortak/constants.py): Yasaklanmış
- `CHOICES` (apps/ortak/constants.py): Kullanıcı durumu seçenekleri listesi

#### Bildirim Türleri
- `APPLICATION_RECEIVED` (apps/ortak/constants.py): Başvuru alındı
- `APPLICATION_APPROVED` (apps/ortak/constants.py): Başvuru onaylandı
- `APPLICATION_REJECTED` (apps/ortak/constants.py): Başvuru reddedildi
- `NEW_MESSAGE` (apps/ortak/constants.py): Yeni mesaj
- `LISTING_EXPIRED` (apps/ortak/constants.py): İlan süresi doldu
- `SYSTEM_ANNOUNCEMENT` (apps/ortak/constants.py): Sistem duyurusu
- `CHOICES` (apps/ortak/constants.py): Bildirim türü seçenekleri listesi

#### Öncelik Seviyeleri
- `LOW` (apps/ortak/constants.py): Düşük
- `NORMAL` (apps/ortak/constants.py): Normal
- `HIGH` (apps/ortak/constants.py): Yüksek
- `URGENT` (apps/ortak/constants.py): Acil
- `CHOICES` (apps/ortak/constants.py): Öncelik seviyesi seçenekleri listesi

#### Dosya Türleri
- `PROFILE_IMAGE` (apps/ortak/constants.py): Profil resmi
- `PET_IMAGE` (apps/ortak/constants.py): Hayvan resmi
- `DOCUMENT` (apps/ortak/constants.py): Belge
- `DEFAULT` (apps/ortak/constants.py): Varsayılan

#### Boyut Limitleri
- `SMALL` (apps/ortak/constants.py): Küçük boyut limiti
- `LARGE` (apps/ortak/constants.py): Büyük boyut limiti
- `MAX` (apps/ortak/constants.py): Maksimum boyut limiti

#### Rate Limitleri
- `LOGIN_ATTEMPTS` (apps/ortak/constants.py): Maksimum giriş denemesi
- `MESSAGE_PER_HOUR` (apps/ortak/constants.py): Saatlik mesaj gönderme limiti
- `APPLICATION_PER_DAY` (apps/ortak/constants.py): Günlük başvuru limiti
- `LISTING_PER_DAY` (apps/ortak/constants.py): Günlük ilan oluşturma limiti

#### Listeler ve Sabitler
- `TURKISH_CITIES` (apps/ortak/constants.py): Türkiye şehir listesi
- `LANGUAGE_CODES` (apps/ortak/constants.py): Dil kodları listesi
- `POPULER_IRKLAR` (apps/ortak/constants.py): Popüler köpek ırkları listesi
- `YERLI_IRKLAR` (apps/ortak/constants.py): Yerli köpek ırkları listesi
- `ADANA`, `ADIYAMAN`, `ISTANBUL`, `IZMIR` (apps/ortak/constants.py): Şehir sabitleri

### validators.py
- `FORBIDDEN_WORDS` (apps/ortak/validators.py): Yasaklı kelimeler listesi
- `TURKISH_CITIES` (apps/ortak/validators.py): Türkiye şehirleri listesi (doğrulama için)

### models.py
#### Tarih Alanları
- `created_at` (apps/ortak/models.py): Oluşturulma tarihi
- `updated_at` (apps/ortak/models.py): Güncellenme tarihi
- `published_at` (apps/ortak/models.py): Yayınlanma tarihi
- `deleted_at` (apps/ortak/models.py): Silinme tarihi

#### Base Model Alanları
- `id` (apps/ortak/models.py): Birincil anahtar
- `title` (apps/ortak/models.py): Başlık
- `slug` (apps/ortak/models.py): SEO dostu URL
- `status` (apps/ortak/models.py): Durum

#### İçerik Durumları
- `DRAFT` (apps/ortak/models.py): Taslak
- `REVIEW` (apps/ortak/models.py): İncelemede
- `PUBLISHED` (apps/ortak/models.py): Yayınlanmış
- `REJECTED` (apps/ortak/models.py): Reddedilmiş
- `ARCHIVED` (apps/ortak/models.py): Arşivlenmiş

#### Analytics Alanları
- `search_vector` (apps/ortak/models.py): Arama vektörü
- `view_count` (apps/ortak/models.py): Görüntülenme sayısı
- `like_count` (apps/ortak/models.py): Beğeni sayısı
- `share_count` (apps/ortak/models.py): Paylaşım sayısı

## 2. apps.kullanicilar

### validators.py
- `TURKISH_PHONE_REGEX` (apps/kullanicilar/validators.py): Türkiye telefon formatı için regex
- `NAME_REGEX` (apps/kullanicilar/validators.py): Ad/soyad doğrulaması için regex
- `INSTAGRAM_REGEX` (apps/kullanicilar/validators.py): Instagram kullanıcı adı doğrulaması için regex

### models.py
#### Kullanıcı Bilgileri
- `email` (apps/kullanicilar/models.py): E-posta adresi
- `first_name` (apps/kullanicilar/models.py): Ad
- `last_name` (apps/kullanicilar/models.py): Soyad
- `telefon` (apps/kullanicilar/models.py): Telefon numarası
- `sehir` (apps/kullanicilar/models.py): Şehir
- `biyografi` (apps/kullanicilar/models.py): Kullanıcı hakkında bilgi
- `profil_resmi` (apps/kullanicilar/models.py): Profil resmi
- `rol` (apps/kullanicilar/models.py): Kullanıcı rolü
- `durum` (apps/kullanicilar/models.py): Kullanıcı durumu

#### Doğrulama Bilgileri
- `email_dogrulanmis` (apps/kullanicilar/models.py): E-posta doğrulanmış mı
- `email_dogrulama_token` (apps/kullanicilar/models.py): E-posta doğrulama jetonu
- `email_dogrulama_tarihi` (apps/kullanicilar/models.py): E-posta doğrulama tarihi
- `kimlik_dogrulandi_mi` (apps/kullanicilar/models.py): Kimlik doğrulanmış mı

#### Tercihler
- `sahiplendiren_mi` (apps/kullanicilar/models.py): Hayvan sahiplendiriyor mu
- `sahiplenmek_istiyor_mu` (apps/kullanicilar/models.py): Hayvan sahiplenmek istiyor mu
- `email_bildirimleri` (apps/kullanicilar/models.py): E-posta bildirimleri açık mı
- `push_bildirimleri` (apps/kullanicilar/models.py): Push bildirimleri açık mı

#### İstatistikler
- `son_giris_tarihi` (apps/kullanicilar/models.py): Son giriş tarihi
- `giris_sayisi` (apps/kullanicilar/models.py): Giriş sayısı
- `uyelik_tarihi` (apps/kullanicilar/models.py): Üyelik tarihi
- `guncelleme_tarihi` (apps/kullanicilar/models.py): Güncelleme tarihi

#### Auth
- `USERNAME_FIELD` (apps/kullanicilar/models.py): Kullanıcı adı alanı
- `REQUIRED_FIELDS` (apps/kullanicilar/models.py): Zorunlu alanlar

#### Sahiplendirme Profili
- `kullanici` (apps/kullanicilar/models.py): İlişkili kullanıcı
- `instagram_hesabi` (apps/kullanicilar/models.py): Instagram hesabı
- `facebook_hesabi` (apps/kullanicilar/models.py): Facebook hesabı
- `hayvan_deneyimi_yil` (apps/kullanicilar/models.py): Hayvan deneyimi (yıl)
- `daha_once_sahiplendin_mi` (apps/kullanicilar/models.py): Daha önce hayvan sahiplenmiş mi
- `veteriner_referansi` (apps/kullanicilar/models.py): Veteriner referansı
- `ev_tipi` (apps/kullanicilar/models.py): Ev tipi
- `bahce_var_mi` (apps/kullanicilar/models.py): Bahçe var mı
- `diger_hayvanlar` (apps/kullanicilar/models.py): Diğer hayvanlar

## 3. apps.kategoriler

### models.py
#### Kategori Modeli Alanları
- `ad` (apps/kategoriler/models.py): Kategori adı
- `slug` (apps/kategoriler/models.py): SEO dostu URL
- `aciklama` (apps/kategoriler/models.py): Kategori açıklaması
- `pet_type` (apps/kategoriler/models.py): Hayvan türü
- `ikon_adi` (apps/kategoriler/models.py): İkon adı
- `renk_kodu` (apps/kategoriler/models.py): Renk kodu
- `kullanim_sayisi` (apps/kategoriler/models.py): Kullanım sayısı
- `aktif` (apps/kategoriler/models.py): Aktif mi
- `sira` (apps/kategoriler/models.py): Sıralama

#### Form Alanı Modeli
- `ad` (apps/kategoriler/models.py): Alan adı
- `alan_tipi` (apps/kategoriler/models.py): Alan tipi
- `secenekler` (apps/kategoriler/models.py): Alan seçenekleri
- `zorunlu` (apps/kategoriler/models.py): Zorunlu mu
- `aktif` (apps/kategoriler/models.py): Aktif mi
- `sira` (apps/kategoriler/models.py): Sıralama

#### Sabitler
- `KATEGORI_HIKAYELERI` (apps/kategoriler/models.py): Kategori hikayeleri

## 4. apps.hayvanlar

### models.py
#### Irk Modeli Alanları
- `id` (apps/hayvanlar/models.py): Birincil anahtar
- `ad` (apps/hayvanlar/models.py): Irk adı
- `aciklama` (apps/hayvanlar/models.py): Irk açıklaması
- `populer` (apps/hayvanlar/models.py): Popüler mi
- `yerli` (apps/hayvanlar/models.py): Yerli mi
- `aktif` (apps/hayvanlar/models.py): Aktif mi
- `fotograf` (apps/hayvanlar/models.py): Fotoğraf
- `thumbnail` (apps/hayvanlar/models.py): Küçük resim
- `kapak_fotografi` (apps/hayvanlar/models.py): Kapak fotoğrafı
- `sira` (apps/hayvanlar/models.py): Sıralama
- `created_at` (apps/hayvanlar/models.py): Oluşturulma tarihi
- `updated_at` (apps/hayvanlar/models.py): Güncellenme tarihi

#### Hayvan Modeli Alanları
- `ad` (apps/hayvanlar/models.py): Hayvan adı
- `slug` (apps/hayvanlar/models.py): SEO dostu URL
- `tur` (apps/hayvanlar/models.py): Hayvan türü
- `yas` (apps/hayvanlar/models.py): Yaş
- `cinsiyet` (apps/hayvanlar/models.py): Cinsiyet
- `boyut` (apps/hayvanlar/models.py): Boyut
- `renk` (apps/hayvanlar/models.py): Renk
- `kisirlastirilmis` (apps/hayvanlar/models.py): Kısırlaştırılmış mı
- `asilar_tamam` (apps/hayvanlar/models.py): Aşıları tamamlanmış mı
- `mikrocipli` (apps/hayvanlar/models.py): Mikroçip takılı mı
- `karakter_ozellikleri` (apps/hayvanlar/models.py): Karakter özellikleri
- `aciklama` (apps/hayvanlar/models.py): Hayvan açıklaması
- `il` (apps/hayvanlar/models.py): İl
- `ilce` (apps/hayvanlar/models.py): İlçe
- `aktif` (apps/hayvanlar/models.py): Aktif mi
- `sahiplenildi` (apps/hayvanlar/models.py): Sahiplenildi mi
- `created_at` (apps/hayvanlar/models.py): Oluşturulma tarihi
- `updated_at` (apps/hayvanlar/models.py): Güncellenme tarihi