# 📚 ProjeBellek Sistemi

ProjeBellek, Evcil Hayvan Platformu projesi için geliştirilen bir bilgi yönetim sistemidir. Bu sistem, proje ile ilgili önemli kararları, standartları, kuralları ve yapılandırma bilgilerini saklayarak proje hafızasını korur ve geliştiricilerin bu bilgilere kolayca erişmesini sağlar.

## 🎯 Amaç ve Faydalar

ProjeBellek sistemi şu amaçları gerçekleştirmek için tasarlanmıştır:

- 📋 Proje süresince alınan kararları belgelemek ve takip etmek
- 📏 Kodlama standartlarını ve en iyi pratikleri belirlemek
- 🔄 Geçici kararların ve istisnaların sürelerini izlemek
- 🧠 Ekip üyelerine tutarlı ve ortak bir bilgi tabanı sağlamak
- 🤖 GitHub Copilot ile entegrasyon sayesinde akıllı kod önerileri sunmak

## 📂 Sistem Yapısı

ProjeBellek sistemi aşağıdaki bileşenlerden oluşur:

- **`/home/akn/Genel/pet/.github/projebellek`**: Ana ProjeBellek dizini
  - **`index.json`**: Tüm kayıtların merkezi indeks dosyası (en güncel versiyonlar dahil)
  - **`entries/`**: Her bir kaydın ayrı JSON dosyası olarak saklandığı klasör (genellikle v1 kayıtları)
  - **`corrected_index.json`**: `index.json` ile aynı içeriğe sahip kopya dosya (yedekleme amaçlı)

## 🆔 Kayıt Formatı

Her ProjeBellek kaydı aşağıdaki formattadır:

```json
{
  "id": "pb_sta_v1_20250604_213830",
  "title": "Django Model Kodlama Standartları",
  "content": "1. Model kuralları: ...",
  "tags": ["django", "model", "standart", "kodlama"],
  "type": "standart", 
  "status": "aktif",
  "created_at": "2025-06-04T21:38:30+03:00",
  "updated_at": "2025-06-04T21:38:30+03:00",
  "author": "akn",
  "version": 1,
  "related_records": [],
  "scope": "HayvanModeli", 
  "expires_at": null
}
```

### 📌 ID Formatı

Kayıt ID'leri şu formattadır: `pb_<tipKısaltması>_v<versiyon>_<tarihSaat>`

- **Tip Kısaltmaları**: 
  - `sta`: standart
  - `kar`: karar
  - `kon`: konfigürasyon
  - `ref`: referans
  - `dok`: dokümantasyon
  - `kur`: iş-kuralı
- **Versiyon**: v1, v2, v3...
- **TarihSaat**: YYYYMMdd_HHmmss formatında

## 🛠️ Kullanım

ProjeBellek sistemi, `/scripts/projebellek.sh` scripti aracılığıyla yönetilir.

### Yeni Kayıt Ekleme

```bash
pb_main pb-add "<başlık>" "<içerik>" "<etiketler>" [<tür>] [<durum>]
```

Örnek:
```bash
pb_main pb-add "User Modeli Email Standardı" "Email doğrulama için şu kontroller eklenmelidir: 1) Format doğrulama..." "kullanicilar,model,güvenlik" "standart" "aktif"
```

### Kayıt Sorgulama

```bash
# Genel sorgu
pb_main pb-query "<sorgu>"

# ID ile sorgu
pb_main pb-query "id:<kayitId>"

# Etiket ile sorgu
pb_main pb-query "etiket:<etiketAdı>"
```

## 📝 Versiyon Yönetimi

ProjeBellek sistemi kayıtların birden fazla versiyonunu destekler:

1. Yeni bir kayıt oluşturulduğunda:
   - `entries/` klasöründe `pb_<tip>_v1_<tarihSaat>.json` adıyla bir dosya oluşturulur.
   - `index.json` dosyasına kayıt eklenir.

2. Mevcut bir kayıt güncellendiğinde:
   - Yeni bir versiyon (örn. v2) `index.json` dosyasında oluşturulur.
   - Yeni kayıt, önceki kayda `related_records` alanı ile referans verir.
   - Orijinal v1 kayıtları `entries/` klasöründe korunur.

## 🔄 İndeks ve Entries İlişkisi

- `index.json`: En güncel versiyonları dahil tüm kayıtları içerir.
- `entries/`: Çoğunlukla orijinal v1 kayıtlarını saklar.
- `corrected_index.json`: `index.json` ile aynı içeriğe sahiptir, yedekleme veya geçici düzeltme amaçlı kullanılmış olabilir.

## 🚀 Gelecek İyileştirmeler

1. `entries/` klasöründe tüm versiyonları (v1, v2, v3...) saklayarak daha net bir versiyon geçmişi oluşturulabilir.
2. İndeks dosyasını sadeleştirmek için yalnızca en güncel versiyonları içerecek şekilde düzenlenebilir.
3. `corrected_index.json` dosyası artık gerekli değilse kaldırılabilir.
4. Versiyon güncelleme işlemleri için daha kapsamlı komutlar eklenebilir.

## 🏷️ Etiket Kategorileri

1. **Tema Etiketleri**: django, api, model, frontend, mimari, güvenlik, performans, test, deployment
2. **Tip Etiketleri**: standart, karar, konfigürasyon, dokümantasyon, iş-kuralı, referans 
3. **Durum Etiketleri**: aktif, gecici, kritik, önemli, tamamlandı, iptal

## 📊 Durum Tanımları

- **aktif**: Geçerli ve uygulanması gereken
- **gecici**: Belirli bir süre için geçerli
- **iptal**: Artık kullanılmayan
- **tamamlandı**: Tamamlanmış görev/karar
- **kritik**: Yüksek öncelikli, acil dikkat gerektiren
- **önemli**: Dikkatlice değerlendirilmesi gereken

## 🤖 GitHub Copilot İle Entegrasyon

ProjeBellek sistemi, GitHub Copilot ile entegre çalışarak akıllı kod önerileri sağlar. Copilot, proje kararlarını ve standartları dikkate alarak önerilerini şekillendirir.

### Copilot'un ProjeBellek'i Sorgulaması

```
@ProjeBellek hayvan modeli alanları
@ProjeBellek etiket:api durum:aktif
@ProjeBellek id:pb_kar_v2_20250615_123045
```

### Kod İçinde ProjeBellek Referansları

```python
# @PB-REF: pb_kar_v2_20250612_152030 - Hayvan Detay API Cache Stratejisi
@method_decorator(cache_page(60 * 30))
def get_object(self, pk):
    # ... Method implementation ...
```

## 📋 Örnek Kullanım Senaryoları

```bash
# Model standardı kaydetme
pb_main pb-add "User Modeli Email Doğrulama Standardı" "Email doğrulama için şu kontroller eklenmelidir: 1) Format doğrulama, 2) MX kaydı kontrolü, 3) Temp-mail engelleme" "kullanicilar,model,güvenlik,email,standart" "standart" "aktif"

# Geçici kararlar
pb_main pb-add "Sprint 9 GEÇİCİ Auth Bypass" "Geliştirme hızını artırmak için Sprint 9 boyunca /api/v2/test/* endpoint'lerinde auth devre dışı bırakıldı" "api,güvenlik,auth,sprint9" "karar" "gecici" --expires="2025-07-15"

# İlişkili kayıtlar sorgulama
pb_main pb-query "etiket:performans,etiket:cache"
```
