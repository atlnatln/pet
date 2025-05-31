"""
🐾 Kullanıcılar İş Mantığı Servisleri
==============================================================================
Kullanıcı işlemlerinin merkezi iş mantığı - Her kullanıcının hikayesi burada yaşar
==============================================================================
"""

import uuid
import secrets
from typing import Dict, Optional, List
from django.db import transaction
from django.core.cache import cache
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, KullaniciProfil
from apps.ortak.exceptions import PlatformBaseException


class UserService:
    """
    Kullanıcı işlemleri için merkezi servis sınıfı
    """
    
    @staticmethod
    @transaction.atomic
    def kullanici_olustur(user_data: Dict) -> CustomUser:
        """
        Yeni kullanıcı oluştur ve hoş geldin sürecini başlat
        """
        try:
            # E-posta doğrulama token oluştur
            verification_token = secrets.token_urlsafe(32)
            user_data['email_dogrulama_token'] = verification_token
            
            # Kullanıcı oluştur
            user = CustomUser.objects.create_user(**user_data)
            
            # Profil detayı oluştur
            KullaniciProfil.objects.create(kullanici=user)
            
            # Hoş geldin e-postası gönder
            EmailService.send_welcome_email(user)
            
            # E-posta doğrulama gönder
            EmailService.send_verification_email(user)
            
            return user
            
        except Exception as e:
            raise PlatformBaseException(
                message=_("Kullanıcı oluşturulamadı: {error}").format(error=str(e)),
                code="USER_CREATION_ERROR"
            )
    
    @staticmethod
    def email_dogrula(token: str) -> bool:
        """
        E-posta doğrulama token ile doğrulama yap
        """
        try:
            user = CustomUser.objects.get(
                email_dogrulama_token=token,
                email_dogrulanmis=False
            )
            
            user.email_dogrula()
            
            # Hoş geldin tamamlama e-postası
            EmailService.send_verification_complete_email(user)
            
            return True
            
        except CustomUser.DoesNotExist:
            raise PlatformBaseException(
                message=_("Geçersiz veya süresi dolmuş doğrulama token'ı"),
                code="INVALID_VERIFICATION_TOKEN"
            )
    
    @staticmethod
    def sifre_sifirlama_talebi(email: str) -> bool:
        """
        Şifre sıfırlama talebi oluştur
        """
        try:
            user = CustomUser.objects.get(email__iexact=email.lower())
            
            # Sıfırlama token oluştur
            reset_token = secrets.token_urlsafe(32)
            
            # Cache'e kaydet (1 saat geçerli)
            cache_key = f"password_reset:{reset_token}"
            cache.set(cache_key, user.id, 3600)
            
            # E-posta gönder
            EmailService.send_password_reset_email(user, reset_token)
            
            return True
            
        except CustomUser.DoesNotExist:
            # Güvenlik için gerçek hatayı verme
            return True
    
    @staticmethod
    @transaction.atomic
    def profil_guncelle(user_id: str, update_data: Dict) -> CustomUser:
        """
        Kullanıcı profil güncelleme
        """
        try:
            user = CustomUser.objects.get(id=user_id)
            
            # Güncelleme verilerini uygula
            for field, value in update_data.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            
            user.full_clean()
            user.save()
            
            # Cache temizle
            UserService._clear_user_cache(user.id)
            
            return user
            
        except CustomUser.DoesNotExist:
            raise PlatformBaseException(
                message=_("Kullanıcı bulunamadı"),
                code="USER_NOT_FOUND"
            )
    
    @staticmethod
    def kullanici_istatistikleri() -> Dict:
        """
        Platform kullanıcı istatistiklerini hesapla
        """
        cache_key = "platform_user_stats"
        stats = cache.get(cache_key)
        
        if stats is None:
            from django.db.models import Count
            
            stats = {
                'toplam_kullanici': CustomUser.objects.count(),
                'aktif_kullanici': CustomUser.objects.aktif_kullanicilar().count(),
                'dogrulanmis_kullanici': CustomUser.objects.filter(email_dogrulanmis=True).count(),
                'sahiplendiren_sayisi': CustomUser.objects.sahiplendirenler().count(),
                'sahiplenmek_isteyen_sayisi': CustomUser.objects.sahiplenmek_isteyenler().count(),
                'sehir_dagilimi': dict(
                    CustomUser.objects.aktif_kullanicilar()
                    .exclude(sehir='')
                    .values('sehir')
                    .annotate(count=Count('id'))
                    .values_list('sehir', 'count')[:10]
                ),
                'bugun_kayit': CustomUser.objects.filter(
                    uyelik_tarihi__date=timezone.now().date()
                ).count(),
                'bu_hafta_kayit': CustomUser.objects.filter(
                    uyelik_tarihi__gte=timezone.now() - timezone.timedelta(days=7)
                ).count()
            }
            
            cache.set(cache_key, stats, 1800)  # 30 dakika
        
        return stats
    
    @staticmethod
    def kullanici_arama(query: str, filters: Dict = None) -> List[CustomUser]:
        """
        Gelişmiş kullanıcı arama
        """
        if not query or len(query) < 2:
            return []
        
        users = CustomUser.objects.arama_yap(query)
        
        # Ek filtreler uygula
        if filters:
            if filters.get('sehir'):
                users = users.filter(sehir=filters['sehir'])
            
            if filters.get('rol'):
                users = users.filter(rol=filters['rol'])
            
            if filters.get('sahiplendiren_mi') is not None:
                users = users.filter(sahiplendiren_mi=filters['sahiplendiren_mi'])
        
        return users[:20]  # Maksimum 20 sonuç
    
    @staticmethod
    def _clear_user_cache(user_id: str):
        """
        Kullanıcı ile ilgili cache'leri temizle
        """
        cache_keys = [
            f"user_profile:{user_id}",
            "platform_user_stats"
        ]
        
        for key in cache_keys:
            cache.delete(key)


class EmailService:
    """
    E-posta servisleri
    """
    
    @staticmethod
    def send_welcome_email(user: CustomUser):
        """
        Hoş geldin e-postası gönder
        """
        try:
            subject = "🐾 Hoş geldin! Sevgi köprüsü kurmaya başlıyoruz"
            
            context = {
                'user': user,
                'platform_name': 'Evcil Hayvan Platformu',
                'verification_url': f"{settings.FRONTEND_URL}/verify-email/{user.email_dogrulama_token}"
            }
            
            html_message = render_to_string('emails/welcome.html', context)
            plain_message = render_to_string('emails/welcome.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True
            )
            
        except Exception as e:
            # Log the error but don't break the flow
            print(f"Welcome email error for {user.email}: {e}")
    
    @staticmethod
    def send_verification_email(user: CustomUser):
        """
        E-posta doğrulama e-postası gönder
        """
        try:
            subject = "📧 E-posta adresinizi doğrulayın"
            
            context = {
                'user': user,
                'verification_url': f"{settings.FRONTEND_URL}/verify-email/{user.email_dogrulama_token}",
                'token': user.email_dogrulama_token
            }
            
            html_message = render_to_string('emails/email_verification.html', context)
            plain_message = render_to_string('emails/email_verification.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True
            )
            
        except Exception as e:
            print(f"Verification email error for {user.email}: {e}")
    
    @staticmethod
    def send_verification_complete_email(user: CustomUser):
        """
        E-posta doğrulama tamamlama e-postası
        """
        try:
            subject = "🎉 E-posta doğrulandı! Maceraya başlayalım"
            
            context = {
                'user': user,
                'dashboard_url': f"{settings.FRONTEND_URL}/dashboard",
                'profile_url': f"{settings.FRONTEND_URL}/profile"
            }
            
            html_message = render_to_string('emails/verification_complete.html', context)
            plain_message = render_to_string('emails/verification_complete.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True
            )
            
        except Exception as e:
            print(f"Verification complete email error for {user.email}: {e}")
    
    @staticmethod
    def send_password_reset_email(user: CustomUser, reset_token: str):
        """
        Şifre sıfırlama e-postası gönder
        """
        try:
            subject = "🔐 Şifre sıfırlama talebi"
            
            context = {
                'user': user,
                'reset_url': f"{settings.FRONTEND_URL}/reset-password/{reset_token}",
                'token': reset_token
            }
            
            html_message = render_to_string('emails/password_reset.html', context)
            plain_message = render_to_string('emails/password_reset.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True
            )
            
        except Exception as e:
            print(f"Password reset email error for {user.email}: {e}")


class UserAnalyticsService:
    """
    Kullanıcı analitik servisleri
    """
    
    @staticmethod
    def get_user_activity_stats(user: CustomUser) -> Dict:
        """
        Kullanıcı aktivite istatistikleri
        """
        # Bu veriler hayvan ve ilan sistemleri eklendikten sonra doldurulacak
        stats = {
            'profil_tamamlama_yuzdesi': user.profil_tamamlama_yuzdesi,
            'uyelik_suresi_gun': (timezone.now() - user.uyelik_tarihi).days,
            'son_giris': user.son_giris_tarihi,
            'giris_sayisi': user.giris_sayisi,
            # 'ilan_sayisi': 0,  # İlan sistemi eklendiğinde aktif edilecek
            # 'basvuru_sayisi': 0,  # Başvuru sistemi eklendiğinde aktif edilecek
            # 'mesaj_sayisi': 0,  # Mesajlaşma sistemi eklendiğinde aktif edilecek
        }
        
        return stats
    
    @staticmethod
    def get_platform_growth_stats() -> Dict:
        """
        Platform büyüme istatistikleri
        """
        from django.db.models import Count
        from django.utils import timezone
        
        # Son 30 günün verilerini al
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        
        daily_registrations = []
        for i in range(30):
            date = thirty_days_ago + timezone.timedelta(days=i)
            count = CustomUser.objects.filter(
                uyelik_tarihi__date=date.date()
            ).count()
            daily_registrations.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
        
        return {
            'daily_registrations': daily_registrations,
            'total_growth': sum(day['count'] for day in daily_registrations)
        }

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu servisler, kullanıcı sisteminin tüm iş mantığını yönetir.
# E-posta akışları, güvenlik kontrolü ve analitik bir arada.
# 🐾 Her servis metodu, kullanıcı deneyimini iyileştirmek için tasarlandı!
