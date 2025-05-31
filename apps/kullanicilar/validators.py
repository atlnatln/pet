"""
🐾 Kullanıcı Validators
==============================================================================
Kullanıcı verilerinin güvenli ve geçerli olmasını sağlayan validatörler
==============================================================================
"""

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator


def validate_turkish_phone(value):
    """
    Türkiye telefon numarası validasyonu
    """
    if not value:
        return
    
    # Sadece rakamları al
    digits = re.sub(r'\D', '', value)
    
    # Geçerli formatlar kontrolü
    valid_patterns = [
        r'^5[0-9]{9}$',      # 5XXXXXXXXX
        r'^05[0-9]{9}$',     # 05XXXXXXXXX  
        r'^905[0-9]{9}$',    # 905XXXXXXXXX
        r'^\+905[0-9]{9}$'   # +905XXXXXXXXX
    ]
    
    if not any(re.match(pattern, value) for pattern in valid_patterns):
        raise ValidationError(
            _('Geçerli bir Türkiye telefon numarası giriniz. Örnek: 5551234567')
        )


def validate_profile_image(image):
    """
    Profil resmi validasyonu
    """
    if not image:
        return
    
    # Dosya boyutu kontrolü (5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError(
            _('Profil resmi en fazla 5MB olabilir.')
        )
    
    # Dosya türü kontrolü
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    if hasattr(image, 'content_type') and image.content_type not in allowed_types:
        raise ValidationError(
            _('Sadece JPEG, PNG ve WebP formatları desteklenir.')
        )
    
    # Dosya uzantısı kontrolü
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if hasattr(image, 'name'):
        import os
        ext = os.path.splitext(image.name.lower())[1]
        if ext not in allowed_extensions:
            raise ValidationError(
                _('Desteklenen dosya uzantıları: .jpg, .jpeg, .png, .webp')
            )


def validate_biography(value):
    """
    Biyografi validasyonu
    """
    if not value:
        return
    
    # Minimum uzunluk
    if len(value.strip()) < 10:
        raise ValidationError(
            _('Biyografi en az 10 karakter olmalıdır.')
        )
    
    # Maksimum uzunluk
    if len(value) > 500:
        raise ValidationError(
            _('Biyografi en fazla 500 karakter olabilir.')
        )
    
    # Yasak kelimeler kontrolü
    forbidden_words = [
        'satılık', 'para', 'ücret', 'bedel', 'fiyat',
        'satın', 'alın', 'para karşılığı'
    ]
    
    value_lower = value.lower()
    for word in forbidden_words:
        if word in value_lower:
            raise ValidationError(
                _(f'Biyografide "{word}" kelimesi kullanılamaz. '
                  'Platform ücretsiz sahiplenme içindir.')
            )
    
    # Spam kontrolü - tekrarlanan karakterler
    if re.search(r'(.)\1{4,}', value):  # 5+ tekrarlanan karakter
        raise ValidationError(
            _('Biyografide çok fazla tekrarlanan karakter var.')
        )


def validate_instagram_username(value):
    """
    Instagram kullanıcı adı validasyonu
    """
    if not value:
        return
    
    # @ işareti varsa kaldır
    if value.startswith('@'):
        value = value[1:]
    
    # Instagram username pattern
    pattern = r'^[a-zA-Z0-9._]{1,30}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Geçerli bir Instagram kullanıcı adı giriniz. '
              'Sadece harf, rakam, nokta ve alt çizgi kullanılabilir.')
        )
    
    # Ardışık nokta kontrolü
    if '..' in value:
        raise ValidationError(
            _('Instagram kullanıcı adında ardışık nokta bulunamaz.')
        )
    
    # Başında/sonunda nokta kontrolü
    if value.startswith('.') or value.endswith('.'):
        raise ValidationError(
            _('Instagram kullanıcı adı nokta ile başlayamaz veya bitemez.')
        )


def validate_name_field(value):
    """
    İsim alanları validasyonu (ad, soyad)
    """
    if not value:
        return
    
    # Minimum uzunluk
    if len(value.strip()) < 2:
        raise ValidationError(
            _('Ad/soyad en az 2 karakter olmalıdır.')
        )
    
    # Sadece harf ve bazı özel karakterlere izin ver
    pattern = r'^[a-zA-ZçÇğĞıİöÖşŞüÜ\s\-\']+$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Ad/soyad sadece harf içerebilir.')
        )
    
    # Sayı kontrolü
    if any(char.isdigit() for char in value):
        raise ValidationError(
            _('Ad/soyad sayı içeremez.')
        )


def validate_reference_person(value):
    """
    Referans kişi validasyonu
    """
    if not value:
        return
    
    # Format kontrolü: "İsim Soyisim - 05551234567"
    pattern = r'^[a-zA-ZçÇğĞıİöÖşŞüÜ\s]+ - (\+90|0)?[5][0-9]{9}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Referans kişi formatı: "İsim Soyisim - 05551234567" şeklinde olmalıdır.')
        )


def validate_veterinary_reference(value):
    """
    Veteriner referansı validasyonu
    """
    if not value:
        return
    
    # Minimum uzunluk
    if len(value.strip()) < 5:
        raise ValidationError(
            _('Veteriner referansı en az 5 karakter olmalıdır.')
        )
    
    # Format önerisi kontrolü
    required_info = ['veteriner', 'hekim', 'klinik', 'hastane']
    value_lower = value.lower()
    
    if not any(info in value_lower for info in required_info):
        raise ValidationError(
            _('Veteriner referansında veteriner hekim veya klinik bilgisi belirtiniz.')
        )


def validate_pet_experience_years(value):
    """
    Hayvan deneyimi yıl validasyonu
    """
    if value is None:
        return
    
    if value < 0:
        raise ValidationError(
            _('Hayvan deneyimi negatif olamaz.')
        )
    
    if value > 80:
        raise ValidationError(
            _('Hayvan deneyimi 80 yıldan fazla olamaz.')
        )


def validate_strong_user_password(password):
    """
    Güçlü şifre validasyonu
    """
    # Django'nun standart validasyonunu kullan
    validate_password(password)
    
    # Ek güvenlik kuralları
    if len(password) < 8:
        raise ValidationError(
            _('Şifre en az 8 karakter olmalıdır.')
        )
    
    # En az bir büyük harf
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            _('Şifre en az bir büyük harf içermelidir.')
        )
    
    # En az bir küçük harf
    if not re.search(r'[a-z]', password):
        raise ValidationError(
            _('Şifre en az bir küçük harf içermelidir.')
        )
    
    # En az bir rakam
    if not re.search(r'\d', password):
        raise ValidationError(
            _('Şifre en az bir rakam içermelidir.')
        )
    
    # En az bir özel karakter
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(
            _('Şifre en az bir özel karakter içermelidir (!@#$%^&* vb.).')
        )
    
    # Yaygın şifreler kontrolü
    common_passwords = [
        '12345678', 'password', 'qwerty123', 'abc123456',
        'password123', 'admin123', 'user123456'
    ]
    
    if password.lower() in common_passwords:
        raise ValidationError(
            _('Bu şifre çok yaygın kullanılıyor. Daha güçlü bir şifre seçiniz.')
        )


# Validator decorators
def email_domain_validator(email):
    """
    E-posta domain validasyonu
    """
    if not email:
        return
    
    # Yasaklı domainler
    blocked_domains = [
        '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
        'mailinator.com', 'temp-mail.org'
    ]
    
    domain = email.split('@')[1].lower() if '@' in email else ''
    
    if domain in blocked_domains:
        raise ValidationError(
            _('Geçici e-posta adresleri kabul edilmez.')
        )


# Compiled regex patterns for performance
TURKISH_PHONE_REGEX = RegexValidator(
    regex=r'^(\+90|0)?[5][0-9]{9}$',
    message=_('Geçerli bir Türkiye telefon numarası giriniz.')
)

NAME_REGEX = RegexValidator(
    regex=r'^[a-zA-ZçÇğĞıİöÖşŞüÜ\s\-\']+$',
    message=_('Sadece harf ve tire karakteri kullanılabilir.')
)

INSTAGRAM_REGEX = RegexValidator(
    regex=r'^[a-zA-Z0-9._]{1,30}$',
    message=_('Geçerli bir Instagram kullanıcı adı giriniz.')
)

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu validatörler, kullanıcı verilerinin güvenli ve tutarlı olmasını sağlar.
# Türkiye odaklı validasyonlar ve güvenlik önlemleri bir arada.
# 🐾 Her validasyon, daha güvenli bir platform için!
