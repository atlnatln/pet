"""
🐾 Evcil Hayvan Platformu - Hayvan Yardımcı İşlevleri
==============================================================================
Hayvanlarla ilgili yardımcı işlevler ve araçlar
==============================================================================
"""

import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def create_thumbnail(photo_field, size=(300, 300)):
    """
    Fotoğraf için thumbnail oluşturur
    
    Args:
        photo_field: ImageField
        size: (genişlik, yükseklik) tuple
        
    Returns:
        ContentFile: Thumbnail dosyası
    """
    # Orijinal resmi aç
    file_path = photo_field.path
    thumbnail_name = f"thumb_{os.path.basename(file_path)}"
    
    # Resmi işle
    with Image.open(file_path) as img:
        # Doğru oran ile küçült
        img.thumbnail(size, Image.LANCZOS)
        
        # Thumbnail'i kaydet
        thumb_io = BytesIO()
        img_format = img.format if img.format else 'JPEG'
        img.save(thumb_io, format=img_format, quality=85)
        thumb_io.seek(0)
        
        # Dosya yolu oluştur
        thumbnail_path = os.path.join('hayvanlar/thumbnails', thumbnail_name)
        
        # Kaydet ve döndür
        return default_storage.save(thumbnail_path, ContentFile(thumb_io.read()))


def karakter_ozellikleri_listesi():
    """
    Tanımlı karakter özellikleri listesi
    
    Returns:
        list: [(anahtar, gösterim adı, açıklama), ...]
    """
    return [
        ('playful', 'Oyuncu', 'Oyun oynamayı seven, aktif'),
        ('calm', 'Sakin', 'Sessiz, sakin ve huzurlu'),
        ('energetic', 'Enerjik', 'Yüksek enerjili ve hareketli'),
        ('friendly', 'Arkadaş Canlısı', 'İnsanlara karşı açık ve samimi'),
        ('shy', 'Çekingen', 'Yeni ortam ve insanlara alışması zaman alır'),
        ('protective', 'Korumacı', 'Ailesini ve bölgesini koruma eğiliminde'),
        ('independent', 'Bağımsız', 'Kendi başına vakit geçirmeyi sever'),
        ('affectionate', 'Sevecen', 'Sevgi göstermeyi ve ilgi görmeyi sever'),
        ('intelligent', 'Zeki', 'Yeni şeyleri hızlıca öğrenir'),
        ('curious', 'Meraklı', 'Keşfetmeyi ve araştırmayı sever')
    ]
