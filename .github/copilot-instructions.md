# Django/React Evcil Hayvan Platformu Kodlama Standartları

Bu dosya, GitHub Copilot için proje kodlama standartlarını, mimari kararlarını ve teknik çerçeveyi içerir. 
Her madde kısa, anlaşılır ve doğrudan uygulanabilir niteliktedir.

## Proje Mimarisi

- Django (Backend) ve React (Frontend) teknolojileriyle geliştirilmiş bir Evcil Hayvan Sahiplendirme platformudur
- Backend için `/apps` klasörü altında Django uygulamaları bulunur (hayvanlar, kullanicilar, ilanlar, vb.)
- Frontend için `/frontend` klasörü altında React komponentleri bulunur

## Genel Kodlama Standartları

- Tüm yeni kod PEP8 standartlarına uygun olmalıdır
- Docstring formatı için Google stilini kullanın (parametre ve dönüş değeri açıklamaları içermeli)
- Karmaşık işlemlerde hız ve performans için ölçüm, test ve optimizasyon yapılmalı
- Hiçbir şifre, API anahtarı veya hassas bilgi kodda saklanmamalı (environment variable kullanılmalı)
- Bütün modeller, view'lar ve fonksiyonlar Türkçe isimlendirilmelidir

## Django Standartları

- Tüm Django model isimleri PascalCase kullanmalıdır (örn: `HayvanModeli`)
- Her model mutlaka `base.py` içindeki abstract `BaseModel` sınıfından türetilmelidir
- `CharField` gibi alanlarda `max_length` değeri ve `verbose_name` belirtilmelidir
- Tüm modellerde `Meta` sınıfı içerisinde `verbose_name` ve `verbose_name_plural` tanımlanmalıdır
- Model validasyonu için `clean()` metodunu kullanın, form validasyonu için Custom Validator yazın
- API endpoint'leri için sürümleme `/api/v[VERSION_NO]/...` şeklinde yapılmalıdır
- Veritabanı sorguları için Django ORM kullanılmalı, ham SQL'den kaçınılmalıdır
- Her API view, appropriate HTTP status kodları döndürmeli (200, 201, 400, 401, 403, 404, 500)
- Listeleme API'larında sayfalandırma (`pagination`) kullanılmalıdır (default: sayfa başına 20 öğe)
- Model ilişkileri (ForeignKey, ManyToMany) için `on_delete` davranışı açıkça belirtilmelidir
- Yetkisiz girişlerin önlenmesi için view'larda `permission_classes` doğru şekilde tanımlanmalıdır
- Django `signals.py` dosyalarında mantıksal olarak birbiriyle doğrudan ilişkili olmayan işlemlerden kaçının

## React Standartları

- TypeScript tercih edilmelidir
- React komponent isimlendirmesinde PascalCase kullanılmalıdır (örn: `AnimalCard.tsx`)
- Props için interface tanımlamaları yapılmalıdır
- State yönetimi için Redux toolkit kullanılmalıdır
- API istekleri için Axios tercih edilmelidir
- CSS için Tailwind kullanılmalıdır
- Erişilebilirlik (accessibility) için uygun ARIA özellikleri eklenmelidir

## Test Standartları

- Backend için pytest kullanılmalıdır
- Her model için en az temel CRUD testleri yazılmalıdır
- Frontend için Jest ve React Testing Library kullanılmalıdır
- Kritik işlevler mutlaka test edilmelidir

## @ProjeBellek Komutları ve Kullanımı

@ProjeBellek, proje hafızasını yönetmek için kullanılan CLI tabanlı bir sistemdir.

### Temel Komut Yapısı

```bash
# Bilgi ekleme
pb_main pb-add "<başlık>" "<içerik>" "<etiketler>" [<tür>] [<durum>]

# Bilgi sorgulama
pb_main pb-query "<sorgu>" 
pb_main pb-query "etiket:<etiketAdı>" 
pb_main pb-query "id:<kayitId>"

# Kayıt karşılaştırma
pb_main pb-diff "id:<kayıt1>" "id:<kayıt2>"

# Kayıt geçmişi
pb_main pb-history "id:<kayıtId>"
```

### Standart Etiket Sistemi

1. **Tema Etiketleri**: django, api, model, frontend, mimari, güvenlik, performans, test, deployment
2. **Tip Etiketleri**: standart, karar, konfigürasyon, dokümantasyon, iş-kuralı, referans 
3. **Durum Etiketleri**: aktif, gecici, kritik, önemli, tamamlandı, iptal

### Gelişmiş Sorgulama Örnekleri

```bash
# Zaman bazlı sorgulama
pb_main pb-query "son:7gün"

# Çoklu etiket sorgusu
pb_main pb-query "etiket:api,etiket:performans"

# Etiket ve durum kombinasyonu
pb_main pb-query "etiket:sprint9 durum:aktif"

# İlişkili kayıtları gösterme
pb_main pb-query "id:pb_kar_v3_20250615_092015 --with-related"
```

### Örnek Kullanım Senaryoları

```bash
# Model standardı kaydetme
pb_main pb-add "User Modeli Email Doğrulama Standardı" "Email doğrulama için şu kontroller eklenmelidir: 1) Format doğrulama, 2) MX kaydı kontrolü, 3) Temp-mail engelleme" "kullanıcılar,model,güvenlik,email,standart" "standart" "aktif"

# Geçici kararlar
pb_main pb-add "Sprint 9 GEÇİCİ Auth Bypass" "Geliştirme hızını artırmak için Sprint 9 boyunca /api/v2/test/* endpoint'lerinde auth devre dışı bırakıldı" "api,güvenlik,auth,sprint9" "karar" "gecici" --expires="2025-07-15"

# İlişkili kayıtlar oluşturma
pb_main pb-add "Hayvan Detay Performans İyileştirmeleri" "Hayvan detay sayfası yüklenme süresi: 1) Eager loading, 2) N+1 sorgu çözümü, 3) Redis cache" "performans,hayvanlar,cache" "karar" "aktif" --related="pb_kar_v1_20250510_091023"
```

## Copilot ve @ProjeBellek Entegrasyonu

Copilot, proje kodlarını geliştirirken @ProjeBellek'teki dinamik bilgileri kullanmak için aşağıdaki protokolleri izlemelidir:

### Copilot'un @ProjeBellek'i Sorgulaması

```
@ProjeBellek hayvan modeli alanları
@ProjeBellek etiket:api durum:aktif
@ProjeBellek id:pb_kar_v2_20250615_123045
```

### Sorgulama Sonrası Yanıt Formatı

```
ProjeBellek'te [pb_kar_v2_20250615_123045] kaydına göre, Hayvan modeli için şu alanlar zorunludur:
- isim (CharField, max_length=100)
- tür (ForeignKey, Kategori)
- cinsiyet (CharField, choices=CINSIYET_SECENEKLERI)
- yaş (PositiveIntegerField)
- ...

Bu bilgiyi dikkate alarak modeli oluşturuyorum.
```

### Kod ve ProjeBellek Referansları

Yazılan kodlarda ProjeBellek referanslarını şu şekilde belirt:

```python
# @PB-REF: pb_kar_v2_20250612_152030 - Hayvan Detay API Cache Stratejisi
@method_decorator(cache_page(60 * 30))
def get_object(self, pk):
    # ...
```

### Copilot İçin Temel İlkeler

1. Her yeni önemli tasarım kararının @ProjeBellek'e kaydedilmesini öner
2. @ProjeBellek'te bulunan kararları kodlama önerilerinle tutarlı hale getir
3. Çelişen bilgilerde yeni tarihlileri önceliklendir
4. ProjeBellek referanslarını kullanarak kodun neden o şekilde yazıldığını açıkla
5. İş kuralı değişikliklerinde ilgili kayıtların güncellenmesini öner

## Statik Talimatlar ve Dinamik @ProjeBellek Ayrımı

Bu dosya (`copilot-instructions.md`) ve @ProjeBellek arasındaki iş bölümü:

| Alan | Bu Dosya (Statik Talimatlar) | @ProjeBellek (Dinamik Sistem) |
|------|------------------------------|------------------------------|
| İçerik | Genel kodlama standartları, mimari yapı, değişmeyen kurallar | Sprint kararları, spesifik tasarım detayları, geçici kurallar |
| Güncelleme | Nadiren (ana prensip değişimlerinde) | Sık sık (her sprint, her önemli karar) |
| Kapsam | Tüm projede geçerli ilkeler | Belirli alan, API veya görevle ilgili kurallar |
| Örnek | "Tüm modellerde created_at alanı bulunmalı" | "Sprint 9'da hayvan_detay API'sine cache eklendi" |

### @ProjeBellek Kategorizasyonu

Projede @ProjeBellek'te saklanan bilgi türleri:

1. **Standartlar**: Uzun vadeli kodlama kuralları ve prensipler
   ```
   pb_main pb-query "etiket:standart durum:aktif"
   ```

2. **Kararlar**: Tasarım ve teknik tercihler
   ```
   pb_main pb-query "etiket:karar son:30gün"
   ```

3. **Konfigürasyonlar**: Sistem ayarları, limitler, seçenekler
   ```
   pb_main pb-query "etiket:konfigürasyon"
   ```

4. **İş Kuralları**: Sisteme özel domain kuralları
   ```
   pb_main pb-query "etiket:iş-kuralı"
   ```

## @ProjeBellek Veri Yapısı

Her @ProjeBellek kaydı aşağıdaki yapıdadır:

```json
{
  "id": "pb_sta_v1_20250604_213830",
  "title": "Django Model Kodlama Standartları",
  "content": "1. Model kuralları:\n- Meta sınıfı içermeli...",
  "tags": ["django", "model", "standart", "kodlama"],
  "type": "standart", 
  "status": "aktif",
  "created_at": "2025-06-04T21:38:30+03:00",
  "updated_at": "2025-06-04T21:38:30+03:00",
  "author": "akn",
  "version": 1,
  "related_records": ["pb_kar_v1_20250510_091023"],
  "scope": "HayvanModeli", 
  "expires_at": null
}
```

### ID Formatı ve Kullanımı

Format: `pb_<tipKısaltması>_v<versiyon>_<tarihSaat>`

- **Tip Kısaltmaları**: 
  - `sta`: standart
  - `kar`: karar
  - `kon`: konfigürasyon 
  - `ref`: referans
  - `dok`: dokümantasyon
  - `kur`: iş-kuralı

- **Versiyon**: Kaydın versiyon numarası (v1, v2, v3...)
- **TarihSaat**: Oluşturma tarihi (YYYYMMdd_HHmmss)

### Durum Tanımları

- **aktif**: Geçerli ve uygulanması gereken
- **gecici**: Belirli bir süre için geçerli
- **iptal**: Artık kullanılmayan
- **tamamlandı**: Tamamlanmış görev/karar
- **kritik**: Yüksek öncelikli, acil dikkat gerektiren
- **önemli**: Dikkatlice değerlendirilmesi gereken