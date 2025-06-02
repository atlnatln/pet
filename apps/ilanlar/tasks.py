"""
📢 İlanlar Asenkron Görevleri
==============================================================================
İlan sistemi için background task'ler
==============================================================================
"""

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def ilan_suresini_guncelle():
    """
    İlanların sürelerini kontrol et ve gerekirse durumunu güncelle
    Günlük çalıştırılmalı
    """
    from .models import Ilan
    
    # Süresi dolan ilanları pasif yap
    now = timezone.now()
    suresi_dolan_ilanlar = Ilan.objects.filter(
        durum='aktif',
        bitis_tarihi__lt=now
    )
    
    updated_count = suresi_dolan_ilanlar.update(durum='suresi_doldu')
    
    logger.info(f"{updated_count} ilanın süresi doldu ve pasif edildi")
    return f"Güncellenen ilan sayısı: {updated_count}"


@shared_task
def ilan_veren_bilgilendir(ilan_id):
    """
    İlan sahibine bilgi maili gönder
    """
    from .models import Ilan
    
    try:
        ilan = Ilan.objects.get(id=ilan_id)
        
        subject = f"İlanınız '{ilan.baslik}' yayında"
        message = f"""
        Merhaba {ilan.ilan_veren_adi},
        
        '{ilan.baslik}' başlıklı ilanınız başarıyla yayına alınmıştır.
        
        İlan linki: https://petplatform.com/ilanlar/{ilan.id}/
        
        İyi günler!
        Pet Platform Ekibi
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [ilan.ilan_veren_email],
            fail_silently=False,
        )
        
        logger.info(f"İlan sahibine bilgilendirme maili gönderildi: {ilan.id}")
        return f"Mail gönderildi: {ilan.ilan_veren_email}"
        
    except Ilan.DoesNotExist:
        logger.error(f"İlan bulunamadı: {ilan_id}")
        return f"İlan bulunamadı: {ilan_id}"
    except Exception as e:
        logger.error(f"Mail gönderimi başarısız: {str(e)}")
        return f"Mail gönderimi başarısız: {str(e)}"


@shared_task
def basvuru_bilgilendir(basvuru_id):
    """
    Başvuru sahibine onay maili gönder
    """
    from .models import IlanBasvuru
    
    try:
        basvuru = IlanBasvuru.objects.get(id=basvuru_id)
        
        subject = f"Başvurunuz alındı - {basvuru.ilan.baslik}"
        message = f"""
        Merhaba {basvuru.basvuran_adi},
        
        '{basvuru.ilan.baslik}' ilanına başvurunuz alınmıştır.
        
        Mesajınız: {basvuru.mesaj}
        
        İlan sahibi en kısa sürede sizinle iletişime geçecektir.
        
        Başvuru durumu: {basvuru.get_durum_display()}
        
        İyi günler!
        Pet Platform Ekibi
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [basvuru.basvuran_email],
            fail_silently=False,
        )
        
        logger.info(f"Başvuran bilgilendirildi: {basvuru.id}")
        return f"Mail gönderildi: {basvuru.basvuran_email}"
        
    except Exception as e:
        logger.error(f"Başvuru maili başarısız: {str(e)}")
        return f"Mail başarısız: {str(e)}"


@shared_task
def ilan_istatistiklerini_guncelle():
    """
    İlan istatistiklerini güncelle (günlük)
    """
    from .models import Ilan
    from django.db.models import Count
    
    # Kategorilere göre ilan sayılarını güncelle
    from apps.kategoriler.models import Kategori
    
    kategoriler = Kategori.objects.all()
    for kategori in kategoriler:
        ilan_sayisi = Ilan.objects.filter(
            hayvan__kategori=kategori,
            durum='aktif'
        ).count()
        
        kategori.kullanim_sayisi = ilan_sayisi
        kategori.save(update_fields=['kullanim_sayisi'])
    
    logger.info("İlan istatistikleri güncellendi")
    return "İstatistikler güncellendi"


@shared_task
def geciken_ilanlar_hatirlatma():
    """
    30 gün önce eklenen aktif ilanlar için hatırlatma gönder
    """
    from .models import Ilan
    
    otuz_gun_once = timezone.now() - timedelta(days=30)
    geciken_ilanlar = Ilan.objects.filter(
        durum='aktif',
        created_at__lte=otuz_gun_once
    )
    
    for ilan in geciken_ilanlar:
        subject = f"İlanınız hala aktif - {ilan.baslik}"
        message = f"""
        Merhaba {ilan.ilan_veren_adi},
        
        '{ilan.baslik}' ilanınız 30 gündür yayında.
        
        Hayvanınız sahiplenildiyse lütfen ilanı kapatmayı unutmayın.
        
        İlan yönetimi: https://petplatform.com/ilanlarim/
        
        Pet Platform Ekibi
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [ilan.ilan_veren_email],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f"Hatırlatma maili gönderilemedi: {ilan.id} - {str(e)}")
    
    logger.info(f"{geciken_ilanlar.count()} ilan için hatırlatma gönderildi")
    return f"Hatırlatma sayısı: {geciken_ilanlar.count()}"
