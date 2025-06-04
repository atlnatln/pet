# Etiketler Uygulaması Fazı için LLM Promptları

Bu döküman, Django/React tabanlı hayvan sahiplenme platformu projesinin "Etiketler Uygulaması" backend fazını, kod kullanmaksızın, sadece sözcüklerle ve kavramsal düzeyde tasarlamak amacıyla bir LLM (Büyük Dil Modeli) için hazırlanmış yönlendirme ve soruları (promptları) içermektedir. Amaç, LLM ile etkileşim kurarak bu fazın bütünsel ve sağlam temelli bir backend imgesini oluşturmaktır.

## Genel İlke
Bir LLM ile sadece cümleler kullanarak projenin özünü sözcüklerle nasıl bulurdum? Her prompt, bu ilkeyi yansıtarak, modelin işlevsel ve kapsamlı bir sözlü tanımını ortaya koymaya odaklanır.

---

## 1. `apps/etiketler/models.py` (Etiket Modeli Tanımı)

Bu bölüm, etiketlerin temel bilgilerini, diğer modellerle ilişkilerini ve davranışlarını tanımlayan Django modelinin kavramsal tasarımına odaklanır.

### 1.1. Temel Alanlar (Attributes)
- "Etiket modelinin sahip olması gereken temel veri alanlarını (fields) sözcüklerle tanımla. Örneğin, etiketin benzersiz adı (name), isteğe bağlı bir açıklaması (description), oluşturulma tarihi (created_at) gibi alanlar nasıl olmalıdır? Etiket adlarının benzersiz (unique) ve büyük/küçük harfe duyarsız olması (case-insensitive uniqueness) için nasıl bir yaklaşım benimsenmeli?"
- "Etiketlerin kullanıcı arayüzünde daha iyi ayırt edilebilmesi veya görselleştirilebilmesi için bir renk kodu (color_code) veya ikon (icon) alanı eklemek mantıklı mıdır? Bu tür alanların potansiyel faydalarını ve modeldeki yerini açıkla."

### 1.2. İlişkiler (Relationships)
- "Etiket modelinin, platformdaki 'Hayvanlar' ve 'İlanlar' modelleriyle nasıl bir çoktan-çoğa (ManyToMany) ilişki kuracağını detaylandır. Bu ilişkinin amacını, her iki model açısından da kullanım senaryolarını ve Django modelindeki yansımasını (örneğin, `related_name` kullanımı) açıkla."
- "Gelecekte eklenebilecek 'Blog Yazıları' gibi diğer içerik türleriyle de etiketlerin ilişkilendirilmesi düşünülüyorsa, bu genel etiketleme sistemi için model tasarımında nasıl bir esneklik sağlanabilir?"

### 1.3. Model Metotları ve Meta Seçenekleri
- "Etiket modeline, bir etiketin kaç tane hayvan veya ilan ile ilişkilendirildiğini döndüren bir Python metodu veya Django model property'si eklemek faydalı olur mu? Bu tür hesaplanmış alanların avantajlarını ve modeldeki yerini tartış."
- "Etiket modelinin Django admin panelindeki davranışını, veritabanı sorgularındaki varsayılan sıralamasını (örneğin, ada göre alfabetik) veya modelin okunabilir isimlerini tanımlamak için `class Meta` içerisinde hangi seçenekler (örneğin, `ordering`, `verbose_name`, `verbose_name_plural`, `unique_together` veya `constraints`) kullanılmalı ve bunların gerekçeleri nelerdir?"

## 2. `apps/etiketler/managers.py` (Özel Veritabanı Yöneticileri)
- "Etiket modeli için, sık kullanılan veya karmaşık veritabanı sorgularını basitleştirecek özel bir Django 'manager' sınıfı nasıl tasarlanabilir? Örneğin, en popüler etiketleri (en çok kullanılanlar) getiren veya belirli bir harf ile başlayan etiketleri listeleyen metotları ve bu manager'ın işlevlerini sözcüklerle açıkla."

## 3. `apps/etiketler/admin.py` (Django Admin Panel Entegrasyonu)
- "Etiket modelinin Django admin arayüzünde nasıl etkin bir şekilde yönetilebileceğini detaylandır. Admin listesinde hangi etiket bilgilerinin (list_display) gösterilmesi, hangi alanlara göre filtreleme (list_filter) ve arama (search_fields) yapılabilmesi gerektiğini belirt. Etiketlerin toplu olarak düzenlenmesi veya birleştirilmesi gibi admin eylemleri (actions) düşünülebilir mi?"

## 4. `apps/etiketler/serializers.py` (API Veri Serileştiricileri)
- "Etiket modeline ait verilerin React frontend'i veya diğer istemciler tarafından tüketilebilmesi için Django REST Framework (DRF) kullanılarak nasıl 'serializer' sınıfları tasarlanmalıdır? Bu serializer'ların hangi model alanlarını içereceğini (örneğin, sadece isim mi, yoksa açıklama ve renk kodu da mı?) ve veri doğrulamalarını nasıl ele alacağını açıkla."
- "İlişkili modeller (Hayvanlar, İlanlar) serileştirilirken, bu modellere ait etiketlerin nasıl temsil edileceğini (örneğin, etiket isimlerinin bir listesi olarak mı, yoksa tam etiket nesneleri olarak mı?) ve bu seçimin performans ve kullanım kolaylığı açısından etkilerini tartış."
- "Etiket oluşturma veya güncelleme sırasında, etiket adının benzersizliğini (büyük/küçük harf duyarsız) sağlamak için serializer katmanında ne tür doğrulamalar (validations) yapılmalıdır?"

## 5. `apps/etiketler/views.py` (API Endpoint Görünümleri)
- "Etiket verileri üzerinde CRUD (Create, Read, Update, Delete) işlemlerini gerçekleştirecek API endpoint'lerini (views veya viewsets) DRF kullanarak nasıl yapılandırmalıyız? Kullanılacak view sınıflarını (APIView, Generic Views, ViewSets) ve bunların temel işlevlerini tanımla."
- "Bu API endpoint'lerinde kimlik doğrulama (authentication) ve yetkilendirme (permissions) mekanizmaları nasıl işletilmeli? Örneğin, herkesin etiketleri listeleyebilmesi ancak sadece yetkili kullanıcıların (adminler) yeni etiket oluşturabilmesi veya mevcut etiketleri düzenleyip silebilmesi gibi kuralları nasıl tanımlarız?"
- "API üzerinden etiketleri çeşitli kriterlere göre (örneğin, isme göre arama, popülerliğe göre sıralama) filtreleme, arama ve sıralama işlevsellikleri bu view'lerde nasıl desteklenmeli? Otomatik tamamlama (autocomplete) senaryoları için özel bir endpoint veya view mantığına ihtiyaç var mıdır?"
- "API'den dönen etiket listelerinin yönetilebilir parçalar halinde sunulması için sayfalama (pagination) stratejileri nasıl uygulanır?"

## 6. `apps/etiketler/urls.py` (API URL Yönlendirmeleri)
- "`views.py` dosyasında tanımlanan etiket API endpoint'lerine (örneğin, `/api/v1/etiketler/`, `/api/v1/etiketler/{id}/`) erişimi sağlayacak URL yapılandırmasını (URL patterns) DRF router veya standart Django URL tanımlamaları kullanarak nasıl oluştururuz? Bu URL'lerin mantığını ve işlevlerini açıkla."

## 7. `apps/etiketler/servisler.py` (İş Mantığı Katmanı - Servisler)
- "Etiketlerle ilgili daha karmaşık iş mantıklarını (örneğin, bir etiket silinirken ilişkili olduğu tüm içeriklerden kaldırılması veya bir etiketin adının değiştirilmesi durumunda tüm ilişkilerde güncellenmesi gibi) API view'lerinden ayırarak bir 'servis katmanı' (`servisler.py`) içinde nasıl soyutlayabiliriz? Bu katmanda yer alabilecek fonksiyonları ve bu yaklaşımın avantajlarını (test edilebilirlik, kod tekrarını önleme, atomik işlemler) anlat."
- "Yeni bir etiket oluşturulurken, sistemde zaten var olan (büyük/küçük harf duyarsız olarak) bir etiketle çakışmasını önlemek ve var olanı kullanmak gibi bir mantık servis katmanında nasıl ele alınabilir?"

## 8. `apps/etiketler/filters.py` (API Filtreleme Setleri)
- "Kullanıcıların etiket API'si üzerinden etiketleri isme göre (örneğin, 'içerir' veya 'başlar' şeklinde) arayabilmesi veya belirli bir modelle (örneğin, sadece 'Hayvanlar' ile ilişkili etiketler) ilişkili olanları filtreleyebilmesi için `django-filter` kütüphanesi kullanılarak nasıl özel bir `FilterSet` sınıfı (`filters.py` içinde) tanımlanır? Bu `FilterSet` içinde hangi alanlara göre ne tür filtreleme seçenekleri sunulabileceğini detaylandır."

---
Bu promptlar, Etiketler Uygulaması fazının backend tasarımını kapsamlı bir şekilde ele almak ve LLM'den detaylı, sözlü bir tasarım elde etmek için bir başlangıç noktasıdır.