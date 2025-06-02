"""
🐾 Evcil Hayvan Platformu - Ortak Permission Sınıfları
==============================================================================
Platform genelinde kullanılacak özel yetkilendirme sınıfları.
Hayvan sahiplenme süreçleri için güvenlik odaklı tasarlanmıştır.

Her permission, platform güvenliği ve kullanıcı hakları için optimize edildi.
==============================================================================
"""

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# ==============================================================================
# 👤 SAHİPLİK KONTROL PERMİSSİONLARI
# ==============================================================================

class IsOwnerOrReadOnly(BasePermission):
    """
    Sadece sahip düzenleyebilir, diğerleri sadece okuyabilir
    Hayvan ilanları ve profilleri için kritik
    """
    
    message = "Bu işlemi sadece içeriğin sahibi yapabilir."
    
    def has_object_permission(self, request, view, obj):
        # Read permissions herkese açık
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions sadece sahibine
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False

class IsOwner(BasePermission):
    """
    Sadece sahip erişebilir (okuma dahil)
    Özel mesajlar ve kişisel bilgiler için
    """
    
    message = "Bu içeriğe sadece sahibi erişebilir."
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False

# ==============================================================================
# ✅ DOĞRULANMIŞ KULLANICI PERMİSSİONLARI
# ==============================================================================

class IsVerifiedUser(BasePermission):
    """
    Sadece doğrulanmış kullanıcılar işlem yapabilir
    Güvenli sahiplenme süreci için kritik
    """
    
    message = "Bu işlemi yapmak için hesabınızı doğrulamanız gerekiyor."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Kullanıcı modelinde email_verified alanı olup olmadığını kontrol et
        if hasattr(request.user, 'email_verified'):
            return request.user.email_verified
        
        # Varsayılan olarak authenticated user'lar verified kabul edilir
        return True

class IsPhoneVerified(BasePermission):
    """
    Telefon numarası doğrulanmış kullanıcılar
    Sahiplenme başvuruları için gerekli
    """
    
    message = "Bu işlemi yapmak için telefon numaranızı doğrulamanız gerekiyor."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if hasattr(request.user, 'phone_verified'):
            return request.user.phone_verified
        
        return True

# ==============================================================================
# 🛡️ MODERATÖR PERMİSSİONLARI
# ==============================================================================

class IsModerator(BasePermission):
    """
    Platform moderatörleri için özel yetkiler
    İçerik onayı ve raporlama sistemi için
    """
    
    message = "Bu işlemi sadece moderatörler yapabilir."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Staff ya da moderator grubu kontrolü
        if request.user.is_staff:
            return True
        
        # Moderator grubu kontrolü
        if hasattr(request.user, 'groups'):
            return request.user.groups.filter(name='moderators').exists()
        
        return False

class IsModeratorOrOwner(BasePermission):
    """
    Moderatör veya sahip işlem yapabilir
    İçerik yönetimi için esnek yetkilendirme
    """
    
    message = "Bu işlemi sadece moderatörler veya içerik sahibi yapabilir."
    
    def has_object_permission(self, request, view, obj):
        # Moderatör kontrolü
        if request.user.is_staff:
            return True
        
        if hasattr(request.user, 'groups'):
            if request.user.groups.filter(name='moderators').exists():
                return True
        
        # Sahiplik kontrolü
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False

# ==============================================================================
# 📅 ZAMAN BAZLI PERMİSSİONLAR
# ==============================================================================

class IsRecentUser(BasePermission):
    """
    Yeni kayıt olan kullanıcılar için sınırlamalar
    Spam ve kötüye kullanım önleme
    """
    
    message = "Hesabınız çok yeni. Lütfen 24 saat bekleyin."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Güvenli method'lar serbest
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 24 saat kontrolü
        if hasattr(request.user, 'date_joined'):
            join_date = request.user.date_joined
            if timezone.now() - join_date < timedelta(hours=24):
                return False
        
        return True

class CanCreateAdoption(BasePermission):
    """
    Sahiplenme ilanı oluşturma yetkisi
    Kullanıcı başına limit ve zaman kontrolü
    """
    
    message = "Sahiplenme ilanı oluşturmak için yetkiniz yok."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Güvenli method'lar serbest
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Doğrulanmış kullanıcı kontrolü
        if hasattr(request.user, 'email_verified'):
            if not request.user.email_verified:
                return False
        
        # Aktif ilan sayısı kontrolü (max 5)
        if hasattr(request.user, 'ilan_set'):
            active_ads = request.user.ilan_set.filter(
                status='published',
                deleted_at__isnull=True
            ).count()
            
            if active_ads >= 5:
                self.message = "En fazla 5 aktif ilanınız olabilir."
                return False
        
        return True

# ==============================================================================
# 💬 MESAJLAŞMA PERMİSSİONLARI
# ==============================================================================

class CanSendMessage(BasePermission):
    """
    Mesaj gönderme yetkisi
    Spam önleme ve güvenlik için
    """
    
    message = "Mesaj gönderme yetkiniz yok."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Doğrulanmış kullanıcı kontrolü
        if hasattr(request.user, 'email_verified'):
            if not request.user.email_verified:
                self.message = "Mesaj göndermek için email adresinizi doğrulayın."
                return False
        
        # Günlük mesaj limiti (50 mesaj)
        today = timezone.now().date()
        if hasattr(request.user, 'sent_messages'):
            daily_messages = request.user.sent_messages.filter(
                created_at__date=today
            ).count()
            
            if daily_messages >= 50:
                self.message = "Günlük mesaj limitinizi aştınız."
                return False
        
        return True

class CanReceiveMessage(BasePermission):
    """
    Mesaj alma yetkisi kontrolü
    Kullanıcının mesajlarını kapatmış olabilir
    """
    
    def has_object_permission(self, request, view, obj):
        # Obj = mesaj alıcısı
        if hasattr(obj, 'accepts_messages'):
            return obj.accepts_messages
        
        return True

# ==============================================================================
# 🚨 RAPOR VE ŞİKAYET PERMİSSİONLARI
# ==============================================================================

class CanReportContent(BasePermission):
    """
    İçerik rapor etme yetkisi
    Kötüye kullanım önleme
    """
    
    message = "İçerik rapor etme yetkiniz yok."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Kendi içeriğini rapor edemez
        if hasattr(view, 'get_object'):
            obj = view.get_object()
            if hasattr(obj, 'owner') and obj.owner == request.user:
                self.message = "Kendi içeriğinizi rapor edemezsiniz."
                return False
        
        # Günlük rapor limiti (10 rapor)
        today = timezone.now().date()
        if hasattr(request.user, 'reports'):
            daily_reports = request.user.reports.filter(
                created_at__date=today
            ).count()
            
            if daily_reports >= 10:
                self.message = "Günlük rapor limitinizi aştınız."
                return False
        
        return True

# ==============================================================================
# 🏆 BAŞVURU PERMİSSİONLARI
# ==============================================================================

class CanApplyForAdoption(BasePermission):
    """
    Sahiplenme başvurusu yapma yetkisi
    Kapsamlı kontrollerle güvenli sahiplenme
    """
    
    message = "Sahiplenme başvurusu yapma yetkiniz yok."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Email doğrulama kontrolü
        if hasattr(request.user, 'email_verified'):
            if not request.user.email_verified:
                self.message = "Başvuru yapmak için email adresinizi doğrulayın."
                return False
        
        # Telefon doğrulama kontrolü
        if hasattr(request.user, 'phone_verified'):
            if not request.user.phone_verified:
                self.message = "Başvuru yapmak için telefon numaranızı doğrulayın."
                return False
        
        # Profil tamamlama kontrolü
        if hasattr(request.user, 'profile_completed'):
            if not request.user.profile_completed:
                self.message = "Başvuru yapmak için profilinizi tamamlayın."
                return False
        
        # Aktif başvuru sayısı kontrolü (max 3)
        if hasattr(request.user, 'applications'):
            active_applications = request.user.applications.filter(
                status__in=['pending', 'under_review']
            ).count()
            
            if active_applications >= 3:
                self.message = "En fazla 3 aktif başvurunuz olabilir."
                return False
        
        return True

    def has_object_permission(self, request, view, obj):
        # Kendi ilanına başvuru yapamaz
        if hasattr(obj, 'owner') and obj.owner == request.user:
            self.message = "Kendi ilanınıza başvuru yapamazsınız."
            return False
        
        # Daha önce bu ilana başvuru yapmış mı?
        if hasattr(request.user, 'applications'):
            if request.user.applications.filter(listing=obj).exists():
                self.message = "Bu ilana daha önce başvuru yaptınız."
                return False
        
        return True

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Her permission sınıfı, platform güvenliği ve kullanıcı deneyimi 
# için özenle tasarlandı. Hayvan refahı ve güvenli sahiplenme süreçleri
# her zaman önceliğimizdir.
# 🐾 Her yetki kontrolü, güvenli bir sahiplenme için! 💝

# ==============================================================================
# 🐾 Ortak İzin Sınıfları
# ==============================================================================
# Platform genelindeki izin kontrolleri
# ==============================================================================

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Sadece admin düzenleyebilir, diğerleri okuyabilir
    """
    
    def has_permission(self, request, view):
        # Okuma izinleri herkes için
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Yazma izinleri sadece admin için
        return request.user and request.user.is_staff


class IsActiveUser(permissions.BasePermission):
    """
    Sadece aktif kullanıcılar
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_active
