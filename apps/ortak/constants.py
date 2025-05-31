"""
🐾 Evcil Hayvan Platformu - Ortak Sabitler
==============================================================================
Platform genelinde kullanılacak sabit değerler
==============================================================================
"""

from django.utils.translation import gettext_lazy as _
from django.db import models # Bu satırı ekleyin

# ==============================================================================
# 🐾 EVCİL HAYVAN TÜRLERİ - Platformun can dostları
# ==============================================================================

# Hayvan türleri
class PetTypes(models.TextChoices):
    """
    🐾 Evcil Hayvan Türleri
    Platformda desteklenen temel hayvan türleri
    """
    KEDI = 'kedi', _('Kedi')
    KOPEK = 'kopek', _('Köpek')
    KUS = 'kus', _('Kuş')
    BALIK = 'balik', _('Balık')
    KEMIRGEN = 'kemirgen', _('Kemirgen')
    SURUNGEN = 'surungen', _('Sürüngen')
    DIGER = 'diger', _('Diğer') # Bu satırı ekleyin veya güncelleyin

# Hayvan boyutları
class PetSizes:
    EXTRA_SMALL = 'xs'  # 0-5 kg
    SMALL = 'sm'        # 5-10 kg
    MEDIUM = 'md'       # 10-25 kg
    LARGE = 'lg'        # 25-45 kg
    EXTRA_LARGE = 'xl'  # 45+ kg
    
    CHOICES = [
        (EXTRA_SMALL, _('Çok Küçük (0-5 kg)')),
        (SMALL, _('Küçük (5-10 kg)')),
        (MEDIUM, _('Orta (10-25 kg)')),
        (LARGE, _('Büyük (25-45 kg)')),
        (EXTRA_LARGE, _('Çok Büyük (45+ kg)')),
    ]

# Hayvan yaşları
class PetAges:
    BABY = 'baby'        # 0-6 ay
    YOUNG = 'young'      # 6 ay - 2 yaş
    ADULT = 'adult'      # 2-7 yaş
    SENIOR = 'senior'    # 7+ yaş
    
    CHOICES = [
        (BABY, _('Yavru (0-6 ay)')),
        (YOUNG, _('Genç (6 ay - 2 yaş)')),
        (ADULT, _('Yetişkin (2-7 yaş)')),
        (SENIOR, _('Yaşlı (7+ yaş)')),
    ]

# Hayvan cinsiyetleri
class PetGenders:
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'
    
    CHOICES = [
        (MALE, _('Erkek')),
        (FEMALE, _('Dişi')),
        (UNKNOWN, _('Bilinmiyor')),
    ]

# ==============================================================================
# 📋 ADOPTION RELATED CONSTANTS - Sahiplenme ile ilgili sabitler
# ==============================================================================

# İlan durumları
class ListingStatus:
    DRAFT = 'draft'
    ACTIVE = 'active'
    ADOPTED = 'adopted'
    INACTIVE = 'inactive'
    EXPIRED = 'expired'
    
    CHOICES = [
        (DRAFT, _('Taslak')),
        (ACTIVE, _('Aktif')),
        (ADOPTED, _('Sahiplenildi')),
        (INACTIVE, _('Pasif')),
        (EXPIRED, _('Süresi Dolmuş')),
    ]

# Başvuru durumları
class ApplicationStatus:
    PENDING = 'pending'
    UNDER_REVIEW = 'under_review'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    WITHDRAWN = 'withdrawn'
    
    CHOICES = [
        (PENDING, _('Beklemede')),
        (UNDER_REVIEW, _('İnceleniyor')),
        (APPROVED, _('Onaylandı')),
        (REJECTED, _('Reddedildi')),
        (WITHDRAWN, _('Geri Çekildi')),
    ]

# Sahiplenme türleri
class AdoptionTypes:
    ADOPTION = 'adoption'
    FOSTERING = 'fostering'
    TEMPORARY_CARE = 'temporary_care'
    
    CHOICES = [
        (ADOPTION, _('Kalıcı Sahiplenme')),
        (FOSTERING, _('Geçici Bakım')),
        (TEMPORARY_CARE, _('Acil Bakım')),
    ]

# ==============================================================================
# 👤 USER RELATED CONSTANTS - Kullanıcı ile ilgili sabitler
# ==============================================================================

# Kullanıcı rolleri
class UserRoles:
    USER = 'user'
    SHELTER_STAFF = 'shelter_staff'
    VETERINARY = 'veterinary'
    VOLUNTEER = 'volunteer'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    
    CHOICES = [
        (USER, _('Kullanıcı')),
        (SHELTER_STAFF, _('Barınak Çalışanı')),
        (VETERINARY, _('Veteriner')),
        (VOLUNTEER, _('Gönüllü')),
        (MODERATOR, _('Moderatör')),
        (ADMIN, _('Yönetici')),
    ]

# Kullanıcı durumları
class UserStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'
    BANNED = 'banned'
    
    CHOICES = [
        (ACTIVE, _('Aktif')),
        (INACTIVE, _('Pasif')),
        (SUSPENDED, _('Askıya Alınmış')),
        (BANNED, _('Yasaklanmış')),
    ]

# ==============================================================================
# 📱 SYSTEM CONSTANTS - Sistem sabitleri
# ==============================================================================

# Bildirim türleri
class NotificationTypes:
    APPLICATION_RECEIVED = 'application_received'
    APPLICATION_APPROVED = 'application_approved'
    APPLICATION_REJECTED = 'application_rejected'
    NEW_MESSAGE = 'new_message'
    LISTING_EXPIRED = 'listing_expired'
    SYSTEM_ANNOUNCEMENT = 'system_announcement'
    
    CHOICES = [
        (APPLICATION_RECEIVED, _('Başvuru Alındı')),
        (APPLICATION_APPROVED, _('Başvuru Onaylandı')),
        (APPLICATION_REJECTED, _('Başvuru Reddedildi')),
        (NEW_MESSAGE, _('Yeni Mesaj')),
        (LISTING_EXPIRED, _('İlan Süresi Doldu')),
        (SYSTEM_ANNOUNCEMENT, _('Sistem Duyurusu')),
    ]

# Öncelik seviyeleri
class PriorityLevels:
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    URGENT = 'urgent'
    
    CHOICES = [
        (LOW, _('Düşük')),
        (NORMAL, _('Normal')),
        (HIGH, _('Yüksek')),
        (URGENT, _('Acil')),
    ]

# ==============================================================================
# 🔧 CONFIGURATION CONSTANTS - Konfigürasyon sabitleri
# ==============================================================================

# Dosya boyutu limitleri (bytes)
class FileSizeLimits:
    PROFILE_IMAGE = 2 * 1024 * 1024    # 2MB
    PET_IMAGE = 5 * 1024 * 1024        # 5MB
    DOCUMENT = 10 * 1024 * 1024        # 10MB

# Sayfa boyutları
class PageSizes:
    DEFAULT = 20
    SMALL = 10
    LARGE = 50
    MAX = 100

# Rate limiting
class RateLimits:
    LOGIN_ATTEMPTS = 5
    MESSAGE_PER_HOUR = 100
    APPLICATION_PER_DAY = 3
    LISTING_PER_DAY = 5

# ==============================================================================
# 🌍 REGIONAL CONSTANTS - Bölgesel sabitler
# ==============================================================================

# Türkiye şehirleri (öncelik verilenler)
TURKISH_CITIES = [
    ('istanbul', _('İstanbul')),
    ('ankara', _('Ankara')),
    ('izmir', _('İzmir')),
    ('bursa', _('Bursa')),
    ('antalya', _('Antalya')),
    ('konya', _('Konya')),
    ('adana', _('Adana')),
    ('gaziantep', _('Gaziantep')),
    ('other', _('Diğer')),
]

# Dil kodları
LANGUAGE_CODES = [
    ('tr', _('Türkçe')),
    ('en', _('English')),
]

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu sabitler, platform genelinde tutarlılık sağlar ve
# magic number kullanımını önler.
# 🐾 Her sabit, daha temiz kod için!
