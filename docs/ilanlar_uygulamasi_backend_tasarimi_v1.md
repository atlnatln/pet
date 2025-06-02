# Romanımızın Ana Bölümü: "İlanlar Uygulaması" Backend Tasarımı

## Önsöz: Etiketlerle Bütünleşik İlan Sistemimiz

**Prompt 1.0 (Kavramsal Çerçeve):**
"Sevgili LLM, 'İlanlar Uygulaması' adını verdiğimiz bu bölüm, projemizin kalbini oluşturacak. Bu romanda, hayvan sahiplendirme platformumuzun can damarı olan ilan sisteminin nasıl tasarlanacağını, önceki bölümde oluşturduğumuz 'Etiket Uygulaması' ile nasıl kusursuz bir şekilde entegre edileceğini, en ince ayrıntısına kadar tasvir et. İlan sistemimiz hangi temel bileşenlerden oluşacak? Kullanıcıların sahiplendirmek istediği hayvanların özelliklerini, fotoğraflarını, hikayelerini nasıl paylaşabilecekleri? İlanların durumlarının (aktif, sahiplendirildi, süre doldu vb.) nasıl yönetileceği? Arama, filtreleme ve özellikle etiket tabanlı sınıflandırmanın nasıl gerçekleştirileceği konularında rehberlik et. Bu sistemin, hayvanların doğru evlere ulaşmasını nasıl kolaylaştıracağını ve kullanıcı deneyimini nasıl zenginleştireceğini açıkla."

---

## Bölüm 1: İlan Modelinin Anatomisi (Django Modeli)

**Prompt 2.1 (Temel `HayvanIlani` Modeli ve Alanları):**
"Şimdi, romanımızın ana karakteri olan `HayvanIlani` (AnimalListing) Django modelini en ince ayrıntısına kadar tasvir et. Bu model aşağıdaki temel kategorilerde özelliklere (alanlara) sahip olmalı:

### 1. Kimlik ve Temel Bilgiler:
* `id`: Otomatik artan birincil anahtar (AutoField/BigAutoField).
* `baslik`: İlanın başlığı. CharField, maximum 100 karakter, boş olamaz.
* `slug`: SEO dostu URL oluşturmak için. SlugField, unique=True, baslik'tan otomatik oluşturulmalı.
* `ilan_tarihi`: İlanın ilk yayınlandığı tarih. DateTimeField, auto_now_add=True.
* `guncellenme_tarihi`: İlanın son güncellendiği tarih. DateTimeField, auto_now=True.
* `durum`: İlanın mevcut durumu. CharField, choices parametresi ile ('aktif', 'sahiplendirildi', 'beklemede', 'süresi_doldu', vb.) ve bunların görünen isimleri tanımlanmalı. Default='aktif'.

### 2. Hayvanın Fiziksel ve Karakteristik Özellikleri:
* `hayvan_turu`: Hayvanın türü (kedi, köpek, kuş, vb.). ForeignKey ile HayvanTuru modeline bağlanmalı.
* `cins`: Hayvanın cinsi (tekir, golden retriever, vb.). ForeignKey ile Cins modeline bağlanmalı, hayvan_turu ile ilişkili olarak filtrelenebilmeli.
* `isim`: Hayvanın adı. CharField, maksimum 50 karakter, null=True, blank=True (opsiyonel olabilir).
* `yas_yil`: Yıl olarak yaş. PositiveSmallIntegerField, null=True, blank=True.
* `yas_ay`: Ay olarak yaş. PositiveSmallIntegerField, null=True, blank=True.
* `cinsiyet`: CharField, choices parametresi ile ('erkek', 'disi', 'bilinmiyor').
* `boyut`: CharField, choices parametresi ile ('kucuk', 'orta', 'buyuk', 'cok_buyuk').
* `renk`: CharField, maksimum 50 karakter.
* `agirlik`: DecimalField, null=True, blank=True, max_digits=5, decimal_places=2 (kg cinsinden).

### 3. Sağlık Durumu:
* `asilar`: Hayvanın aşıları hakkında bilgi. TextField, blank=True.
* `kisirlastirilmis`: BooleanField, default=False.
* `saglik_durumu`: TextField, hayvanın genel sağlık durumu, bilinen rahatsızlıkları, vb.
* `ozel_ihtiyaclar`: TextField, blank=True, varsa özel bakım gereksinimleri.

### 4. Davranışsal Özellikler ve Uyumluluk:
* `karakter_ozellikleri`: TextField, hayvanın davranışsal özellikleri (sakin, oyuncu, vb.).
* `cocuklarla_uyumlu`: BooleanField, null=True, blank=True.
* `diger_hayvanlarla_uyumlu`: BooleanField, null=True, blank=True.
* `ev_ortamina_uyumlu`: BooleanField, null=True, blank=True.

### 5. Konum Bilgileri:
* `sehir`: CharField, maksimum 50 karakter, hayvanın bulunduğu şehir.
* `ilce`: CharField, maksimum 50 karakter, hayvanın bulunduğu ilçe.
* `adres`: TextField, blank=True, daha detaylı adres bilgisi (isteğe bağlı).
* `enlem`: DecimalField, null=True, blank=True, harita için.
* `boylam`: DecimalField, null=True, blank=True, harita için.

### 6. İletişim ve Sahiplik Bilgileri:
* `ilan_sahibi`: ForeignKey ile Django'nun User modeline bağlantı, on_delete=models.CASCADE.
* `iletisim_tercihi`: CharField, choices parametresi ile ('telefon', 'email', 'her_ikisi').
* `telefon`: CharField, maksimum 20 karakter, null=True, blank=True.
* `gizli_adres`: BooleanField, default=True, adresin diğer kullanıcılara gösterilip gösterilmeyeceği.

### 7. Detaylı İçerik:
* `aciklama`: TextField, hayvan hakkında detaylı bilgi, hikayesi, alışkanlıkları.
* `sahiplendirme_sartlari`: TextField, blank=True, sahiplendirme için özel şartlar varsa.

### 8. İstatistikler ve Ölçümler:
* `goruntulenme_sayisi`: PositiveIntegerField, default=0, ilanın kaç kez görüntülendiğini takip etmek için.
* `favori_sayisi`: PositiveIntegerField, default=0, kaç kullanıcının bu ilanı favorilere eklediği.

### 9. İlişkiler:
* `tags`: ManyToManyField ile Tag modeline bağlantı, blank=True, önceki bölümde tasarladığımız etiket sistemi ile entegrasyon.

Her bir alanın veri tipi, kısıtlamaları, varsayılan değerleri ve ilişkilerini ayrıntılı bir şekilde tanımla. Ayrıca, modelin Meta sınıfındaki ordering, verbose_name gibi ayarlar ile __str__ metodunu da belirt."

**Prompt 2.2 (İlanlar için Yardımcı Modeller):**
"İlanlarımızı zenginleştirmek için gerekli yardımcı modelleri detaylı bir şekilde tanımla. Bu modeller, ana `HayvanIlani` modelimize bağlanarak sistemin daha organize ve işlevsel olmasını sağlayacak:

### 1. `HayvanTuru` (AnimalType) Modeli:
* `id`: Otomatik artan birincil anahtar.
* `ad`: Türün adı (kedi, köpek, kuş, vb.). CharField, maksimum 50 karakter, unique=True.
* `icon`: İsteğe bağlı bir ikon/simge için. CharField, maksimum 50 karakter, blank=True.
* `slug`: URL için. SlugField, unique=True.

### 2. `Cins` (Breed) Modeli:
* `id`: Otomatik artan birincil anahtar.
* `hayvan_turu`: ForeignKey ile HayvanTuru modeline bağlantı. on_delete=models.CASCADE.
* `ad`: Cinsin adı (Tekir, Golden Retriever, vb.). CharField, maksimum 100 karakter.
* `aciklama`: Cins hakkında kısa bilgi. TextField, blank=True.
* `slug`: URL için. SlugField.

**Meta sınıfında:**
* `unique_together = ('hayvan_turu', 'ad')` - Bir hayvan türü altında aynı isimde iki cins olamaz.
* `ordering = ('hayvan_turu', 'ad')` - Önce tür sonra ada göre sırala.

### 3. `HayvanFotografi` (AnimalPhoto) Modeli:
* `id`: Otomatik artan birincil anahtar.
* `ilan`: ForeignKey ile HayvanIlani modeline bağlantı. on_delete=models.CASCADE.
* `fotograf`: ImageField, fotoğraf dosyasını saklamak için.
* `baslik`: Fotoğrafın başlığı/açıklaması. CharField, maksimum 100 karakter, blank=True.
* `yukleme_tarihi`: DateTimeField, auto_now_add=True.
* `siralama`: PositiveSmallIntegerField, default=0, fotoğrafların gösterim sırasını ayarlamak için.
* `ana_fotograf`: BooleanField, default=False, ilanın ana fotoğrafı olup olmadığını belirtmek için.

### 4. `Basvuru` (Application) Modeli:
* `id`: Otomatik artan birincil anahtar.
* `ilan`: ForeignKey ile HayvanIlani modeline bağlantı. on_delete=models.CASCADE.
* `basvuran`: ForeignKey ile User modeline bağlantı. on_delete=models.CASCADE.
* `basvuru_tarihi`: DateTimeField, auto_now_add=True.
* `mesaj`: TextField, başvuranın iletmek istediği mesaj.
* `durum`: CharField, choices parametresi ile ('beklemede', 'onaylandi', 'reddedildi'). default='beklemede'.
* `islem_tarihi`: DateTimeField, null=True, blank=True, başvurunun onaylandığı/reddedildiği tarih.
* `islem_notu`: TextField, blank=True, ilan sahibinin başvuru hakkındaki notu.

### 5. `Favori` (Favorite) Modeli:
* `id`: Otomatik artan birincil anahtar.
* `ilan`: ForeignKey ile HayvanIlani modeline bağlantı. on_delete=models.CASCADE.
* `kullanici`: ForeignKey ile User modeline bağlantı. on_delete=models.CASCADE.
* `ekleme_tarihi`: DateTimeField, auto_now_add=True.

**Meta sınıfında:**
* `unique_together = ('ilan', 'kullanici')` - Bir kullanıcı bir ilanı sadece bir kez favorilere ekleyebilir.

Bu yardımcı modellerin her biri için önemli metodları (örneğin, `__str__` metodunu) ve Meta sınıfı ayarlarını (örn. verbose_name, verbose_name_plural) tanımla. Ayrıca, bazı modellere özel metodlar (örneğin, HayvanFotografi modeli için 'ana fotoğraf yoksa ilk fotoğrafı ana fotoğraf olarak işaretle' gibi bir metod) eklenebileceğini belirt."

**Prompt 2.3 (Arama ve Filtreleme için Model Hazırlıkları):**
"İlan modelimiz ve yardımcı modellerimiz üzerinde etkili arama, filtreleme ve sıralama işlemleri yapabilmek için gerekli teknik hazırlıkları detaylandır. Özellikle etiket sistemiyle entegrasyon ve performans optimizasyonu konularına odaklanarak:

### 1. İndeksleme Stratejisi:
* Hangi alanların veritabanı indeksine sahip olması gerektiğini belirt:
  * `HayvanIlani.durum` - Duruma göre filtreleme sık kullanılacağı için
  * `HayvanIlani.hayvan_turu` - Tür filtrelemesi yaygın bir kullanım durumu
  * `HayvanIlani.sehir` ve `HayvanIlani.ilce` - Konum bazlı aramalar için
  * `HayvanIlani.ilan_tarihi` - Tarihe göre sıralama yapılacağı için
  * Etiket ilişkisi için indeks gereksinimleri

### 2. Full-Text Search için Hazırlıklar:
* Django'nun `SearchVector` veya PostgreSQL'in full-text search özellikleriyle entegre çalışabilmesi için `HayvanIlani` modelinde hangi alanların arama vektörlerine dahil edilmesi gerektiğini açıkla:
  * `baslik`
  * `aciklama`
  * `karakter_ozellikleri`
  * vb.

### 3. Etiketlerle Filtreleme için Optimizasyonlar:
* Önceki bölümde tasarladığımız Tag modeli ile HayvanIlani modeli arasındaki ManyToMany ilişkisini filtreleme işlemlerinde optimum performansla kullanabilmek için:
  * Django ORM'de etkili filtreleme sorgularının nasıl yapılandırılacağı
  * Çok sayıda etiket filtrelemesi yapılırken performans düşüşlerini önleme stratejileri
  * `select_related` ve `prefetch_related` optimizasyonları

### 4. Coğrafi Sorgular için Hazırlıklar:
* Enlem/boylam koordinatları üzerinden yakınlık bazlı aramalar yapabilmek için:
  * GeoDjango kullanımı veya alternatif çözümler
  * Coğrafi indeksleme gereksinimleri
  * Mesafe bazlı sıralama için gerekli fonksiyonlar

### 5. Arama Sonuçlarının Alaka Düzeyine Göre Sıralanması:
* İlanları, aranan kriterlere uygunluk derecesine göre sıralamak için puan sisteminin nasıl yapılandırılabileceğini açıkla:
  * Başlık eşleşmelerine yüksek puan
  * Açıklama eşleşmelerine orta puan
  * Etiket eşleşmelerine belirli puan
  * Diğer alanlardaki eşleşmelere farklı puanlar
  * Bu puanların nasıl birleştirileceği ve sonuçların nasıl sıralanacağı

Bu hazırlıkların, özellikle API endpointlerinde ve view'larda nasıl kullanılacağına dair genel bir çerçeve sun. Hem basit kullanım senaryoları hem de karmaşık, çok parametreli arama ve filtreleme işlemleri için optimum yaklaşımı belirle."

---

## Bölüm 2: İlanların Yönetim Paneli (Django Admin)

**Prompt 3.1 (Admin Panelinde İlan Yönetimi):**
"İlanlarımızın ve ilgili modellerin Django admin panelinde nasıl yönetileceğini en ince ayrıntısına kadar tasarla. Site yöneticilerinin ilanları kolayca yönetebilmesi, arayabilmesi, filtreleyebilmesi ve düzenleyebilmesi için gerekli tüm özellikleri açıkla:

### 1. `HayvanIlaniAdmin` Sınıfı:
* `list_display`: Admin paneli liste görünümünde hangi alanların gösterileceği:
  ```python
  list_display = ('baslik', 'hayvan_turu', 'cins', 'sehir', 'durum', 'ilan_tarihi', 'goruntulenme_sayisi', 'get_etiketler')
  ```
  * `get_etiketler` özel bir metod olmalı ve ilanın etiketlerini virgülle ayrılmış şekilde göstermeli

* `list_filter`: Sağ tarafta hangi filtrelerin yer alacağı:
  ```python
  list_filter = ('durum', 'hayvan_turu', 'kisirlastirilmis', 'sehir', 'ilan_tarihi')
  ```

* `search_fields`: Admin arama kutusunun hangi alanlarda arama yapacağı:
  ```python
  search_fields = ('baslik', 'aciklama', 'sehir', 'ilce', 'ilan_sahibi__username')
  ```

* `filter_horizontal`: Çoklu seçim alanları için daha kullanışlı arayüz:
  ```python
  filter_horizontal = ('tags',)
  ```

* `readonly_fields`: Düzenleme formunda salt okunur olması gereken alanlar:
  ```python
  readonly_fields = ('ilan_tarihi', 'guncellenme_tarihi', 'slug', 'goruntulenme_sayisi', 'favori_sayisi')
  ```

* `prepopulated_fields`: Otomatik doldurulacak alanlar:
  ```python
  prepopulated_fields = {'slug': ('baslik',)}
  ```

### 2. Gelişmiş Özellikler:
* `fieldsets`: Düzenleme formunda alanları mantıksal gruplara ayırmak için:
  ```python
  fieldsets = (
      ('Temel Bilgiler', {
          'fields': ('baslik', 'slug', 'durum', 'ilan_sahibi', 'aciklama')
      }),
      ('Hayvan Özellikleri', {
          'fields': ('hayvan_turu', 'cins', 'isim', 'yas_yil', 'yas_ay', 'cinsiyet', 'boyut', 'renk', 'agirlik')
      }),
      ('Sağlık Bilgileri', {
          'fields': ('asilar', 'kisirlastirilmis', 'saglik_durumu', 'ozel_ihtiyaclar')
      }),
      ('Davranış ve Uyumluluk', {
          'fields': ('karakter_ozellikleri', 'cocuklarla_uyumlu', 'diger_hayvanlarla_uyumlu', 'ev_ortamina_uyumlu')
      }),
      ('Konum Bilgileri', {
          'fields': ('sehir', 'ilce', 'adres', 'enlem', 'boylam', 'gizli_adres')
      }),
      ('İletişim', {
          'fields': ('iletisim_tercihi', 'telefon')
      }),
      ('Etiketler', {
          'fields': ('tags',)
      }),
      ('Sahiplendirme Detayları', {
          'fields': ('sahiplendirme_sartlari',)
      }),
      ('İstatistikler', {
          'classes': ('collapse',),
          'fields': ('goruntulenme_sayisi', 'favori_sayisi', 'ilan_tarihi', 'guncellenme_tarihi')
      }),
  )
  ```

* `inlines`: İlan düzenleme sayfasında fotoğrafları da yönetebilmek için:
  ```python
  class HayvanFotografiInline(admin.TabularInline):
      model = HayvanFotografi
      extra = 1
      fields = ('fotograf', 'baslik', 'siralama', 'ana_fotograf')
  
  class HayvanIlaniAdmin(admin.ModelAdmin):
      inlines = [HayvanFotografiInline]
      # ... diğer ayarlar
  ```

* `actions`: Toplu işlemler için özel admin aksiyonları:
  ```python
  actions = ['mark_as_adopted', 'mark_as_expired', 'reset_view_count']
  
  def mark_as_adopted(self, request, queryset):
      queryset.update(durum='sahiplendirildi')
  mark_as_adopted.short_description = "Seçili ilanları 'sahiplendirildi' olarak işaretle"
  
  # ... diğer action metodları
  ```

### 3. Diğer Model Admin Sınıfları:
* `HayvanTuruAdmin`, `CinsAdmin`, `BasvuruAdmin`, `FavoriAdmin` için benzer düzenlemeleri ve özelleştirmeleri detaylandır. Özellikle:
  * Liste görünümlerinde hangi alanların gösterileceği
  * Filtreleme ve arama seçenekleri
  * Formların nasıl yapılandırılacağı
  
* `BasvuruAdmin` için özel aksiyonlar:
  ```python
  actions = ['approve_applications', 'reject_applications']
  
  def approve_applications(self, request, queryset):
      queryset.update(durum='onaylandi', islem_tarihi=timezone.now())
  approve_applications.short_description = "Seçili başvuruları onayla"
  ```

### 4. Admin Tema Özelleştirmeleri:
* Admin panelinde ilanlarla ilgili dashboard widget'ları veya özet bilgiler
* İlan durumlarını görsel olarak ayırt etmek için CSS sınıfları
* Harita entegrasyonu ile konum bilgilerinin gösterimi

Bu admin yapılandırmalarının her biri, site yöneticilerinin ilanları ve ilgili verileri verimli bir şekilde yönetmesine yardımcı olacak şekilde tasarlanmalıdır. Ayrıca, büyük veri setleriyle çalışırken performans sorunlarını önlemek için gerekli optimizasyonları da belirt."

---

## Bölüm 3: İlanların API Dünyası (Django Rest Framework)

**Prompt 4.1 (İlan API Endpoints):**
"Django Rest Framework kullanarak ilanlar ve ilgili veriler için oluşturulacak API endpoint'lerini en detaylı şekilde tanımla. Bu endpoint'ler, frontend uygulamasının ve mobil uygulamaların ilan verilerine erişimini sağlayacaktır. Özellikle etiket sistemiyle entegrasyona ve filtreleme yeteneklerine odaklanarak:

### 1. Temel İlan Endpoint'leri:

#### İlan Listeleme ve Oluşturma:
* URL: `GET, POST /api/ilanlar/`
* İşlev: Tüm ilanları listelemek ve yeni ilan oluşturmak
* Yetkilendirme:
  * GET için kimlik doğrulaması gerekmez (herkes erişebilir)
  * POST için kimlik doğrulaması gerekir
* Filtreleme Parametreleri:
  * Hayvan türü: `?hayvan_turu=kedi`
  * Şehir: `?sehir=Istanbul`
  * Durum: `?durum=aktif`
  * Etiketler: `?tags=oyuncu,kisirlastirilmis` (AND mantığı)
  * Yaş aralığı: `?min_yas=1&max_yas=5`
  * Cinsiyet: `?cinsiyet=erkek`
  * Boyut: `?boyut=kucuk`
  * Arama: `?search=sevimli+tekir`
  * Özel filtreler: `?kisirlastirilmis=true&cocuklarla_uyumlu=true`
  * Sıralama: `?ordering=-ilan_tarihi` (en yeniden eskiye)
* Sayfalama: Varsayılan sayfa boyutu 10, maksimum 50
* Response Format (GET):
  ```json
  {
    "count": 100,
    "next": "http://example.com/api/ilanlar/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "baslik": "Sevimli Tekir Yuva Arıyor",
        "slug": "sevimli-tekir-yuva-ariyor",
        "durum": "aktif",
        "hayvan_turu": {
          "id": 1,
          "ad": "Kedi",
          "slug": "kedi"
        },
        "cins": {
          "id": 5,
          "ad": "Tekir",
          "slug": "tekir"
        },
        "cinsiyet": "erkek",
        "yas": {
          "yil": 2,
          "ay": 4
        },
        "sehir": "İstanbul",
        "ilce": "Kadıköy",
        "kisirlastirilmis": true,
        "kisa_aciklama": "2 yaşında oyuncu bir tekir, apartman hayatına alışık...",
        "tags": [
          {
            "id": 3,
            "name": "Oyuncu",
            "slug": "oyuncu"
          },
          {
            "id": 7,
            "name": "Kısırlaştırılmış",
            "slug": "kisirlastirilmis"
          }
        ],
        "ana_fotograf": "https://example.com/media/hayvan_fotograflari/123_ana.jpg",
        "ilan_tarihi": "2025-05-20T15:30:00Z",
        "favori_sayisi": 8
      },
      // ... diğer ilanlar
    ]
  }
  ```

#### Tek İlan Detayı:
* URL: `GET, PUT, PATCH, DELETE /api/ilanlar/{id}/` veya `/api/ilanlar/{slug}/`
* İşlev: Belirli bir ilanın detaylarını görüntülemek, güncellemek veya silmek
* Yetkilendirme:
  * GET için kimlik doğrulaması gerekmez
  * PUT, PATCH, DELETE için ilan sahibi veya admin olma gerekir
* Response Format (GET):
  ```json
  {
    "id": 1,
    "baslik": "Sevimli Tekir Yuva Arıyor",
    "slug": "sevimli-tekir-yuva-ariyor",
    "durum": "aktif",
    "aciklama": "2 yaşında oyuncu bir tekir. Apartman hayatına alışık, çocuklarla çok iyi anlaşıyor...",
    "hayvan_turu": {
      "id": 1,
      "ad": "Kedi"
    },
    "cins": {
      "id": 5,
      "ad": "Tekir"
    },
    "isim": "Minnoş",
    "yas_yil": 2,
    "yas_ay": 4,
    "cinsiyet": "erkek",
    "boyut": "orta",
    "renk": "Gri çizgili",
    "agirlik": 4.5,
    "asilar": "Kuduz, Karma",
    "kisirlastirilmis": true,
    "saglik_durumu": "Sağlıklı, düzenli veteriner kontrolünden geçirildi.",
    "ozel_ihtiyaclar": "",
    "karakter_ozellikleri": "Çok oyuncu ve sevecen. Kucağa alınmayı ve okşanmayı çok seviyor.",
    "cocuklarla_uyumlu": true,
    "diger_hayvanlarla_uyumlu": true,
    "ev_ortamina_uyumlu": true,
    "sehir": "İstanbul",
    "ilce": "Kadıköy",
    "iletisim_tercihi": "telefon",
    "telefon": "+905XX XXX XXXX",  // Yalnızca giriş yapmış kullanıcılara gösterilir
    "sahiplendirme_sartlari": "Ev ziyareti yapılacaktır. Sahiplenme sözleşmesi imzalanması gerekiyor.",
    "tags": [
      {
        "id": 3,
        "name": "Oyuncu",
        "slug": "oyuncu",
        "icon": "fa-play"
      },
      {
        "id": 7,
        "name": "Kısırlaştırılmış",
        "slug": "kisirlastirilmis",
        "icon": "fa-check-circle"
      }
    ],
    "fotograflar": [
      {
        "id": 101,
        "url": "https://example.com/media/hayvan_fotograflari/123_1.jpg",
        "baslik": "Minnoş oyun oynarken",
        "ana_fotograf": true
      },
      {
        "id": 102,
        "url": "https://example.com/media/hayvan_fotograflari/123_2.jpg",
        "baslik": "Minnoş uyurken",
        "ana_fotograf": false
      }
    ],
    "ilan_sahibi": {
      "id": 42,
      "username": "hayvan_sever",
      "ad_soyad": "Ali Yılmaz", // Gizlilik ayarlarına göre gösterilir
      "profil_fotografi": "https://example.com/media/profil/42.jpg"
    },
    "ilan_tarihi": "2025-05-20T15:30:00Z",
    "guncellenme_tarihi": "2025-05-21T10:15:00Z",
    "goruntulenme_sayisi": 156,
    "favori_sayisi": 8,
    "kullanici_favoriledi": false  // Giriş yapmış kullanıcı için dinamik olarak belirlenir
  }
  ```

### 2. Yardımcı API Endpoint'leri:

#### Hayvan Türleri:
* URL: `GET /api/hayvan-turleri/`
* İşlev: Tüm hayvan türlerini listelemek
* Response Format:
  ```json
  [
    {
      "id": 1,
      "ad": "Kedi",
      "slug": "kedi",
      "icon": "fa-cat"
    },
    {
      "id": 2,
      "ad": "Köpek",
      "slug": "kopek",
      "icon": "fa-dog"
    },
    // ... diğer türler
  ]
  ```

#### Belirli Bir Hayvan Türüne Ait Cinsler:
* URL: `GET /api/hayvan-turleri/{id}/cinsler/`
* İşlev: Belirli bir hayvan türüne ait cinsleri listelemek
* Response Format:
  ```json
  {
    "hayvan_turu": {
      "id": 1,
      "ad": "Kedi",
      "slug": "kedi"
    },
    "cinsler": [
      {
        "id": 1,
        "ad": "Tekir",
        "slug": "tekir"
      },
      {
        "id": 2,
        "ad": "Siyam",
        "slug": "siyam"
      },
      // ... diğer cinsler
    ]
  }
  ```

#### Kullanıcının Kendi İlanları:
* URL: `GET /api/kullanici/ilanlar/`
* İşlev: Giriş yapmış kullanıcının kendi ilanlarını listelemek
* Yetkilendirme: Kimlik doğrulaması gerekli
* Filtreleme: `?durum=aktif` gibi standart ilan filtreleri kullanılabilir

#### Favoriler Yönetimi:
* URL: `POST /api/ilanlar/{id}/favori/`
* İşlev: Bir ilanı favorilere eklemek veya favorilerden çıkarmak
* Yetkilendirme: Kimlik doğrulaması gerekli
* Request Body: Gerekmez (toggle işlemi)
* Response: `{"status": "added", "favori_sayisi": 9}` veya `{"status": "removed", "favori_sayisi": 8}`

* URL: `GET /api/kullanici/favoriler/`
* İşlev: Kullanıcının favori ilanlarını listelemek
* Yetkilendirme: Kimlik doğrulaması gerekli

#### Başvuru Yönetimi:
* URL: `POST /api/ilanlar/{id}/basvur/`
* İşlev: Bir ilana sahiplenme başvurusu yapmak
* Yetkilendirme: Kimlik doğrulaması gerekli
* Request Body:
  ```json
  {
    "mesaj": "Bu sevimli kediyi sahiplenmek istiyorum. Daha önce de kedim vardı..."
  }
  ```

* URL: `GET /api/kullanici/basvurular/`
* İşlev: Kullanıcının yaptığı başvuruları listelemek
* Yetkilendirme: Kimlik doğrulaması gerekli

* URL: `GET /api/kullanici/gelen-basvurular/`
* İşlev: Kullanıcının ilanlarına gelen başvuruları listelemek
* Yetkilendirme: Kimlik doğrulaması gerekli

* URL: `PUT /api/basvurular/{id}/`
* İşlev: Bir başvurunun durumunu güncellemek (onaylamak/reddetmek)
* Yetkilendirme: Başvurunun ait olduğu ilanın sahibi olma gerekir
* Request Body:
  ```json
  {
    "durum": "onaylandi",
    "islem_notu": "Ev ziyareti için sizinle iletişime geçeceğim."
  }
  ```

### 3. Arama ve Filtreleme Özellikleri:

#### Gelişmiş Arama:
* URL: `GET /api/ilanlar/arama/`
* Parametreler: Standart ilan filtreleme parametrelerinin yanında:
  * `mesafe`: Belirli bir konuma olan maksimum mesafe (km cinsinden)
  * `lat` ve `lng`: Arama yapılacak konum koordinatları
  * `tag_logic`: Etiket filtrelemesi için mantık (default: "and", alternatif: "or")
  * `fields`: Hangi alanlarda arama yapılacağı (default: tüm alanlar)
  * `min_foto`: Minimum fotoğraf sayısı
  * `sort_by`: Özel sıralama seçenekleri ("en_yeni", "en_populer", "en_eski", "en_yakin")

Tüm bu endpoint'lerin URL yapılandırmasının nasıl tanımlanacağını, view'ların nasıl gerçekleştirileceğini ve Django Rest Framework'ün ViewSet, pagination, filtering gibi özelliklerinin nasıl kullanılacağını detaylı bir şekilde açıkla. Aynı zamanda, performans optimizasyonu için select_related ve prefetch_related gibi tekniklerin nerede ve nasıl kullanılacağını belirt."

**Prompt 4.2 (İlan Serializerları):**
"Django Rest Framework kullanarak ilanlar ve ilgili modeller için oluşturulacak serializer sınıflarını en ince ayrıntısına kadar tasarla. Bu serializer'lar, model verilerinin API yanıtlarına dönüştürülmesini ve istek verilerinin model nesnelerine dönüştürülmesini sağlayacaktır. Özellikle ilanlar ve etiketler arasındaki entegrasyona odaklanarak:

### 1. `HayvanIlaniSerializer` Sınıfı:

#### Temel Yapı:
```python
class HayvanIlaniSerializer(serializers.ModelSerializer):
    hayvan_turu = HayvanTuruSerializer(read_only=True)
    hayvan_turu_id = serializers.PrimaryKeyRelatedField(
        queryset=HayvanTuru.objects.all(), 
        source='hayvan_turu',
        write_only=True
    )
    
    cins = CinsSerializer(read_only=True)
    cins_id = serializers.PrimaryKeyRelatedField(
        queryset=Cins.objects.all(),
        source='cins',
        write_only=True
    )
    
    fotograflar = HayvanFotografiSerializer(many=True, read_only=True, source='hayvanfotografi_set')
    
    ilan_sahibi = UserSummarySerializer(read_only=True)
    tags = TagListSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source='tags',
        required=False
    )
    
    # İlan için bir "kısa açıklama" hesapla
    kisa_aciklama = serializers.SerializerMethodField()
    
    # Ana fotoğrafın URL'sini al
    ana_fotograf = serializers.SerializerMethodField()
    
    # Kullanıcının bu ilanı favorilere ekleyip eklemediğini kontrol et
    kullanici_favoriledi = serializers.SerializerMethodField()
    
    class Meta:
        model = HayvanIlani
        fields = [
            'id', 'baslik', 'slug', 'durum', 'hayvan_turu', 'hayvan_turu_id',
            'cins', 'cins_id', 'isim', 'yas_yil', 'yas_ay', 'cinsiyet', 'boyut',
            'renk', 'agirlik', 'asilar', 'kisirlastirilmis', 'saglik_durumu',
            'ozel_ihtiyaclar', 'karakter_ozellikleri', 'cocuklarla_uyumlu',
            'diger_hayvanlarla_uyumlu', 'ev_ortamina_uyumlu', 'sehir', 'ilce',
            'adres', 'enlem', 'boylam', 'gizli_adres', 'iletisim_tercihi',
            'telefon', 'sahiplendirme_sartlari', 'tags', 'tag_ids',
            'fotograflar', 'ilan_sahibi', 'ilan_tarihi', 'guncellenme_tarihi',
            'goruntulenme_sayisi', 'favori_sayisi', 'kisa_aciklama', 'ana_fotograf',
            'kullanici_favoriledi'
        ]
        read_only_fields = [
            'slug', 'ilan_tarihi', 'guncellenme_tarihi', 'goruntulenme_sayisi',
            'favori_sayisi', 'ilan_sahibi'
        ]
```

#### Özel Metodlar:
```python
def get_kisa_aciklama(self, obj):
    """Açıklamadan 150 karakterlik bir özet oluştur"""
    if not obj.aciklama:
        return ""
    if len(obj.aciklama) <= 150:
        return obj.aciklama
    return obj.aciklama[:147] + "..."

def get_ana_fotograf(self, obj):
    """Ana fotoğrafın URL'sini döndür, yoksa ilk fotoğrafı kullan"""
    try:
        ana_foto = obj.hayvanfotografi_set.filter(ana_fotograf=True).first()
        if not ana_foto:
            ana_foto = obj.hayvanfotografi_set.first()
        if ana_foto:
            return ana_foto.fotograf.url
    except Exception:
        pass
    return None

def get_kullanici_favoriledi(self, obj):
    """Giriş yapmış kullanıcı bu ilanı favorilere eklediyse True döndür"""
    request = self.context.get('request')
    if request and request.user.is_authenticated:
        return Favori.objects.filter(
            ilan=obj, 
            kullanici=request.user
        ).exists()
    return False
```

#### Create ve Update Metodları:
```python
def create(self, validated_data):
    # tags verisini ayır
    tags_data = validated_data.pop('tags', [])
    
    # Kullanıcıyı ilan sahibi olarak ayarla
    request = self.context.get('request')
    if request and request.user.is_authenticated:
        validated_data['ilan_sahibi'] = request.user
    
    # İlanı oluştur
    instance = super().create(validated_data)
    
    # Etiketleri ekle
    if tags_data:
        instance.tags.set(tags_data)
    
    return instance

def update(self, instance, validated_data):
    # tags verisini ayır
    tags_data = validated_data.pop('tags', None)
    
    # Diğer alanları güncelle
    instance = super().update(instance, validated_data)
    
    # Etiketleri güncelle (eğer gönderildiyse)
    if tags_data is not None:
        instance.tags.set(tags_data)
    
    return instance

def to_representation(self, instance):
    """
    Bazı alanları kullanıcı tipine göre göster/gizle
    """
    representation = super().to_representation(instance)
    request = self.context.get('request')
    
    # Giriş yapmamış kullanıcılar veya ilan sahibi olmayan kullanıcılar için iletişim bilgilerini gizle
    if not request or not request.user.is_authenticated or request.user != instance.ilan_sahibi:
        representation.pop('telefon', None)
        if instance.gizli_adres:
            representation.pop('adres', None)
    
    return representation
```

### 2. Farklı Kullanım Senaryoları için Özelleştirilmiş Serializer'lar:

#### Liste Görünümü için Hafif Serializer:
```python
class HayvanIlaniListSerializer(serializers.ModelSerializer):
    hayvan_turu = serializers.StringRelatedField()
    cins = serializers.StringRelatedField()
    tags = TagListSerializer(many=True, read_only=True)
    kisa_aciklama = serializers.SerializerMethodField()
    ana_fotograf = serializers.SerializerMethodField()
    yas = serializers.SerializerMethodField()
    
    class Meta:
        model = HayvanIlani
        fields = [
            'id', 'baslik', 'slug', 'durum', 'hayvan_turu', 'cins', 
            'cinsiyet', 'yas', 'sehir', 'ilce', 'kisirlastirilmis',
            'tags', 'ana_fotograf', 'kisa_aciklama', 'ilan_tarihi', 
            'favori_sayisi'
        ]
    
    def get_yas(self, obj):
        """Yaşı yıl ve ay olarak birleştir"""
        if obj.yas_yil is None and obj.yas_ay is None:
            return "Belirtilmemiş"
        
        parts = []
        if obj.yas_yil:
            parts.append(f"{obj.yas_yil} yıl")
        if obj.yas_ay:
            parts.append(f"{obj.yas_ay} ay")
        return " ".join(parts)
    
    # get_kisa_aciklama ve get_ana_fotograf metodları HayvanIlaniSerializer ile aynı
```

#### Fotoğraf Serializer:
```python
class HayvanFotografiSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = HayvanFotografi
        fields = ['id', 'url', 'baslik', 'siralama', 'ana_fotograf', 'yukleme_tarihi']
    
    def get_url(self, obj):
        try:
            return obj.fotograf.url
        except:
            return None
```

#### Başvuru Serializer:
```python
class BasvuruSerializer(serializers.ModelSerializer):
    basvuran = UserSummarySerializer(read_only=True)
    ilan = HayvanIlaniListSerializer(read_only=True)
    ilan_id = serializers.PrimaryKeyRelatedField(
        queryset=HayvanIlani.objects.all(),
        source='ilan',
        write_only=True
    )
    
    class Meta:
        model = Basvuru
        fields = [
            'id', 'ilan', 'ilan_id', 'basvuran', 'basvuru_tarihi',
            'mesaj', 'durum', 'islem_tarihi', 'islem_notu'
        ]
        read_only_fields = ['basvuran', 'basvuru_tarihi', 'durum', 'islem_tarihi']
    
    def create(self, validated_data):
        # Başvuranı otomatik olarak giriş yapmış kullanıcı yap
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['basvuran'] = request.user
        
        # Aynı ilana aynı kullanıcının başvurusunu engelle
        ilan = validated_data.get('ilan')
        if Basvuru.objects.filter(ilan=ilan, basvuran=validated_data['basvuran']).exists():
            raise serializers.ValidationError("Bu ilana daha önce başvuru yapmışsınız.")
        
        return super().create(validated_data)
```

### 3. Yardımcı Serializer'lar:

#### Hayvan Türü ve Cins Serializer'ları:
```python
class HayvanTuruSerializer(serializers.ModelSerializer):
    class Meta:
        model = HayvanTuru
        fields = ['id', 'ad', 'slug', 'icon']

class CinsSerializer(serializers.ModelSerializer):
    hayvan_turu = HayvanTuruSerializer(read_only=True)
    
    class Meta:
        model = Cins
        fields = ['id', 'ad', 'slug', 'aciklama', 'hayvan_turu']
```

#### Kullanıcı Özet Serializer:
```python
class UserSummarySerializer(serializers.ModelSerializer):
    ad_soyad = serializers.SerializerMethodField()
    profil_fotografi = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'ad_soyad', 'profil_fotografi']
    
    def get_ad_soyad(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.username
    
    def get_profil_fotografi(self, obj):
        try:
            return obj.profile.profil_fotografi.url
        except:
            return None
```

#### Favori Serializer:
```python
class FavoriSerializer(serializers.ModelSerializer):
    ilan = HayvanIlaniListSerializer(read_only=True)
    
    class Meta:
        model = Favori
        fields = ['id', 'ilan', 'ekleme_tarihi']
        read_only_fields = ['kullanici', 'ekleme_tarihi']
```

### 4. Validasyon ve İşleme Mantığı:

#### Cins-Tür Uyumluluk Kontrolü:
```python
def validate(self, data):
    """Seçilen cinsin hayvan türüne ait olduğunu doğrula"""
    hayvan_turu = data.get('hayvan_turu')
    cins = data.get('cins')
    
    if hayvan_turu and cins and cins.hayvan_turu != hayvan_turu:
        raise serializers.ValidationError({
            "cins": f"Seçilen cins ({cins.ad}), seçilen hayvan türüne ({hayvan_turu.ad}) ait değil."
        })
    
    return data
```

#### Fotoğraf İşleme:
```python
def create_or_update_photos(self, instance, photos_data):
    """İlanın fotoğraflarını oluştur/güncelle"""
    if not photos_data:
        return

    # Maksimum 10 fotoğraf kontrolü
    if instance.hayvanfotografi_set.count() + len(photos_data) > 10:
        raise serializers.ValidationError({
            "fotograflar": "Bir ilana en fazla 10 fotoğraf ekleyebilirsiniz."
        })
        
    # Yeni fotoğrafları ekle
    for photo_data in photos_data:
        HayvanFotografi.objects.create(ilan=instance, **photo_data)
        
    # Ana fotoğraf kontrolü - hiç ana fotoğraf işaretlenmediyse ilk fotoğrafı ana yap
    if not instance.hayvanfotografi_set.filter(ana_fotograf=True).exists():
        ilk_foto = instance.hayvanfotografi_set.first()
        if ilk_foto:
            ilk_foto.ana_fotograf = True
            ilk_foto.save()
```

### 5. Performans Optimizasyonu:

#### Prefetch ve Select İlişkili Alanlar:
```python
# View sınıfında:
def get_queryset(self):
    queryset = HayvanIlani.objects.all()
    
    # İlişkili verileri tek sorguda çek
    queryset = queryset.select_related(
        'hayvan_turu',
        'cins',
        'ilan_sahibi'
    ).prefetch_related(
        'tags',
        'hayvanfotografi_set'
    )
    
    return queryset
```

Bu serializer tasarımı, API üzerinden ilanların tutarlı bir şekilde temsil edilmesini, ilgili verilerin efektif bir şekilde yüklenmesini ve etiket sistemiyle sorunsuz bir entegrasyonu sağlar. Farklı görünümler için özelleştirilmiş serializer sınıfları, istemciye sadece ihtiyaç duyulan verileri göndererek API performansını optimize eder."

**Prompt 4.3 (Arama ve Filtreleme Mekanizması):**
"İlan API'mizde etkili arama ve filtreleme işlemleri yapabilmemiz için gerekli filtreleme, sıralama ve arama yeteneklerini en ince ayrıntısına kadar tasarla. Django Rest Framework'ün filtreleme altyapısını ve özellikle etiket sistemimizle entegrasyonu en verimli şekilde nasıl yapılandıracağımızı açıkla:

### 1. Temel Filtreleme Altyapısı:

#### Kullanılacak Paketler:
```python
# requirements.txt'ye eklenecek
django-filter>=21.1
```

#### Filterset Sınıfı:
```python
from django_filters import rest_framework as filters

class HayvanIlaniFilter(filters.FilterSet):
    # Temel filtreler
    durum = filters.ChoiceFilter(choices=HayvanIlani.DURUM_CHOICES)
    hayvan_turu = filters.NumberFilter(field_name='hayvan_turu__id')
    hayvan_turu_slug = filters.CharFilter(field_name='hayvan_turu__slug')
    cins = filters.NumberFilter(field_name='cins__id')
    cins_slug = filters.CharFilter(field_name='cins__slug')
    sehir = filters.CharFilter(lookup_expr='iexact')
    ilce = filters.CharFilter(lookup_expr='iexact')
    cinsiyet = filters.ChoiceFilter(choices=HayvanIlani.CINSIYET_CHOICES)
    boyut = filters.ChoiceFilter(choices=HayvanIlani.BOYUT_CHOICES)
    
    # Boolean filtreler
    kisirlastirilmis = filters.BooleanFilter()
    cocuklarla_uyumlu = filters.BooleanFilter()
    diger_hayvanlarla_uyumlu = filters.BooleanFilter()
    ev_ortamina_uyumlu = filters.BooleanFilter()
    
    # Yaş filtresi - yaş aralığı
    min_yas = filters.NumberFilter(method='filter_min_yas')
    max_yas = filters.NumberFilter(method='filter_max_yas')
    
    # Etiket filtresi
    tags = filters.CharFilter(method='filter_tags')
    tag_ids = filters.CharFilter(method='filter_tag_ids')
    tag_category = filters.CharFilter(method='filter_tag_category')
    tag_logic = filters.ChoiceFilter(
        choices=[('and', 'AND'), ('or', 'OR')],
        method='filter_tag_logic',
        initial='and'
    )
    
    # Fotoğraf sayısı filtresi
    min_foto = filters.NumberFilter(method='filter_min_foto')
    has_photo = filters.BooleanFilter(method='filter_has_photo')
    
    # Tarih filtresi
    min_date = filters.DateTimeFilter(field_name='ilan_tarihi', lookup_expr='gte')
    max_date = filters.DateTimeFilter(field_name='ilan_tarihi', lookup_expr='lte')
    
    # Arama filtresi
    search = filters.CharFilter(method='filter_search')
    
    class Meta:
        model = HayvanIlani
        fields = [
            'durum', 'hayvan_turu', 'hayvan_turu_slug', 'cins', 'cins_slug',
            'sehir', 'ilce', 'cinsiyet', 'boyut', 'kisirlastirilmis',
            'cocuklarla_uyumlu', 'diger_hayvanlarla_uyumlu', 'ev_ortamina_uyumlu',
        ]
```

#### Filtreleme Metodları:
```python
def filter_min_yas(self, queryset, name, value):
    """Minimum yaş filtresi (yıl bazında)"""
    return queryset.filter(yas_yil__gte=value)

def filter_max_yas(self, queryset, name, value):
    """Maksimum yaş filtresi (yıl bazında)"""
    return queryset.filter(yas_yil__lte=value)

def filter_tags(self, queryset, name, value):
    """
    Etiketlere göre filtreleme (slug bazında)
    Örnek: ?tags=oyuncu,kisirlastirilmis
    """
    tag_logic = self.data.get('tag_logic', 'and')
    if not value:
        return queryset
    
    tag_slugs = [slug.strip() for slug in value.split(',')]
    
    if tag_logic == 'and':
        # AND mantığı: Tüm etiketlere sahip ilanları getir
        for slug in tag_slugs:
            queryset = queryset.filter(tags__slug=slug)
        return queryset
    else:
        # OR mantığı: Etiketlerden herhangi birine sahip ilanları getir
        return queryset.filter(tags__slug__in=tag_slugs).distinct()

def filter_tag_ids(self, queryset, name, value):
    """
    Etiket ID'lerine göre filtreleme
    Örnek: ?tag_ids=1,5,9
    """
    tag_logic = self.data.get('tag_logic', 'and')
    if not value:
        return queryset
    
    try:
        tag_ids = [int(id.strip()) for id in value.split(',')]
    except ValueError:
        return queryset.none()
    
    if tag_logic == 'and':
        # AND mantığı
        for tag_id in tag_ids:
            queryset = queryset.filter(tags__id=tag_id)
        return queryset
    else:
        # OR mantığı
        return queryset.filter(tags__id__in=tag_ids).distinct()

def filter_tag_category(self, queryset, name, value):
    """
    Etiket kategorisine göre filtreleme
    Örnek: ?tag_category=davranis
    """
    if not value:
        return queryset
    
    return queryset.filter(tags__category=value).distinct()

def filter_tag_logic(self, queryset, name, value):
    """
    Bu metod doğrudan filtreleme yapmaz, diğer etiket filtrelerinin davranışını etkiler.
    Bu nedenle queryset'i değiştirmeden döndürüyoruz.
    """
    return queryset

def filter_min_foto(self, queryset, name, value):
    """
    Minimum fotoğraf sayısı filtresi
    Örnek: ?min_foto=3
    """
    if value < 1:
        return queryset
    
    # Fotoğraf sayısına göre filtreleme için annotation kullan
    from django.db.models import Count
    return queryset.annotate(
        foto_sayisi=Count('hayvanfotografi')
    ).filter(foto_sayisi__gte=value)

def filter_has_photo(self, queryset, name, value):
    """
    Fotoğrafı olan/olmayan ilanlar
    Örnek: ?has_photo=true
    """
    from django.db.models import Exists, OuterRef
    has_photo = HayvanFotografi.objects.filter(ilan=OuterRef('pk')).values('id')
    
    if value is True:
        return queryset.filter(Exists(has_photo))
    elif value is False:
        return queryset.filter(~Exists(has_photo))
    return queryset

def filter_search(self, queryset, name, value):
    """
    Metin bazlı arama
    Başlık, açıklama, karakter özellikleri ve etiketlerde arar
    """
    if not value:
        return queryset
    
    # PostgreSQL full text search kullanımı
    from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
    
    # Arama vektörlerini oluştur
    vector = SearchVector('