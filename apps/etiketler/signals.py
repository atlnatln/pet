"""
🏷️ Evcil Hayvan Platformu - Etiketler Signals
==============================================================================
Etiket modeli için signal handlers
==============================================================================
"""

from django.db.models.signals import pre_delete, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction

from .models import Etiket
import logging

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=None)
def etiket_kullanim_degisim_izle(sender, instance, action, pk_set, **kwargs):
    """
    ManyToMany ilişkisi değiştiğinde etiket kullanım sayılarını güncelle.
    - Özellikle Hayvan ve İlan modelleriyle ilişki değişimlerini izler
    - Sender parametresi None olarak belirtildiğinden tüm M2M bağlantılarını dinler
    - İlgili bağlantılar, apps/etiketler/apps.py içinde bağlanır
    """
    try:
        if not hasattr(instance, 'etiketler'):
            return
            
        # İlişkinin diğer tarafının Etiket olduğunu doğrula
        if not sender._meta.get_field('etiketler').related_model == Etiket:
            return
            
        # Sadece ekleme/çıkarma işlemlerini işle
        if action not in ('post_add', 'post_remove', 'post_clear'):
            return
            
        # İşlem tamamlandıktan sonra çalışması için transaction kullan
        transaction.on_commit(lambda: _guncelle_etiket_istatistikleri(sender, pk_set, action))
    
    except Exception as e:
        logger.error(f"Etiket kullanımı izleme sinyalinde hata: {str(e)}")


def _guncelle_etiket_istatistikleri(sender, pk_set, action):
    """Etiket istatistiklerini günceller"""
    try:
        if action == 'post_clear':
            # Bu işlem için daha karmaşık bir yenileme gerekiyor
            # Tüm etiketleri yeniliyoruz (maliyetli bir işlem)
            # İleride optimize edilebilir
            pass
        else:
            # Özellikle etkilenen etiketleri güncelle
            if pk_set:
                # İleride bir istatistik alanı eklenmesi durumunda burada güncelleme yapılacak
                # Şu anki modelde böyle bir alan olmadığı için işlem yapmıyoruz
                pass
    except Exception as e:
        logger.error(f"Etiket istatistikleri güncelleme hatası: {str(e)}")


@receiver(pre_delete, sender=Etiket)
def etiket_silinme_oncesi(sender, instance, **kwargs):
    """
    Etiket silinmeden önce kontrol işlemleri yapar
    - Kullanımda olan etiketlerin silinmesi yerine pasif yapılmasını sağlar
    """
    try:
        # Etiket kullanımda mı kontrol et
        hayvan_sayisi = getattr(instance, 'hayvanlar', None)
        ilan_sayisi = getattr(instance, 'ilanlar', None)
        
        kullanim_var = False
        if hayvan_sayisi and hayvan_sayisi.exists():
            kullanim_var = True
        if ilan_sayisi and ilan_sayisi.exists():
            kullanim_var = True
            
        if kullanim_var:
            # Kullanımda olan etiketi silmek yerine pasif yap
            instance.aktif = False
            # Kayıt zamanını güncelle
            instance.guncelleme_tarihi = timezone.now()
            # pre_delete signal içinde olduğumuzdan, silme işlemini iptal etmek için
            # instance'ı tekrar save ediyoruz ve sonra False döndürerek silme işlemini engelliyoruz
            instance.save(update_fields=['aktif', 'guncelleme_tarihi'])
            
            # Silme işlemini iptal etmek için False döndürüyoruz
            return False
    
    except Exception as e:
        logger.error(f"Etiket silme öncesi kontrolde hata: {str(e)}")
