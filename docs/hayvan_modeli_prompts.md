# Hayvan Modeli Fazı için LLM Promptları

Bu döküman, Django/React tabanlı hayvan sahiplenme platformu projesinin "Hayvan Modeli" backend fazını, kod kullanmaksızın, sadece sözcüklerle ve kavramsal düzeyde tasarlamak amacıyla bir LLM (Büyük Dil Modeli) için hazırlanmış yönlendirme ve soruları (promptları) içermektedir. Amaç, LLM ile etkileşim kurarak bu fazın bütünsel ve sağlam temelli bir backend imgesini oluşturmaktır.

## Genel İlke
Bir LLM ile sadece cümleler kullanarak projenin özünü sözcüklerle nasıl bulurdum? Her prompt, bu ilkeyi yansıtarak, modelin işlevsel ve kapsamlı bir sözlü tanımını ortaya koymaya odaklanır.

---

## 1. `apps/hayvanlar/models.py` (Hayvan Modeli Tanımı)

Bu bölüm, hayvanların temel bilgilerini, ilişkilerini ve davranışlarını tanımlayan Django modelinin kavramsal tasarımına odaklanır.

### 1.1. Temel Alanlar (Attributes)
- "Hayvan modelinin sahip olması gereken temel veri alanlarını (fields) sözcüklerle tanımla. İsim, tür (kedi, köpek vb.), cins, yaş (tahmini veya kesin), cinsiyet, boyut (küçük, orta, büyük), genel açıklama, sağlık durumu (aşıları, kısırlaştırma durumu), sahiplenme durumu (sahiplendirilebilir, rezerve, sahiplendirildi) gibi kritik bilgileri kapsamalıdır."
- "Hayvanların platformda sergilenecek fotoğrafları için modelde nasıl bir alan yapısı düşünülmeli? Tek bir ana fotoğraf mı, yoksa birden fazla fotoğraf galerisi mi desteklenmeli? Bu alanların özelliklerini açıkla."
- "Hayvanın bulunduğu coğrafi konum (örneğin il, ilçe) ve sisteme eklendiği tarih/saat bilgileri için gerekli model alanlarını ve bu alanların amaçlarını belirt."

### 1.2. İlişkiler (Relationships)
- "Hayvan modelini, daha önce tasarladığımız 'Kategori' modeli (örneğin, 'evcil hayvan', 'çiftlik hayvanı' gibi genel sınıflandırmalar) ile nasıl bir ilişki (ForeignKey, ManyToManyField vb.) kurarak bağlamalıyız? Bu ilişkinin mantığını ve Django modelindeki yansımasını açıkla."
- "Hayvanları daha detaylı sınıflandırmak veya özelliklerini belirtmek için kullanılacak 'Etiket' modeli (örneğin, 'oyuncu', 'çocuklarla iyi anlaşır', 'özel bakım gerekir') ile Hayvan modeli arasında nasıl bir çoktan-çoğa (ManyToMany) ilişki kurulmalıdır? Bu ilişkinin amacını ve kullanım senaryolarını izah et."
- "Sistemdeki her hayvanın bir sorumlu 'Kullanıcı' (bireysel sahip, barınak yetkilisi vb.) ile nasıl ilişkilendirileceğini modelle. Bu ilişkinin türünü ve önemini vurgula."

### 1.3. Model Metotları ve Meta Seçenekleri
- "Hayvan modeline eklenebilecek, iş mantığını kolaylaştıracak veya veri sunumunu zenginleştirecek özel Python metotları veya Django model property'leri neler olabilir? Örneğin, hayvanın yaşını okunabilir bir formatta döndüren bir metot veya ana fotoğrafının URL'ini veren bir property."
- "Hayvan modelinin Django admin panelindeki davranışını, veritabanı sorgularındaki varsayılan sıralamasını veya modelin okunabilir isimlerini tanımlamak için `class Meta` içerisinde hangi seçenekler (örneğin, `ordering`, `verbose_name`, `verbose_name_plural`) kullanılmalı ve bunların gerekçeleri nelerdir?"

## 2. `apps/hayvanlar/managers.py` (Özel Veritabanı Yöneticileri)
- "Hayvan modeli için sıkça tekrarlanacak veya karmaşık veritabanı sorgularını basitleştirmek amacıyla özel bir Django 'manager' sınıfı nasıl tasarlanır? Bu manager sınıfında yer alabilecek (örneğin, `get_available_animals()` veya `get_animals_by_species(species_name)`) metotları ve işlevlerini sözcüklerle açıkla."

## 3. `apps/hayvanlar/utils.py` (Yardımcı Fonksiyonlar)
- "`apps/hayvanlar/` dizini altında, hayvanlarla ilgili genel amaçlı yardımcı fonksiyonları barındıracak `utils.py` dosyasında ne tür işlevler tanımlanabilir? Örneğin, hayvan fotoğraflarını yükleme sırasında yeniden boyutlandırma, isimlendirme standartları uygulama veya hayvan profilleri için benzersiz kısa isimler (slug) oluşturma gibi fonksiyonları ve amaçlarını anlat."

## 4. `apps/hayvanlar/signals.py` (Olay Bazlı İşlemler - Sinyaller)
- "Hayvan modeli üzerinde bir kayıt oluşturulduğunda (post_save), güncellendiğinde veya silindiğinde (post_delete) otomatik olarak tetiklenecek işlemler için Django sinyalleri (signals) nasıl kurgulanır? Örneğin, yeni bir hayvan eklendiğinde ilgili kullanıcılara bildirim gönderilmesi veya bir hayvan sahiplendirildiğinde istatistiklerin güncellenmesi gibi senaryoları ve bu sinyallerin işleyişini açıkla."

## 5. `apps/hayvanlar/admin.py` (Django Admin Panel Entegrasyonu)
- "Hayvan modelinin Django admin arayüzünde nasıl daha etkin ve kullanıcı dostu bir şekilde yönetilebileceğini detaylandır. Admin listesinde hangi hayvan bilgilerinin (list_display) gösterilmesi, hangi alanlara göre filtreleme (list_filter) ve arama (search_fields) yapılabilmesi gerektiğini belirt. Varsa, ilişkili modellerin (örneğin fotoğraflar) inline olarak düzenlenebilmesi için öneriler sun."

## 6. `apps/hayvanlar/serializers.py` (API Veri Serileştiricileri)
- "Hayvan modeline ait verilerin React frontend'i veya diğer istemciler tarafından tüketilebilmesi için Django REST Framework (DRF) kullanılarak nasıl 'serializer' sınıfları tasarlanmalıdır? Bu serializer'ların hangi model alanlarını içereceğini, ilişkili modellerden (Kategori, Etiket, Kullanıcı) hangi bilgileri nasıl (nested serializer, primary key, slug vb.) sunacağını ve veri doğrulamalarını (validations) nasıl ele alacağını açıkla."
- "Farklı API endpoint ihtiyaçları için (örneğin, bir hayvan listesi için daha az detay içeren bir serializer, tek bir hayvanın tüm detaylarını gösteren başka bir serializer) birden fazla serializer tanımlamanın gerekçelerini ve bu serializer'lar arasındaki farkları belirt."

## 7. `apps/hayvanlar/views.py` (API Endpoint Görünümleri)
- "Hayvan verileri üzerinde CRUD (Create, Read, Update, Delete) işlemlerini gerçekleştirecek API endpoint'lerini (views veya viewsets) DRF kullanarak nasıl yapılandırmalıyız? Kullanılacak view sınıflarını (APIView, Generic Views, ViewSets) ve bunların temel işlevlerini tanımla."
- "Bu API endpoint'lerinde kimlik doğrulama (authentication) ve yetkilendirme (permissions) mekanizmaları nasıl işletilmeli? Örneğin, herkesin hayvanları listeleyebilmesi ancak sadece kayıtlı kullanıcıların yeni hayvan ekleyebilmesi veya sadece hayvanın sorumlu kullanıcısının güncelleme/silme yapabilmesi gibi kuralları nasıl tanımlarız?"
- "API üzerinden hayvanları çeşitli kriterlere göre filtreleme, arama ve sıralama işlevsellikleri bu view'lerde nasıl desteklenmeli? DRF'in bu konudaki yerleşik araçlarından (filtering backends) nasıl faydalanılır?"
- "API'den dönen hayvan listelerinin yönetilebilir parçalar halinde sunulması için sayfalama (pagination) stratejileri (örneğin, PageNumberPagination, LimitOffsetPagination) nasıl uygulanır?"

## 8. `apps/hayvanlar/urls.py` (API URL Yönlendirmeleri)
- "`views.py` dosyasında tanımlanan hayvan API endpoint'lerine (örneğin, `/api/v1/hayvanlar/`, `/api/v1/hayvanlar/{id}/`) erişimi sağlayacak URL yapılandırmasını (URL patterns) DRF router veya standart Django URL tanımlamaları kullanarak nasıl oluştururuz? Bu URL'lerin mantığını ve işlevlerini açıkla."

## 9. `apps/hayvanlar/servisler.py` (İş Mantığı Katmanı - Servisler)
- "Hayvanlarla ilgili daha karmaşık veya birden fazla adımı içeren iş mantıklarını (örneğin, bir hayvan kaydı oluşturulurken aynı anda profil resmi işleme, ilgili kullanıcılara e-posta gönderme gibi) API view'lerinden ayırarak bir 'servis katmanı' (`servisler.py`) içinde nasıl soyutlayabiliriz? Bu katmanda yer alabilecek fonksiyonları ve bu yaklaşımın avantajlarını (test edilebilirlik, kod tekrarını önleme vb.) anlat."

## 10. `apps/hayvanlar/filters.py` (API Filtreleme Setleri)
- "Kullanıcıların hayvan API'si üzerinden hayvanları tür, cins, yaş aralığı, konum, sahip olduğu etiketler gibi çeşitli ve birleşik kriterlere göre dinamik olarak filtreleyebilmesi için `django-filter` kütüphanesi kullanılarak nasıl özel bir `FilterSet` sınıfı (`filters.py` içinde) tanımlanır? Bu `FilterSet` içinde hangi alanlara göre ne tür filtreleme (exact match, range, case-insensitive contains vb.) seçenekleri sunulabileceğini detaylandır."

---
Bu promptlar, Hayvan Modeli fazının backend tasarımını kapsamlı bir şekilde ele almak ve LLM'den detaylı, sözlü bir tasarım elde etmek için bir başlangıç noktasıdır.