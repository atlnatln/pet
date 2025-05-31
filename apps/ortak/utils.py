"""
🐾 Evcil Hayvan Platformu - Ortak Utilities
==============================================================================
Platform genelinde kullanılacak yardımcı fonksiyonlar
==============================================================================
"""

import uuid
import hashlib
import secrets
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.cache import cache
from django.utils.translation import gettext as _
from PIL import Image
import io

# ==============================================================================
# 🔧 STRING UTILITIES - String yardımcıları
# ==============================================================================

def generate_unique_id(prefix: str = "") -> str:
    """
    Benzersiz ID üret
    """
    unique_id = str(uuid.uuid4()).replace('-', '')[:12]
    return f"{prefix}_{unique_id}" if prefix else unique_id

def generate_secure_token(length: int = 32) -> str:
    """
    Güvenli token üret
    """
    return secrets.token_urlsafe(length)

def create_slug(text: str, max_length: int = 50) -> str:
    """
    SEO dostu slug oluştur
    """
    # Türkçe karakterleri dönüştür
    turkish_map = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c'
    }
    
    for tr_char, en_char in turkish_map.items():
        text = text.replace(tr_char, en_char)
    
    slug = slugify(text, allow_unicode=False)
    return slug[:max_length] if len(slug) > max_length else slug

def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 3) -> str:
    """
    Hassas veriyi maskele (email, telefon vs.)
    """
    if not data or len(data) <= visible_chars * 2:
        return mask_char * len(data) if data else ""
    
    start = data[:visible_chars]
    end = data[-visible_chars:]
    middle = mask_char * (len(data) - visible_chars * 2)
    
    return f"{start}{middle}{end}"

# ==============================================================================
# 📅 DATE & TIME UTILITIES - Tarih ve zaman yardımcıları
# ==============================================================================

def get_age_display(birth_date: datetime) -> str:
    """
    Doğum tarihinden yaş hesapla ve görüntüle
    """
    if not birth_date:
        return _("Bilinmiyor")
    
    now = timezone.now().date()
    age = now - birth_date.date() if hasattr(birth_date, 'date') else now - birth_date
    
    years = age.days // 365
    months = (age.days % 365) // 30
    days = age.days % 30
    
    if years > 0:
        return f"{years} yaş" + (f" {months} ay" if months > 0 else "")
    elif months > 0:
        return f"{months} ay" + (f" {days} gün" if days > 0 and months < 6 else "")
    else:
        return f"{days} gün"

def time_ago(date_time: datetime) -> str:
    """
    "X zaman önce" formatında zaman farkı
    """
    if not date_time:
        return _("Bilinmiyor")
    
    now = timezone.now()
    diff = now - date_time
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return _("az önce")
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} dakika önce"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} saat önce"
    elif seconds < 2592000:  # 30 days
        days = int(seconds // 86400)
        return f"{days} gün önce"
    else:
        return date_time.strftime("%d.%m.%Y")

def is_business_hours() -> bool:
    """
    Mesai saatleri içinde mi kontrol et
    """
    now = timezone.localtime()
    return 9 <= now.hour <= 18 and now.weekday() < 5  # Pazartesi-Cuma 09:00-18:00

# ==============================================================================
# 🖼️ IMAGE UTILITIES - Görsel yardımcıları
# ==============================================================================

def resize_image(image_file, max_width: int = 800, max_height: int = 600, quality: int = 85) -> ContentFile:
    """
    Görseli yeniden boyutlandır
    """
    # Dosya tipini kontrol et
    if not image_file.content_type.startswith('image/'):
        raise ValueError("Geçersiz görsel dosyası")
    
    # PIL ile aç
    image = Image.open(image_file)
    
    # EXIF rotasyonunu düzelt
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if exif is not None:
            for tag, value in exif.items():
                if tag == 274:  # Orientation tag
                    if value == 3:
                        image = image.rotate(180, expand=True)
                    elif value == 6:
                        image = image.rotate(270, expand=True)
                    elif value == 8:
                        image = image.rotate(90, expand=True)
    
    # RGB'ye çevir (RGBA varsa)
    if image.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if 'A' in image.mode else None)
        image = background
    
    # Boyutlandır
    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    # Kaydet
    output = io.BytesIO()
    format_map = {
        'image/jpeg': 'JPEG',
        'image/jpg': 'JPEG',
        'image/png': 'PNG',
        'image/webp': 'WEBP'
    }
    image_format = format_map.get(image_file.content_type, 'JPEG')
    image.save(output, format=image_format, quality=quality, optimize=True)
    
    return ContentFile(output.getvalue(), name=image_file.name)

def generate_thumbnail(image_file, size: tuple = (150, 150)) -> ContentFile:
    """
    Thumbnail oluştur
    """
    return resize_image(image_file, max_width=size[0], max_height=size[1], quality=90)

# ==============================================================================
# 🔐 SECURITY UTILITIES - Güvenlik yardımcıları
# ==============================================================================

def hash_data(data: str, salt: str = None) -> str:
    """
    Veriyi hash'le
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    combined = f"{data}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()

def validate_phone_number(phone: str) -> bool:
    """
    Türk telefon numarası validasyonu
    """
    # Sadece rakamları al
    digits = re.sub(r'\D', '', phone)
    
    # Türkiye formatları: 5XXXXXXXXX, 90XXXXXXXXXX, 0XXXXXXXXXX
    if len(digits) == 10 and digits.startswith('5'):
        return True
    elif len(digits) == 12 and digits.startswith('90'):
        return True
    elif len(digits) == 11 and digits.startswith('05'):
        return True
    
    return False

def clean_phone_number(phone: str) -> str:
    """
    Telefon numarasını temizle ve standart formata çevir
    """
    if not phone:
        return ""
    
    # Sadece rakamları al
    digits = re.sub(r'\D', '', phone)
    
    # Standart formata çevir (5XXXXXXXXX)
    if len(digits) == 10 and digits.startswith('5'):
        return digits
    elif len(digits) == 12 and digits.startswith('90'):
        return digits[2:]
    elif len(digits) == 11 and digits.startswith('05'):
        return digits[1:]
    
    return phone  # Geçersizse olduğu gibi döndür

# ==============================================================================
# 💾 CACHE UTILITIES - Cache yardımcıları
# ==============================================================================

def get_cache_key(prefix: str, *args) -> str:
    """
    Cache key oluştur
    """
    key_parts = [str(arg) for arg in args if arg is not None]
    return f"{prefix}:{'_'.join(key_parts)}"

def cache_get_or_set(key: str, callable_func, timeout: int = 300):
    """
    Cache'den al yoksa set et
    """
    cached_data = cache.get(key)
    if cached_data is None:
        cached_data = callable_func()
        cache.set(key, cached_data, timeout)
    return cached_data

def invalidate_cache_pattern(pattern: str):
    """
    Pattern'e uyan cache'leri temizle
    """
    # Redis backend kullanıyorsak
    try:
        from django_redis import get_redis_connection
        conn = get_redis_connection("default")
        keys = conn.keys(f"*{pattern}*")
        if keys:
            conn.delete(*keys)
    except:
        # Fallback: cache.clear() kullan
        cache.clear()

# ==============================================================================
# 📊 DATA UTILITIES - Veri yardımcıları
# ==============================================================================

def paginate_queryset(queryset, page: int = 1, per_page: int = 20):
    """
    QuerySet'i sayfalandır
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    paginator = Paginator(queryset, per_page)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return {
        'items': page_obj.object_list,
        'page': page_obj.number,
        'pages': paginator.num_pages,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'total': paginator.count,
    }

def serialize_for_json(obj) -> Any:
    """
    Objeyi JSON serializable hale getir
    """
    if hasattr(obj, 'isoformat'):  # datetime objects
        return obj.isoformat()
    elif hasattr(obj, '__dict__'):  # model instances
        return {key: serialize_for_json(value) for key, value in obj.__dict__.items() 
                if not key.startswith('_')}
    elif isinstance(obj, (list, tuple)):
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_for_json(value) for key, value in obj.items()}
    else:
        return obj

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu utility fonksiyonlar, platform genelinde kod tekrarını önler
# ve tutarlı işlemler sağlar.
# 🐾 Her yardımcı fonksiyon, daha temiz kod için!
