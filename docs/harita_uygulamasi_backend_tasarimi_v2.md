# Romanımızın Mekânsal Keşif Bölümü: "Harita Uygulaması" Backend Tasarımı (Revize Edilmiş)

## Önsöz: Etkileşimli Harita Üzerinden Hayvan Dostlarımızı Keşfetmek

**Prompt 1.0 (Revize Edilmiş Kavramsal Çerçeve):**
"Sevgili LLM, 'Harita Uygulaması'nın bu revize edilmiş bölümünde, kullanıcılarımızın hayvan dostlarımızı interaktif bir harita üzerinde keşfetmelerini sağlayacak bir backend tasarlayacağız. Temel varsayımımız şu: İlan sahipleri, hayvanlarının konumunu doğrudan harita üzerinde bir nokta seçerek belirleyecekler; sistemin koordinatlardan otomatik adres tespiti (reverse geocoding) yapmasına gerek olmayacak. Kullanıcılar harita üzerinde gezinebilecek, yakınlaştırıp uzaklaştırabilecek ve farklı bölgelerdeki hayvan ilanlarını (işaretçilerini) görebilecekler. Bu sistem, daha önce tasarladığımız 'İlanlar Uygulaması' ve 'Etiket Uygulaması' ile nasıl kusursuz bir uyum içinde çalışacak? Harita görünümünde ilanların filtrelenmesi (etiketlere, türe vb. göre) nasıl sağlanacak? Performanslı bir harita deneyimi için backend'in hangi verileri, hangi formatta ve hangi koşullarda sunması gerektiğini adım adım kelimelerle inşa edelim."

---

## Bölüm 1: Altyapısal Hazırlıklar ve Model Entegrasyonu

**Prompt 2.1 (GeoDjango ve `HayvanIlani` Modelinde Konum Yönetimi):**
"Harita uygulamamız için GeoDjango'nun temel altyapısının (PostgreSQL/PostGIS kurulumu, `settings.py` ayarları) hazır olduğunu varsayarak, `HayvanIlani` modelimizdeki konum bilgisinin yönetimine odaklanalım.

1.  **`HayvanIlani` Modelinde `konum` Alanı:**
    *   Modelimizde, hayvanın konumunu saklamak için `django.contrib.gis.db.models.PointField` tipinde bir `konum` alanı olduğunu teyit et. Bu alanın `geography=True` ve `null=True, blank=True` (kullanıcı konum girmeyidebilir) olabileceğini belirt.
    *   Kullanıcı bir ilanı kaydederken veya güncellerken, frontend'den gelen (harita üzerinden seçilmiş) enlem/boylam bilgisinin bu `konum` (PointField) alanına nasıl kaydedileceğini açıkla. Bu süreçte backend'in ek bir geocoding işlemi yapmasına **gerek olmadığını** vurgula.

2.  **Veri Girişi ve Validasyon:**
    *   Frontend'den gelen koordinat verisinin (enlem, boylam) backend tarafından nasıl alınacağını ve `Point` nesnesine dönüştürülerek `konum` alanına atanacağını tanımla.
    *   Koordinatların geçerli aralıklarda olup olmadığına dair temel bir validasyonun (örn: enlem -90 ile +90 arası) serializer veya model seviyesinde nasıl yapılabileceğini belirt.

Bu bölüm, kullanıcı tarafından doğrudan sağlanan konum verisinin modelimizde nasıl saklanacağını ve yönetileceğini netleştirmelidir."

---

## Bölüm 2: Harita Odaklı API Endpoint'leri

**Prompt 3.1 (Harita Görünümü İçin İlan Veri Servisi):**
"Kullanıcıların harita üzerinde gezinirken gördükleri alandaki hayvan ilanlarını listeleyecek temel API endpoint'ini tasarla. Bu endpoint, performans ve filtrelenebilirlik açısından optimize edilmelidir.

*   **Endpoint URL ve Metodu:** `GET /api/ilanlar/harita-gorunumu/`
*   **Temel İşlev:** Belirli bir coğrafi sınırlayıcı kutu (bounding box - `bbox`) ve mevcut filtrelere (etiketler, hayvan türü, ilan durumu vb.) uyan hayvan ilanlarını, harita üzerinde işaretçi olarak gösterilmeye uygun bir formatta döndürmek.
*   **İstek Parametreleri (Query Parameters):**
    *   `bbox`: Görüntülenen harita alanının coğrafi sınırları. Format: `min_boylam,min_enlem,max_boylam,max_enlem` (örn: `28.9,41.0,29.1,41.2`). Bu parametre zorunlu olmalı.
    *   `zoom`: Mevcut harita yakınlaştırma seviyesi (isteğe bağlı, kümeleme için kullanılabilir).
    *   `tags`: Virgülle ayrılmış etiket slug'ları veya ID'leri (örn: `oyuncu,kisirlastirilmis`).
    *   `hayvan_turu`: Hayvan türü ID'si veya slug'ı.
    *   Diğer ilan filtreleri (`durum`, `cinsiyet` vb. ilan modelinden gelen alanlar).
*   **Yanıt Formatı (GeoJSON FeatureCollection):**
    ```json
    {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [29.035, 41.080] // [boylam, enlem]
          },
          "properties": {
            "id": 123, // İlan ID'si
            "slug": "sevimli-tekir-yuva-ariyor",
            "baslik": "Sevimli Tekir Yuva Arıyor",
            "hayvan_turu_slug": "kedi", // Hızlı filtreleme ve ikon seçimi için
            "ana_fotograf_thumbnail_url": "https://example.com/media/thumbnails/123.jpg", // Küçük resim
            // İşaretçi popup'ında gösterilecek diğer kısa bilgiler (örn: yaş, cinsiyet)
            "yas_str": "2 yıl",
            "cinsiyet_str": "Erkek"
          }
        }
        // ... diğer ilanlar ...
      ]
    }
    ```
    *   `properties` içinde, frontend'in işaretçileri ve kısa bilgi pencerelerini (popup) oluşturmak için ihtiyaç duyacağı minimum ve optimize edilmiş bilgileri içermesini sağla.

Bu endpoint'in, `HayvanIlani` modelindeki `konum` alanını kullanarak `bbox` içindeki ilanları nasıl verimli bir şekilde sorgulayacağını (GeoDjango'nun mekansal sorgu yetenekleri, örn: `konum__within=bbox_polygon`) ve diğer filtreleri nasıl uygulayacağını açıkla."

**Prompt 3.2 (Harita İşaretçi Kümeleme API Endpoint'i):**
"Harita görünümü uzaklaştırıldığında (zoom out), çok sayıda işaretçinin üst üste binerek okunaksız hale gelmesini önlemek ve performansı artırmak için işaretçi kümeleme (marker clustering) mantığını destekleyecek bir API endpoint'i tasarla.

*   **Endpoint URL ve Metodu:** `GET /api/ilanlar/harita-kumeleri/`
*   **Temel İşlev:** Belirli bir coğrafi sınırlayıcı kutu (`bbox`), yakınlaştırma seviyesi (`zoom`) ve mevcut filtrelere göre, ya tekil ilan işaretçilerini ya da ilan kümelerini döndürmek.
*   **İstek Parametreleri:**
    *   `bbox`: Zorunlu.
    *   `zoom`: Zorunlu. Yakınlaştırma seviyesine göre kümeleme algoritması farklı çalışabilir.
    *   Diğer ilan filtreleri (`tags`, `hayvan_turu` vb.).
*   **Yanıt Formatı (GeoJSON FeatureCollection):**
    *   **Tekil İşaretçi (Yakın zoom seviyelerinde):**
        ```json
        {
          "type": "Feature",
          "geometry": { "type": "Point", "coordinates": [29.035, 41.080] },
          "properties": {
            "id": 123, // İlan ID'si
            "cluster": false, // Bu bir küme değil
            // ... Prompt 3.1'deki gibi diğer ilan özellikleri ...
          }
        }
        ```
    *   **Küme İşaretçisi (Uzak zoom seviyelerinde):**
        ```json
        {
          "type": "Feature",
          "geometry": { "type": "Point", "coordinates": [29.050, 41.090] }, // Kümenin merkezi
          "properties": {
            "cluster": true,
            "point_count": 15, // Bu kümedeki ilan sayısı
            "cluster_id": "cluster_abc123" // Küme için benzersiz bir ID
            // İsteğe bağlı: Kümedeki hayvan türü dağılımı gibi özet bilgiler
          }
        }
        ```
*   **Backend Kümeleme Mantığı:**
    *   Backend'in belirli bir `zoom` seviyesi ve `bbox` için ilanları nasıl kümeleyeceğine dair genel bir yaklaşım tanımla (örn: grid tabanlı bir algoritma veya PostGIS'in kümeleme fonksiyonları kullanılabilirse).
    *   Filtrelerin kümeleme sonuçlarını nasıl etkileyeceğini açıkla (filtrelenmiş ilanlar üzerinden kümeleme yapılmalı).

Bu endpoint, frontend'in farklı zoom seviyelerinde haritayı akıcı bir şekilde göstermesine yardımcı olacaktır. Backend'in bu kümelemeyi nasıl verimli bir şekilde yapabileceğine dair stratejiler sun."

---

## Bölüm 3: Mekansal Sorgu Verimliliği ve OSM Politikaları

**Prompt 4.1 (Verimli Mekansal Sorgular ve Filtre Entegrasyonu):**
"Harita API endpoint'lerinin (`harita-gorunumu` ve `harita-kumeleri`) performanslı çalışması için Django ORM ve GeoDjango kullanılarak mekansal sorguların nasıl optimize edileceğini detaylandır. Özellikle, coğrafi filtreleme (`bbox` ile) ile standart ilan ve etiket filtrelerinin bir arada verimli bir şekilde nasıl çalışacağını açıkla.

1.  **GeoDjango Sorgu Örnekleri:**
    *   `konum__within=bbox_polygon`: Belirli bir poligon (sınırlayıcı kutu) içindeki noktaları bulma.
    *   Gerekirse diğer mekansal sorgu fonksiyonları.

2.  **Filtrelerin Birleştirilmesi:**
    *   `HayvanIlaniFilter` (veya benzeri bir filtreleme sınıfı) kullanarak hem mekansal filtrelerin hem de `tags`, `hayvan_turu` gibi diğer alanlara dayalı filtrelerin nasıl birleştirileceğini göster.
    *   Veritabanı seviyesinde bu birleşik sorguların nasıl oluşturulacağı ve performans için nasıl optimize edileceği (indeks kullanımı vb.).

3.  **Veritabanı İndeksleri:**
    *   `HayvanIlani` modelindeki `konum` (PointField) alanı için mekansal bir indeksin (örn: GiST indeksi PostGIS'te) mutlak gerekliliğini vurgula.
    *   Sık kullanılan filtre alanları (örn: `durum`, `hayvan_turu_id`, `tags` ilişkisi) için de uygun veritabanı indekslerinin önemini belirt.

4.  **Performans İpuçları:**
    *   `select_related` ve `prefetch_related` kullanarak ilişkili verilerin (örn: ilan sahibinin bazı bilgileri, etiketler) verimli bir şekilde çekilmesi.
    *   Sadece ihtiyaç duyulan alanların (`.values()` veya `.only()`) seçilerek veri transferinin azaltılması, özellikle GeoJSON `properties` için.
    *   Büyük veri setlerinde sayfalama (pagination) veya sonuç sınırlama stratejileri (özellikle kümeleme yapılmıyorsa).

Bu bölüm, backend'in yoğun harita isteklerine hızlı ve verimli yanıtlar verebilmesi için gerekli teknik detayları sağlamalıdır."

**Prompt 4.2 (OpenStreetMap Kullanım Politikaları ve Atıf):**
"Kullanıcılarımızın harita üzerinde gezinirken gördükleri altlık haritanın OpenStreetMap (OSM) veya OSM tabanlı bir sağlayıcıdan geldiğini varsayarak, bu kullanımın getirdiği sorumlulukları ve politikalara uyumu tekrar vurgula. Koordinattan adres tespitine (reverse geocoding) gerek olmaması bu durumu nasıl etkiler?

1.  **Harita Döşemeleri (Map Tiles) ve Kullanım Politikası:**
    *   Frontend uygulamasının harita döşemelerini OSM'in ana sunucularından veya üçüncü parti bir sağlayıcıdan (MapTiler, Mapbox'ın ücretsiz katmanı vb.) çekeceğini belirt.
    *   Bu döşeme sunucularının kendi "Kullanım Politikaları" olduğunu ve bunların "adil kullanım", trafik limitleri ve ticari kullanım koşulları içerebileceğini hatırlat.
    *   Backend'in bu döşeme istekleriyle doğrudan bir ilgisi olmasa da, projenin genel sürdürülebilirliği için frontend'in bu politikalara uyması gerektiğini (örn: geçerli User-Agent, aşırı istekten kaçınma) ve backend geliştiricisinin bu konuda bilgi sahibi olmasının önemli olduğunu belirt.

2.  **Atıf (Attribution) Zorunluluğu:**
    *   OSM verileri kullanıldığında, harita üzerinde her zaman "© OpenStreetMap contributors" (veya benzeri, sağlayıcıya göre değişebilen) bir atıfın gösterilmesinin yasal bir zorunluluk (ODbL lisansı gereği) olduğunu kesin bir dille ifade et.
    *   Bu atıfın frontend tarafında nasıl gösterileceğine dair bir not düş.

3.  **Geocoding Servis Limitlerinin Durumu:**
    *   İlan oluştururken koordinatların kullanıcı tarafından doğrudan harita üzerinden seçilmesi nedeniyle, Nominatim gibi OSM geocoding servislerinin katı API limitlerinin **ilan kaydı sırasındaki konum belirleme işlemi için birincil bir endişe olmaktan çıktığını** tekrar teyit et. Bu, backend için bir rahatlama sağlar.
    *   Eğer ileride "bir adres yazarak yakınındaki ilanları bul" gibi bir özellik eklenirse, o zaman geocoding servislerine ve limitlerine tekrar ihtiyaç duyulacağını not et.

Bu bölüm, projenin OSM ekosistemiyle sorumlu bir şekilde etkileşimde bulunmasını sağlamak için gerekli farkındalığı yaratmalıdır."

---

## Son Söz: Harita Üzerinde Bir Araya Gelen Dostluklar

**Prompt 5.1 (Genel Değerlendirme ve Entegrasyon):**
"Bu revize edilmiş 'Harita Uygulaması' backend tasarımının, 'İlanlar Uygulaması' ve 'Etiket Uygulaması' ile nasıl bütünsel bir kullanıcı deneyimi sunacağını özetle. Özellikle, harita üzerindeki işaretçilere tıklandığında ilan detaylarına nasıl geçileceği veya harita filtrelerinin etiket/ilan filtreleriyle nasıl senkronize çalışacağı gibi etkileşimleri düşünerek, bu üç uygulamanın backend seviyesinde nasıl bir uyum içinde olacağını genel hatlarıyla belirt. Bu tasarımın, kullanıcıların aradıkları hayvan dostlarına coğrafi bir keşifle ulaşmalarını nasıl kolaylaştıracağını vurgula."