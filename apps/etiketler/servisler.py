"""
🏷️ Evcil Hayvan Platformu - Etiketler Servisleri
==============================================================================
Etiketler uygulaması için servis katmanı
==============================================================================
"""

from typing import List, Dict, Any, Optional
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from .models import Etiket


class EtiketService:
    """
    Etiketler ile ilgili işlevsel servisleri içeren sınıf.
    Bu katman, iş mantığını controller (view) katmanından ayırır.
    """
    
    @staticmethod
    def etiket_olustur_veya_getir(etiket_adi: str) -> Etiket:
        """
        Verilen ada sahip etiketi getirir, yoksa oluşturur.
        Büyük/küçük harf farkı gözetmez.
        
        Args:
            etiket_adi (str): Etiket adı
            
        Returns:
            Etiket: Bulunan veya yeni oluşturulan etiket nesnesi
        """
        etiket_adi = etiket_adi.strip()
        if not etiket_adi:
            raise ValueError(_("Etiket adı boş olamaz"))
            
        # Benzer etiket ara (büyük/küçük harf duyarsız)
        etiket = Etiket.tum_etiketler.filter(ad__iexact=etiket_adi).first()
        
        if etiket:
            # Etiket pasif ise aktifleştir
            if not etiket.aktif:
                etiket.aktif = True
                etiket.save(update_fields=['aktif'])
            return etiket
            
        # Etiket bulunamadıysa yenisini oluştur
        yeni_etiket = Etiket(
            ad=etiket_adi,
            slug=slugify(etiket_adi)
        )
        yeni_etiket.save()
        return yeni_etiket
    
    @classmethod
    @transaction.atomic
    def etiketleri_guncelle(cls, nesne, yeni_etiketler: List[str]) -> Dict[str, Any]:
        """
        Bir nesnenin (Hayvan, İlan vb.) etiketlerini günceller.
        
        Args:
            nesne: Etiketleri güncellenecek nesne (hayvan/ilan/vb)
            yeni_etiketler: Yeni etiket adları listesi
            
        Returns:
            Dict: İşlem sonucu ve istatistikler
        """
        if not hasattr(nesne, 'etiketler'):
            raise AttributeError(_("Bu nesne etiketlenemez"))
            
        # Boş string içeren veya boş olan etiketleri filtrele
        temiz_etiketler = [e.strip() for e in yeni_etiketler if e and e.strip()]
        
        # İşlem öncesi mevcut etiketler
        mevcut_etiketler = list(nesne.etiketler.values_list('ad', flat=True))
        
        # İstatistikler
        stats = {
            'eklenen': [],
            'kaldirilan': [],
            'degismedi': [],
            'toplam': len(temiz_etiketler)
        }
        
        # Tüm etiketleri kaldır ve yeni etiketleri ekle
        nesne.etiketler.clear()
        
        for etiket_adi in temiz_etiketler:
            # Aynı etiket birden fazla gelmişse sadece bir kez ekle
            if etiket_adi.lower() in [e.lower() for e in stats['eklenen']]:
                continue
                
            etiket = cls.etiket_olustur_veya_getir(etiket_adi)
            nesne.etiketler.add(etiket)
            
            if etiket_adi.lower() in [e.lower() for e in mevcut_etiketler]:
                stats['degismedi'].append(etiket_adi)
            else:
                stats['eklenen'].append(etiket_adi)
        
        # Kaldırılan etiketleri belirle  
        for eski_etiket in mevcut_etiketler:
            if eski_etiket.lower() not in [e.lower() for e in temiz_etiketler]:
                stats['kaldirilan'].append(eski_etiket)
                
        return stats
    
    @staticmethod
    def benzer_etiketler_onerisi(metin: str, limit: int = 5) -> List[str]:
        """
        Verilen metne göre etiket önerileri oluşturur
        
        Args:
            metin (str): Analiz edilecek metin
            limit (int): Döndürülecek maksimum öneri sayısı
            
        Returns:
            List[str]: Önerilen etiket adları listesi
        """
        # Daha gelişmiş öneri algoritmaları için yer tutucu
        # Burada AI destekli öneri sistemi entegre edilecek
        # Şimdilik basit anahtar kelime eşleştirmesi yapıyoruz
        
        # Metni küçük harfe çevir ve noktalama işaretlerini kaldır
        from re import sub
        temiz_metin = sub(r'[^\w\s]', ' ', metin.lower())
        kelimeler = temiz_metin.split()
        
        # Sık kullanılan kelimeleri kaldır
        stopwords = ["ve", "veya", "ile", "için", "bir", "bu", "şu", "o", "da", "de"]
        filtrelenmis_kelimeler = [k for k in kelimeler if len(k) > 3 and k not in stopwords]
        
        # Kelime frekansını hesapla
        from collections import Counter
        kelime_frekanslari = Counter(filtrelenmis_kelimeler)
        en_sik_kelimeler = [kelime for kelime, _ in kelime_frekanslari.most_common(limit)]
        
        # Veritabanında mevcut olan etiketlerle eşleştir
        mevcut_etiketler = list(Etiket.objects.values_list('ad', flat=True))
        
        oneriler = []
        for kelime in en_sik_kelimeler:
            # Tam eşleşme varsa ekle
            if kelime in [e.lower() for e in mevcut_etiketler]:
                oneriler.append(kelime)
                continue
                
            # Kısmi eşleşme ara
            for etiket in mevcut_etiketler:
                if kelime in etiket.lower() and etiket not in oneriler:
                    oneriler.append(etiket)
                    break
        
        # Öneri sayısını tamamla
        if len(oneriler) < limit:
            # Daha çok öneri eklemek için popüler etiketleri kullan
            populer_etiketler = Etiket.objects.en_populer(limit=limit)
            for etiket in populer_etiketler:
                if etiket.ad not in oneriler and len(oneriler) < limit:
                    oneriler.append(etiket.ad)
        
        return oneriler[:limit]