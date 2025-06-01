"""
🐾 Evcil Hayvan Platformu - Hayvanlar Sinyalleri
==============================================================================
Hayvan modellerindeki değişiklikleri izleyen ve tepki veren sinyal işleyicileri
==============================================================================
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction

from .models import KopekIrk, Hayvan

@receiver(post_save, sender=KopekIrk)
def kopek_irk_degisiklik_izleyici(sender, instance, created, **kwargs):
    """Köpek ırkı değişikliklerini izle ve gerekli işlemleri yap"""
    # Kategorileri otomatik güncelle (save metodunda çağrıldığı için burada çağrılmayabilir,
    # ancak başka bir yerden güncellendiğinde de çalışması için ekliyoruz)
    if instance.aktif and instance.populer:
        transaction.on_commit(lambda: instance.kategori_ile_senkronize_et())


@receiver(post_delete, sender=KopekIrk)
def kopek_irk_silme_izleyici(sender, instance, **kwargs):
    """Köpek ırkı silindiğinde ilgili kategoriyi pasife çek"""
    try:
        from apps.kategoriler.models import Kategori
        
        # Köpek kategorisini bul
        kopekler_kategori = Kategori.objects.filter(
            ad__iexact='Köpekler',
            parent__isnull=True
        ).first()
        
        if kopekler_kategori:
            # Bu ırk için alt kategori var mı?
            alt_kategori = Kategori.objects.filter(
                parent=kopekler_kategori,
                ad__iexact=instance.ad
            ).first()
            
            # Varsa pasife çek
            if alt_kategori:
                alt_kategori.aktif = False
                alt_kategori.save(update_fields=['aktif'])
                
    except Exception as e:
        import logging
        logging.warning(f"Köpek ırkı silindiğinde kategori güncellemesi sırasında hata: {e}")
