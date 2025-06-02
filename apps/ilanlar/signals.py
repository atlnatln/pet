"""
📢 İlanlar Sinyalleri
==============================================================================
İlan modeli değişikliklerini izleyen signal handler'lar
==============================================================================
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from .models import Ilan, IlanBasvuru


@receiver(post_save, sender=Ilan)
def ilan_kayit_sonrasi(sender, instance, created, **kwargs):
    """İlan kaydedildiğinde çalışır"""
    
    if created:
        # Yeni ilan oluşturuldu
        print(f"✅ Yeni ilan oluşturuldu: {instance.baslik}")
        
        # Async task tetikle (eğer Celery varsa)
        try:
            from .tasks import ilan_veren_bilgilendir
            transaction.on_commit(
                lambda: ilan_veren_bilgilendir.delay(instance.id)
            )
        except ImportError:
            # Celery yoksa normal işlem
            pass
        
        # Kategori kullanım sayısını artır
        if instance.hayvan and instance.hayvan.kategori:
            kategori = instance.hayvan.kategori
            kategori.kullanim_sayisi += 1
            kategori.save(update_fields=['kullanim_sayisi'])
    
    else:
        # Mevcut ilan güncellendi
        print(f"🔄 İlan güncellendi: {instance.baslik}")


@receiver(post_delete, sender=Ilan)
def ilan_silme_sonrasi(sender, instance, **kwargs):
    """İlan silindiğinde çalışır"""
    
    print(f"🗑️ İlan silindi: {instance.baslik}")
    
    # Kategori kullanım sayısını azalt
    if instance.hayvan and instance.hayvan.kategori:
        kategori = instance.hayvan.kategori
        if kategori.kullanim_sayisi > 0:
            kategori.kullanim_sayisi -= 1
            kategori.save(update_fields=['kullanim_sayisi'])


@receiver(pre_save, sender=Ilan)
def ilan_kayit_oncesi(sender, instance, **kwargs):
    """İlan kaydedilmeden önce çalışır"""
    
    # Durum değişikliklerini kontrol et
    if instance.pk:
        try:
            eski_ilan = Ilan.objects.get(pk=instance.pk)
            
            # Aktif durumdan pasife geçiyorsa
            if eski_ilan.durum == 'aktif' and instance.durum != 'aktif':
                print(f"📋 İlan pasif edildi: {instance.baslik}")
            
            # Pasiften aktife geçiyorsa
            elif eski_ilan.durum != 'aktif' and instance.durum == 'aktif':
                print(f"📢 İlan aktif edildi: {instance.baslik}")
                
        except Ilan.DoesNotExist:
            pass


@receiver(post_save, sender=IlanBasvuru)
def basvuru_kayit_sonrasi(sender, instance, created, **kwargs):
    """Başvuru kaydedildiğinde çalışır"""
    
    if created:
        print(f"📩 Yeni başvuru: {instance.ilan.baslik} - {instance.basvuran_adi}")
        
        # Başvuran bilgilendir
        try:
            from .tasks import basvuru_bilgilendir
            transaction.on_commit(
                lambda: basvuru_bilgilendir.delay(instance.id)
            )
        except ImportError:
            pass
        
        # İlan sahibine de bildirim gönderilebilir
        # TODO: İlan sahibi bilgilendirme sistemi


@receiver(post_save, sender=Ilan)
def ilan_durum_degisiklik_izleyici(sender, instance, created, **kwargs):
    """İlan durumu değiştiğinde otomatik işlemler"""
    
    if created and instance.durum == 'aktif':
        # Yeni ilan aktif olarak oluşturulduysa yayınlanma tarihini set et
        if not instance.yayinlanma_tarihi:
            Ilan.objects.filter(id=instance.id).update(
                yayinlanma_tarihi=timezone.now()
            )
