"""
🐾 Evcil Hayvan Platformu - Ortak Validatörler
==============================================================================
Platform genelinde kullanılacak özel validasyon fonksiyonları.
Hayvan sahiplenme süreçleri için özelleştirilmiş validasyonlar.

Her validatör, platform güvenliği ve veri kalitesi için tasarlandı.
==============================================================================
"""

import re
import os
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# ==============================================================================
# 📞 TELEFON NUMARASI VALIDASYONU - Türkiye formatı
# ==============================================================================

def validate_turkish_phone(value):
    """
    Türkiye telefon numarası formatı validasyonu
    Desteklenen formatlar:
    - +90 5XX XXX XX XX
    - 0 5XX XXX XX XX  
    - 5XX XXX XX XX
    """
    # Tüm boşluk ve özel karakterleri temizle
    clean_number = re.sub(r'[\s\-\(\)]+', '', str(value))
    
    # Türkiye ülke kodu kontrolü
    if clean_number.startswith('+90'):
        clean_number = clean_number[3:]
    elif clean_number.startswith('90'):
        clean_number = clean_number[2:]
    elif clean_number.startswith('0'):
        clean_number = clean_number[1:]
    
    # 5XX XXX XX XX formatı kontrolü
    turkish_mobile_pattern = r'^5[0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2}$'
    
    if not re.match(turkish_mobile_pattern, clean_number):
        raise ValidationError(
            _('Geçerli bir Türkiye telefon numarası girin. Örnek: +90 532 123 45 67'),
            code='invalid_phone'
        )
    
    return clean_number

# Regex validator olarak da kullanım
turkish_phone_validator = RegexValidator(
    regex=r'^(\+90|0)?[5][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2}$',
    message=_('Geçerli bir Türkiye cep telefonu numarası girin.'),
    code='invalid_turkish_phone'
)

# ==============================================================================
# 🖼️ GÖRSEL VALIDASYONU - Hayvan fotoğrafları için
# ==============================================================================

def validate_image_size(image):
    """
    Görsel boyut validasyonu
    Maksimum boyut: 10MB
    Minimum boyut: 100KB
    """
    max_size = getattr(settings, 'MAX_IMAGE_SIZE', 10 * 1024 * 1024)  # 10MB
    min_size = getattr(settings, 'MIN_IMAGE_SIZE', 100 * 1024)  # 100KB
    
    if image.size > max_size:
        raise ValidationError(
            _(f'Görsel boyutu {max_size // (1024*1024)}MB\'dan büyük olamaz.'),
            code='image_too_large'
        )
    
    if image.size < min_size:
        raise ValidationError(
            _(f'Görsel boyutu {min_size // 1024}KB\'dan küçük olamaz.'),
            code='image_too_small'
        )

def validate_image_format(image):
    """
    Görsel format validasyonu
    İzin verilen formatlar: JPEG, PNG, WebP
    """
    allowed_formats = ['JPEG', 'PNG', 'WEBP']
    
    try:
        with Image.open(image) as img:
            if img.format not in allowed_formats:
                raise ValidationError(
                    _('Sadece JPEG, PNG ve WebP formatları kabul edilir.'),
                    code='invalid_image_format'
                )
            
            # Minimum çözünürlük kontrolü
            min_width = getattr(settings, 'MIN_IMAGE_WIDTH', 300)
            min_height = getattr(settings, 'MIN_IMAGE_HEIGHT', 300)
            
            if img.width < min_width or img.height < min_height:
                raise ValidationError(
                    _(f'Görsel en az {min_width}x{min_height} piksel olmalıdır.'),
                    code='image_resolution_too_low'
                )
            
            # Maksimum çözünürlük kontrolü
            max_width = getattr(settings, 'MAX_IMAGE_WIDTH', 4000)
            max_height = getattr(settings, 'MAX_IMAGE_HEIGHT', 4000)
            
            if img.width > max_width or img.height > max_height:
                raise ValidationError(
                    _(f'Görsel en fazla {max_width}x{max_height} piksel olabilir.'),
                    code='image_resolution_too_high'
                )
                
    except (OSError, IOError):
        raise ValidationError(
            _('Geçersiz görsel dosyası.'),
            code='invalid_image'
        )

def validate_pet_image(image):
    """
    Hayvan fotoğrafı için komple validasyon
    """
    validate_image_size(image)
    validate_image_format(image)
    
    # Dosya uzantısı kontrolü
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(image.name)[1].lower()
    
    if ext not in allowed_extensions:
        raise ValidationError(
            _('Sadece JPG, PNG ve WebP dosyaları yükleyebilirsiniz.'),
            code='invalid_file_extension'
        )

# ==============================================================================
# 📝 İÇERİK FİLTRELEME - Uygunsuz içerik kontrolü
# ==============================================================================

# Yasaklı kelimeler listesi (hayvan refahı için)
FORBIDDEN_WORDS = [
    'satılık', 'para', 'ücret', 'bedel', 'fiyat', 'parayla',
    'dövüş', 'kavga', 'agresif', 'saldırgan',
    'hasta', 'hastalık', 'enfeksiyon', 'parazit',
    # Daha fazla kelime eklenebilir
]

def validate_content_appropriateness(text):
    """
    İçerik uygunluğu kontrolü
    Hayvan satışı ve zararlı içerik tespiti
    """
    if not text:
        return
    
    text_lower = text.lower()
    
    # Yasaklı kelime kontrolü
    for word in FORBIDDEN_WORDS:
        if word in text_lower:
            raise ValidationError(
                _(f'İçeriğinizde uygunsuz kelime tespit edildi: "{word}". '
                  f'Platform politikalarımıza göre hayvan satışı yasaktır.'),
                code='inappropriate_content'
            )
    
    # Telefon numarası kontrolü (içerikte telefon paylaşımı yasak)
    phone_pattern = r'[0-9]{3}[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}'
    if re.search(phone_pattern, text):
        raise ValidationError(
            _('İçerikte telefon numarası paylaşamazsınız. '
              'İletişim için platform mesajlaşma sistemini kullanın.'),
            code='phone_in_content'
        )
    
    # Email kontrolü
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_pattern, text):
        raise ValidationError(
            _('İçerikte email adresi paylaşamazsınız. '
              'İletişim için platform mesajlaşma sistemini kullanın.'),
            code='email_in_content'
        )

# ==============================================================================
# 🏷️ ETİKET VALIDASYONU - İçerik etiketleri için
# ==============================================================================

def validate_tag_name(tag_name):
    """
    Etiket adı validasyonu
    Türkçe karakter desteği ile
    """
    # Minimum ve maksimum uzunluk
    if len(tag_name) < 2:
        raise ValidationError(
            _('Etiket adı en az 2 karakter olmalıdır.'),
            code='tag_too_short'
        )
    
    if len(tag_name) > 30:
        raise ValidationError(
            _('Etiket adı en fazla 30 karakter olabilir.'),
            code='tag_too_long'
        )
    
    # Sadece harf, rakam ve tire karakteri
    tag_pattern = r'^[a-zA-ZğüşıöçĞÜŞİÖÇ0-9\-\s]+$'
    if not re.match(tag_pattern, tag_name):
        raise ValidationError(
            _('Etiket sadece harf, rakam ve tire karakteri içerebilir.'),
            code='invalid_tag_format'
        )

# ==============================================================================
# 📍 KONUM VALIDASYONU - Türkiye il/ilçe kontrolü
# ==============================================================================

# Türkiye'nin 81 ili
TURKISH_CITIES = [
    'Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Aksaray', 'Amasya',
    'Ankara', 'Antalya', 'Ardahan', 'Artvin', 'Aydın', 'Balıkesir',
    'Bartın', 'Batman', 'Bayburt', 'Bilecik', 'Bingöl', 'Bitlis',
    'Bolu', 'Burdur', 'Bursa', 'Çanakkale', 'Çankırı', 'Çorum',
    'Denizli', 'Diyarbakır', 'Düzce', 'Edirne', 'Elazığ', 'Erzincan',
    'Erzurum', 'Eskişehir', 'Gaziantep', 'Giresun', 'Gümüşhane', 'Hakkari',
    'Hatay', 'Iğdır', 'Isparta', 'İstanbul', 'İzmir', 'Kahramanmaraş',
    'Karabük', 'Karaman', 'Kars', 'Kastamonu', 'Kayseri', 'Kırıkkale',
    'Kırklareli', 'Kırşehir', 'Kilis', 'Kocaeli', 'Konya', 'Kütahya',
    'Malatya', 'Manisa', 'Mardin', 'Mersin', 'Muğla', 'Muş',
    'Nevşehir', 'Niğde', 'Ordu', 'Osmaniye', 'Rize', 'Sakarya',
    'Samsun', 'Siirt', 'Sinop', 'Sivas', 'Şanlıurfa', 'Şırnak',
    'Tekirdağ', 'Tokat', 'Trabzon', 'Tunceli', 'Uşak', 'Van',
    'Yalova', 'Yozgat', 'Zonguldak'
]

def validate_turkish_city(city_name):
    """
    Türkiye ili validasyonu
    """
    if city_name not in TURKISH_CITIES:
        raise ValidationError(
            _('Geçerli bir Türkiye ili seçiniz.'),
            code='invalid_turkish_city'
        )

# ==============================================================================
# 🎂 YAŞ VALIDASYONU - Hayvan yaşları için
# ==============================================================================

def validate_pet_age(age_months):
    """
    Hayvan yaşı validasyonu (ay cinsinden)
    """
    if age_months is None:
        return
    
    if age_months < 0:
        raise ValidationError(
            _('Hayvan yaşı negatif olamaz.'),
            code='negative_age'
        )
    
    if age_months > 300:  # 25 yıl
        raise ValidationError(
            _('Hayvan yaşı 25 yıldan fazla olamaz.'),
            code='age_too_high'
        )

# ==============================================================================
# 🏥 ASI KONTROLÜ - Aşı tarih validasyonu
# ==============================================================================

def validate_vaccination_date(date):
    """
    Aşı tarihi validasyonu
    """
    from django.utils import timezone
    from datetime import timedelta
    
    if not date:
        return
    
    today = timezone.now().date()
    
    # Gelecek tarih kontrolü
    if date > today:
        raise ValidationError(
            _('Aşı tarihi gelecekte olamaz.'),
            code='future_vaccination_date'
        )
    
    # Çok eski tarih kontrolü (5 yıl)
    five_years_ago = today - timedelta(days=5*365)
    if date < five_years_ago:
        raise ValidationError(
            _('Aşı tarihi 5 yıldan eski olamaz.'),
            code='vaccination_date_too_old'
        )

# ==============================================================================
# 🛡️ SECURITY VALIDATORS - Enhanced security validation
# ==============================================================================

def validate_file_security(file: UploadedFile):
    """
    Enhanced file security validation
    """
    # Check file size
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError(_('Dosya boyutu 5MB\'dan büyük olamaz.'))
    
    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    file_extension = file.name.lower().split('.')[-1]
    if f'.{file_extension}' not in allowed_extensions:
        raise ValidationError(_('Geçersiz dosya formatı.'))
    
    # Check file header (magic numbers)
    file.seek(0)
    header = file.read(8)
    file.seek(0)
    
    # JPEG magic numbers
    if not (header.startswith(b'\xff\xd8\xff') or  # JPEG
            header.startswith(b'\x89PNG\r\n\x1a\n') or  # PNG
            header.startswith(b'GIF87a') or header.startswith(b'GIF89a') or  # GIF
            header.startswith(b'RIFF')):  # WebP
        raise ValidationError(_('Dosya içeriği geçersiz.'))
    
    # Additional image validation
    try:
        image = Image.open(file)
        image.verify()
    except Exception:
        raise ValidationError(_('Geçersiz görsel dosyası.'))

def validate_strong_password(password):
    """
    Strong password validation for pet platform users
    """
    if len(password) < 8:
        raise ValidationError(_('Şifre en az 8 karakter olmalıdır.'))
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError(_('Şifre en az bir büyük harf içermelidir.'))
    
    if not re.search(r'[a-z]', password):
        raise ValidationError(_('Şifre en az bir küçük harf içermelidir.'))
    
    if not re.search(r'\d', password):
        raise ValidationError(_('Şifre en az bir rakam içermelidir.'))
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(_('Şifre en az bir özel karakter içermelidir.'))
    
    # Check against common passwords
    common_passwords = [
        'password', '123456', 'password123', 'admin', 'qwerty',
        'hayvan123', 'kedi123', 'kopek123', 'sevgi123'
    ]
    
    if password.lower() in common_passwords:
        raise ValidationError(_('Bu şifre çok yaygın kullanılıyor.'))

def validate_user_input_security(value):
    """
    Validate user input for security threats
    """
    # XSS prevention
    xss_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'onload\s*=',
        r'onerror\s*=',
        r'onclick\s*=',
    ]
    
    for pattern in xss_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError(_('Geçersiz içerik tespit edildi.'))
    
    # SQL injection prevention
    sql_patterns = [
        r'union\s+select',
        r'drop\s+table',
        r'delete\s+from',
        r'insert\s+into',
        r'update\s+.*\s+set',
    ]
    
    for pattern in sql_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError(_('Güvenlik riski tespit edildi.'))

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Her validatör, platform güvenliği ve hayvan refahını ön planda tutar.
# Uygunsuz içerik filtreleme, kaliteli veri girişi ve kullanıcı deneyimi 
# için tasarlandı.
# 🐾 Her kontrol, güvenli bir sahiplenme için! 💝
