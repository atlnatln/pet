"""
🐾 Evcil Hayvan Platformu - Ortak Model Temelleri
==============================================================================
Tüm Django uygulamalarının kullanacağı ortak abstract modeller.
Her model, hayvan refahı ve platform güvenliği için optimize edilmiştir.

Bu modeller, platformun DNA'sını oluşturur ve tutarlılık sağlar.
==============================================================================
"""

import uuid
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# ==============================================================================
# 🕒 TIMESTAMP MODEL - Zaman damgası temeli
# ==============================================================================

class TimestampedModel(models.Model):
    """
    Tüm modeller için ortak zaman damgası alanları
    Her hayvan hikayesinin zamanını takip eder
    """
    
    created_at = models.DateTimeField(
        verbose_name="Oluşturulma Tarihi",
        auto_now_add=True,
        help_text="Kayıt ilk oluşturulduğunda otomatik set edilir"
    )
    
    updated_at = models.DateTimeField(
        verbose_name="Güncellenme Tarihi", 
        auto_now=True,
        help_text="Kayıt her güncellendiğinde otomatik güncellenir"
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']  # En yeni kayıtlar önce
    
    def get_age_display(self):
        """Oluşturulma tarihinden itibaren geçen süreyi human-readable format döner"""
        from django.utils.timesince import timesince
        return timesince(self.created_at)

# ==============================================================================
# 🔑 UUID MODEL - Güvenli kimlik temeli
# ==============================================================================

class UUIDModel(models.Model):
    """
    Güvenli UUID primary key kullanımı
    Hayvan kimliklerinin tahmin edilememesi için
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Benzersiz Kimlik",
        help_text="Sistem tarafından otomatik oluşturulan güvenli kimlik"
    )
    
    class Meta:
        abstract = True
    
    def get_short_id(self):
        """Kısa UUID formatı (URL'lerde kullanım için)"""
        return str(self.id).split('-')[0]

# ==============================================================================
# 🔗 SLUG MODEL - SEO dostu URL temeli
# ==============================================================================

class SlugModel(models.Model):
    """
    SEO friendly URL slug'ları
    Hayvan profillerinin aranabilir URL'leri için
    """
    
    title = models.CharField(
        max_length=200,
        verbose_name="Başlık",
        help_text="Slug oluşturmak için kullanılacak başlık"
    )
    
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name="URL Slug",
        help_text="SEO dostu URL parçası (otomatik oluşturulur)",
        blank=True
    )
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        """Slug otomatik oluşturma"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # Benzersiz slug oluşturma
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Model için canonical URL"""
        from django.urls import reverse
        model_name = self.__class__._meta.model_name
        return reverse(f'{model_name}-detail', kwargs={'slug': self.slug})

# ==============================================================================
# 📝 PUBLISHABLE MODEL - Yayın durumu temeli
# ==============================================================================

class PublishableModel(models.Model):
    """
    Draft/Published durumları
    İlanların onay süreçleri için
    """
    
    class StatusChoices(models.TextChoices):
        DRAFT = 'draft', 'Taslak'
        REVIEW = 'review', 'İnceleme'
        PUBLISHED = 'published', 'Yayında'
        REJECTED = 'rejected', 'Reddedildi'
        ARCHIVED = 'archived', 'Arşivlendi'
    
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
        verbose_name="Durum",
        help_text="İçeriğin yayın durumu"
    )
    
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Yayın Tarihi",
        help_text="İçerik yayına geçtiğinde otomatik set edilir"
    )
    
    class Meta:
        abstract = True
    
    def publish(self):
        """İçeriği yayına al"""
        self.status = self.StatusChoices.PUBLISHED
        self.published_at = timezone.now()
        self.save(update_fields=['status', 'published_at'])
    
    def unpublish(self):
        """İçeriği yayından kaldır"""
        self.status = self.StatusChoices.DRAFT
        self.published_at = None
        self.save(update_fields=['status', 'published_at'])
    
    def is_published(self):
        """Yayında mı kontrol et"""
        return self.status == self.StatusChoices.PUBLISHED
    
    @property
    def is_visible(self):
        """Kullanıcılara görülebilir mi"""
        return self.status == self.StatusChoices.PUBLISHED

# ==============================================================================
# 🗑️ SOFT DELETE MODEL - Güvenli silme temeli
# ==============================================================================

class SoftDeleteQuerySet(models.QuerySet):
    """Soft delete için özel QuerySet"""
    
    def active(self):
        """Silinmemiş kayıtları döner"""
        return self.filter(deleted_at__isnull=True)
    
    def deleted(self):
        """Silinmiş kayıtları döner"""
        return self.filter(deleted_at__isnull=False)
    
    def hard_delete(self):
        """Kalıcı silme (dikkatli kullan!)"""
        return super().delete()

class SoftDeleteManager(models.Manager):
    """Soft delete için özel Manager"""
    
    def get_queryset(self):
        """Varsayılan olarak sadece aktif kayıtları döner"""
        return SoftDeleteQuerySet(self.model, using=self._db).active()
    
    def all_with_deleted(self):
        """Tüm kayıtları (silinmiş dahil) döner"""
        return SoftDeleteQuerySet(self.model, using=self._db)
    
    def deleted_only(self):
        """Sadece silinmiş kayıtları döner"""
        return SoftDeleteQuerySet(self.model, using=self._db).deleted()

class SoftDeleteModel(models.Model):
    """
    Güvenli silme (soft delete) işlemleri
    Hayvan kayıtlarının geri getirilebilir olması için
    """
    
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Silinme Tarihi",
        help_text="Kayıt silindiğinde otomatik set edilir"
    )
    
    deleted_by = models.ForeignKey(
        'kullanicilar.Kullanici',  # String reference to avoid circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_%(class)s_set',
        verbose_name="Silen Kullanıcı",
        help_text="Kaydı silen kullanıcı"
    )
    
    # Custom manager'lar
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Tüm kayıtlara erişim için
    
    class Meta:
        abstract = True
    
    def delete(self, hard=False, user=None):
        """
        Soft delete işlemi
        hard=True ile kalıcı silme yapılabilir
        """
        if hard:
            super().delete()
        else:
            self.deleted_at = timezone.now()
            if user:
                self.deleted_by = user
            self.save(update_fields=['deleted_at', 'deleted_by'])
    
    def restore(self):
        """Silinmiş kaydı geri getir"""
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=['deleted_at', 'deleted_by'])
    
    def is_deleted(self):
        """Silinmiş mi kontrol et"""
        return self.deleted_at is not None

# ==============================================================================
# 👤 OWNERSHIP MODEL - Sahiplik temeli
# ==============================================================================

class OwnedModel(models.Model):
    """
    Kullanıcı sahipliği kontrolü
    Her içeriğin sahibinin takibi için
    """
    
    owner = models.ForeignKey(
        'kullanicilar.Kullanici',  # String reference
        on_delete=models.CASCADE,
        related_name='owned_%(class)s_set',
        verbose_name="Sahip",
        help_text="İçeriğin sahibi olan kullanıcı"
    )
    
    class Meta:
        abstract = True
    
    def is_owner(self, user):
        """Kullanıcının sahip olup olmadığını kontrol et"""
        return self.owner == user

# ==============================================================================
# 🔍 SEARCHABLE MODEL - Arama temeli
# ==============================================================================

class SearchableModel(models.Model):
    """
    Full-text search için optimize edilmiş
    Hayvan ve ilan aramaları için
    """
    
    search_vector = models.TextField(
        blank=True,
        verbose_name="Arama Vektörü",
        help_text="Arama için optimize edilmiş metin (otomatik oluşturulur)"
    )
    
    class Meta:
        abstract = True
    
    def update_search_vector(self):
        """Arama vektörünü güncelle"""
        searchable_fields = getattr(self, 'SEARCHABLE_FIELDS', [])
        search_content = []
        
        for field_name in searchable_fields:
            field_value = getattr(self, field_name, '')
            if field_value:
                search_content.append(str(field_value))
        
        self.search_vector = ' '.join(search_content).lower()
    
    def save(self, *args, **kwargs):
        """Kaydetmeden önce arama vektörünü güncelle"""
        self.update_search_vector()
        super().save(*args, **kwargs)

# ==============================================================================
# 🏢 COMPLETE BASE MODEL - Komple temel model
# ==============================================================================

class BaseModel(TimestampedModel, UUIDModel, SoftDeleteModel):
    """
    Platform için komple temel model
    Çoğu model bu temelden türeyecek
    """
    
    class Meta:
        abstract = True
    
    def clean(self):
        """Model validasyonu"""
        super().clean()
        
        # Silinmiş kayıtlar üzerinde işlem yapmaya izin verme
        if self.is_deleted():
            raise ValidationError("Silinmiş kayıtlar üzerinde işlem yapılamaz.")

# ==============================================================================
# 📊 ANALYTICS MODEL - Analitik temeli
# ==============================================================================

class AnalyticsModel(models.Model):
    """
    Platform analitiği için
    Görüntülenme, beğeni gibi metriklerin takibi
    """
    
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Görüntülenme Sayısı",
        help_text="Kaç kez görüntülendiği"
    )
    
    like_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Beğeni Sayısı",
        help_text="Toplam beğeni sayısı"
    )
    
    share_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Paylaşım Sayısı",
        help_text="Kaç kez paylaşıldığı"
    )
    
    class Meta:
        abstract = True
    
    def increment_views(self):
        """Görüntülenme sayısını artır"""
        self.__class__.objects.filter(id=self.id).update(
            view_count=models.F('view_count') + 1
        )
        self.refresh_from_db(fields=['view_count'])
    
    def increment_likes(self):
        """Beğeni sayısını artır"""
        self.__class__.objects.filter(id=self.id).update(
            like_count=models.F('like_count') + 1
        )
        self.refresh_from_db(fields=['like_count'])
    
    def increment_shares(self):
        """Paylaşım sayısını artır"""
        self.__class__.objects.filter(id=self.id).update(
            share_count=models.F('share_count') + 1
        )
        self.refresh_from_db(fields=['share_count'])

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Her abstract model, platformdaki tüm hayvan hikayelerinin 
# güvenli, tutarlı ve optimize edilmiş şekilde saklanması için tasarlandı.
# 🐾 Her satır kod, bir hayvan hayatı için yazıldı! 💝
