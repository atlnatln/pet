# Romanımızın Yeni Bölümü: "Etiket Uygulaması" Backend Tasarımı

**Rol:** Sen, usta bir prompt mühendisi ve sözcüklerle dünyalar inşa eden bir eğitmensin. Şu anki görevin, Django/React tabanlı hayvan sahiplenme projemizin backend'ine eklenecek "Etiket Uygulaması"nın detaylı bir planını, sanki bir romanın yeni bölümünü yazıyormuşçasına, kelimelerle ve kavramlarla oluşturmak. Kod yazmayacaksın; bunun yerine, her bir adımı ve bileşeni en ince ayrıntısına kadar betimleyen, yol gösterici ve kesin ifadeler kullanacaksın.

**Amaç:** "Etiket Uygulaması"nın backend tarafını, Django ve Django Rest Framework kullanarak, hiçbir belirsizliğe yer bırakmayacak şekilde tasarlamak ve bu tasarımı adım adım kelimelerle belgelemek.

---

## Giriş: Etiketlerin Romanımızdaki Rolü ve Önemi

**Prompt 1.0 (Kavramsal Çerçeve):**
"Sevgili LLM, 'Etiket Uygulaması' adını verdiğimiz bu yeni bölümün projemize katacağı değeri ve temel işlevini tanımlayarak başlayalım. Etiketler, hayvan ilanlarını hangi açılardan zenginleştirecek ve sınıflandıracak? Kullanıcıların aradıkları özelliklere sahip hayvanları bulmalarına nasıl bir kolaylık sağlayacak? Örneğin, 'oyuncu', 'çocuklarla iyi anlaşır', 'apartman yaşamına uygun', 'özel bakım gerekir', 'enerjik', 'sakin', 'hipoalerjenik' gibi etiketlerin sistemdeki rolünü, ilanlarla nasıl bir bağ kuracağını ve kullanıcı deneyimine etkilerini detaylı bir şekilde açıkla."

---

## Perde 1: Etiket Modelinin Karakter Yaratımı (Django Modeli)

**Prompt 2.1 (Temel `Etiket` Modeli Detaylandırması):**
Romanımızın bu yeni kahramanı olan `Etiket` Django modelini, sahip olacağı temel özellikler ile birlikte detaylıca tasvir et:

**Ana Karakter Özellikleri:**
- `ad`: Etiketin özünü yansıtan ismi (örn: 'Oyuncu', 'Çocuk Dostu', 'Hipoalerjenik'). Bu alan:
  * Maksimum 50 karakter uzunluğunda olmalı (kısa ve öz olması için)
  * Benzersiz (unique=True) olmalı - aynı etiket tekrar oluşturulmasın
  * Boş geçilemez (null=False, blank=False) - her etiketin bir adı olmalı
  * Büyük/küçük harf duyarsız benzersizlik için özel validasyon gerekebilir

- `slug`: URL dostu kimlik (örn: 'oyuncu', 'cocuk-dostu', 'hipoalerjenik'). Bu alan:
  * Kesinlikle benzersiz (unique=True) olmalı - URL çakışması olmasın
  * `ad` alanından otomatik türetilmeli (Django'nun `slugify` fonksiyonu ile)
  * Maksimum 60 karakter (slug'lar genelde orjinalden biraz daha uzun olabilir)
  * Model'in `save()` metodunda otomatik oluşturulmalı

- `aciklama`: Etiketin anlamını netleştiren isteğe bağlı açıklama. Bu alan:
  * Maksimum 200 karakter (kısa ama açıklayıcı)
  * Boş olabilir (blank=True, null=True)
  * Admin panelinde yardım metni olarak kullanılabilir
  * Frontend'de tooltip veya info popup'ı için kullanılabilir

- `kategori`: Etiketleri gruplandırmak için kategori sistemi. Bu alan:
  * `EtiketKategori` modeline ForeignKey
  * Boş olabilir (null=True, blank=True) - kategorisiz etiketlere izin ver
  * Silme koruması (on_delete=models.PROTECT) - kategori silindiğinde etiketler korunmalı

- `renk_kodu`: Etiketin görsel temsili için HEX renk kodu. Bu alan:
  * Maksimum 7 karakter (#ffffff formatı)
  * Varsayılan değer olmalı (default='#6366f1')
  * Validasyon ile HEX formatı kontrol edilmeli

- `populer`: Sık kullanılan etiketleri işaretlemek için. Bu alan:
  * Boolean field (default=False)
  * Frontend'de öncelikli gösterim için kullanılabilir
  * Admin panelinde filtreleme imkanı sağlar

- `kullanim_sayisi`: Bu etiketi kullanan ilan sayısı. Bu alan:
  * PositiveIntegerField (negatif olamaz)
  * Otomatik hesaplanmalı (signal'lar ile)
  * Admin panelinde ve API'de istatistik için kullanılabilir

- `aktif`: Etiketin kullanılabilir durumda olup olmadığı. Bu alan:
  * Boolean field (default=True)
  * Pasif etiketler API'de gösterilmemeli
  * Soft delete mantığı için kullanılabilir

**Zaman Damgası Alanları:**
- `created_at`: İlk oluşturma zamanı (auto_now_add=True)
- `updated_at`: Son güncelleme zamanı (auto_now=True)

**Model Meta Özellikleri:**
- Sıralama: Popülerlik, kullanım sayısı ve alfabetik sıra
- İndeksleme: `aktif`, `populer`, `kategori`, `slug` alanları için
- Verbose name'ler: Türkçe admin paneli için

**Prompt 2.2 (Etiket Kategorileri: İkinci Katman Organizasyonu):**
Etiketleri gruplandırmak için `EtiketKategori` modelini tasarla:

**Kategori Karakteristikleri:**
- `ad`: Kategori adı (örn: 'Karakter Özellikleri', 'Yaşam Tarzı', 'Sağlık Durumu')
- `slug`: URL dostu kategori kimliği
- `aciklama`: Kategorinin kapsamını açıklayan metin
- `ikon_adi`: FontAwesome ikon referansı (örn: 'fa-heart', 'fa-home')
- `renk_kodu`: Kategori temsil rengi
- `sira`: Kategori görüntülenme sırası
- `aktif`: Kategori durumu

**Özel Kategori Örnekleri:**
1. **Karakter Özellikleri**: oyuncu, sakin, enerjik, uysal, meraklı
2. **Sosyal Özellikler**: çocuk_dostu, diğer_hayvanlarla_uyumlu, yalnız_yaşamayı_tercih_eder
3. **Yaşam Tarzı**: apartman_uygun, bahçe_gerekir, şehir_hayatı
4. **Sağlık ve Bakım**: kısırlaştırılmış, aşıları_tam, özel_bakım_gerekir, hipoalerjenik
5. **Eğitim Durumu**: tuvalet_eğitimi_almış, temel_komutları_biliyor, eğitime_açık

**Prompt 2.3 (İlanlar ile Etiketler Arasındaki Can Bağı):**
`İlan` ve `Etiket` modelleri arasındaki ilişkiyi tanımla:

**İlişki Türü:** ManyToManyField
- Bir ilan birden fazla etikete sahip olabilir
- Bir etiket birden fazla ilana atanabilir
- İlişki `İlan` modelinde tanımlanmalı (semantik olarak daha doğru)
- `related_name='ilanlar'` ile ters ilişki adlandırılmalı

**Through Model Potansiyeli:**
Gelecekte etiket-ilan ilişkisine ek bilgiler eklemek için:
- `IlanEtiket` intermediate modeli düşünülebilir
- Önem derecesi, ekleme tarihi gibi meta bilgiler
- Şimdilik basit ManyToMany yeterli

**API Entegrasyonu:**
- İlan serializer'ında etiketlerin nested gösterimi
- Etiket slug'ları ile filtreleme desteği
- Çoklu etiket seçimi için frontend desteği

---

## Perde 2: Etiketlerin Sahne Arkası Yönetimi (Django Admin)

**Prompt 3.1 (EtiketAdmin: Yönetim Panelinin Kalbi):**
Django admin panelinde etiket yönetimini optimize et:

**Liste Görünümü (list_display):**
- `ad`: Etiketin adı (kalın yazı ile vurgulanmış)
- `kategori`: Hangi kategoriye ait (kategori rengi ile renklendirilmiş)
- `kullanim_sayisi`: Kaç ilana atanmış (badge şeklinde)
- `populer_badge`: Popüler durumu (görsel rozet)
- `aktif_badge`: Aktif durumu (checkmark/cross)
- `created_at`: Oluşturma tarihi

**Filtreleme Seçenekleri (list_filter):**
- Kategori (RelatedOnlyFieldListFilter)
- Popüler durumu
- Aktif durumu
- Oluşturma tarihi (DateFieldListFilter)
- Kullanım sayısı aralığı (custom filter)

**Arama Kapsamı (search_fields):**
- Etiket adı (`ad`)
- Açıklama (`aciklama`)
- Kategori adı (`kategori__ad`)

**Toplu İşlemler (actions):**
- Seçili etiketleri popüler yap
- Seçili etiketleri aktif/pasif yap
- Kullanım istatistiklerini güncelle
- Kategori değiştir (custom action)

**Form Optimizasyonları:**
- Slug otomatik doldurma (`prepopulated_fields`)
- Renk seçici widget
- Kategori seçimi için optimize edilmiş dropdown
- Açıklama alanı için daha büyük textarea

**Prompt 3.2 (İlan Admin Entegrasyonu):**
Mevcut `İlanAdmin`'e etiket desteği ekle:

**İlan Liste Görünümüne Etiket Ekleme:**
- Etiket sayısı gösterimi
- En popüler 3 etiketin badge şeklinde gösterimi
- Etiketlere göre filtreleme seçeneği

**İlan Form Entegrasyonu:**
- Etiket seçimi için çoklu seçim widget'ı
- Kategori bazında etiket gruplandırması
- Autocomplete özelliği ile etiket arama
- Yeni etiket ekleme imkanı (admin yetkisi ile)

**İlan Detay Sayfasında:**
- Atanmış etiketlerin liste halinde gösterimi
- Her etiketin kategori rengi ile renklendirilmesi
- Etiket üzerine tıklayarak o etiketi kullanan diğer ilanları görme

---

## Perde 3: Etiketlerin API Senfонisi (Django Rest Framework)

**Prompt 4.1 (Temel Etiket API Endpoint'leri):**
Etiketler için RESTful API tasarımı:

**Endpoint Yapısı:**
```
GET    /api/v1/etiketler/                 # Tüm etiketleri listele
POST   /api/v1/etiketler/                 # Yeni etiket oluştur (admin)
GET    /api/v1/etiketler/{slug}/          # Etiket detayı
PUT    /api/v1/etiketler/{slug}/          # Etiket güncelle (admin)
DELETE /api/v1/etiketler/{slug}/          # Etiket sil (admin)
GET    /api/v1/etiketler/populer/         # Popüler etiketler
GET    /api/v1/etiketler/kategoriler/     # Etiket kategorileri
GET    /api/v1/etiketler/{slug}/ilanlar/  # Bu etikete sahip ilanlar
```