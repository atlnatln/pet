"""
🐾 Kategoriler Admin Interface
==============================================================================
Kategori yönetimi için kullanıcı dostu admin arayüzü
==============================================================================
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.db import models  # Bu import eksikti
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Kategori, KategoriOzellik


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    """
    Kategori admin arayüzü - Hikayeli kategori yönetimi
    """
    
    list_display = [
        'ad', 'parent', 'pet_type', 'sira', 'aktif', 
        'kullanim_sayisi', 'renk_kodu', 'created_at'  # olusturulma_tarihi -> created_at
    ]
    
    list_filter = [
        'pet_type', 'aktif', 'parent', 'created_at'  # olusturulma_tarihi -> created_at
    ]
    
    search_fields = ['ad', 'aciklama', 'slug']
    
    prepopulated_fields = {'slug': ('ad',)}
    
    ordering = ['parent__ad', 'sira', 'ad']
    
    list_editable = ['sira', 'aktif']  # Bu alanlar list_display'de olmalı
    
    list_per_page = 25
    
    fieldsets = (
        (_('🏷️ Temel Bilgiler'), {
            'fields': ('ad', 'slug', 'aciklama', 'parent')
        }),
        (_('🎨 Görsel Kimlik'), {
            'fields': ('pet_type', 'ikon_adi', 'renk_kodu'),
            'classes': ('collapse',)
        }),
        (_('⚙️ Ayarlar'), {
            'fields': ('aktif', 'sira'),
            'classes': ('collapse',)
        }),
        (_('📊 İstatistikler'), {
            'fields': ('kullanim_sayisi',),
            'classes': ('collapse',),
            'description': _('Bu alanlar otomatik güncellenir')
        }),
    )
    
    readonly_fields = ['kullanim_sayisi']
    
    actions = ['aktif_yap', 'pasif_yap', 'istatistikleri_guncelle']
    
    def kategori_gorseli(self, obj):
        """Kategori ikonu ve rengi göster"""
        if obj.ikon_adi:
            return format_html(
                '<i class="fa {} fa-2x" style="color: {}"></i>',
                obj.ikon_adi,
                obj.renk_kodu
            )
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px;"></div>',
            obj.renk_kodu
        )
    kategori_gorseli.short_description = _('🎨 Görsel')
    
    def parent_kategori(self, obj):
        """Ana kategori göster"""
        if obj.parent:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:kategoriler_kategori_change', args=[obj.parent.id]),
                obj.parent.ad
            )
        return format_html('<strong>{}</strong>', _('Ana Kategori'))
    parent_kategori.short_description = _('📂 Ana Kategori')
    
    def pet_type_badge(self, obj):
        """Pet type badge göster"""
        colors = {
            'dog': '#f59e0b',
            'cat': '#8b5cf6', 
            'bird': '#06b6d4',
            'fish': '#3b82f6',
            'rabbit': '#f97316',
            'reptile': '#059669',
            'other': '#dc2626'
        }
        color = colors.get(obj.pet_type, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            color,
            obj.get_pet_type_display()
        )
    pet_type_badge.short_description = _('🐾 Tür')
    
    def alt_kategori_sayisi(self, obj):
        """Alt kategori sayısı"""
        count = obj.alt_kategoriler.filter(aktif=True).count()
        if count > 0:
            return format_html(
                '<a href="{}?parent__id__exact={}">{} alt kategori</a>',
                reverse('admin:kategoriler_kategori_changelist'),
                obj.id,
                count
            )
        return _('Alt kategori yok')
    alt_kategori_sayisi.short_description = _('📁 Alt Kategoriler')
    
    def aktif_badge(self, obj):
        """Aktif durum badge"""
        if obj.aktif:
            return format_html(
                '<span style="color: green;">✅ {}</span>',
                _('Aktif')
            )
        return format_html(
            '<span style="color: red;">❌ {}</span>',
            _('Pasif')
        )
    aktif_badge.short_description = _('📊 Durum')
    
    def get_queryset(self, request):
        """Optimize edilmiş queryset"""
        return super().get_queryset(request).select_related('parent').annotate(
            alt_kategori_count=Count('alt_kategoriler', filter=models.Q(alt_kategoriler__aktif=True))
        )
    
    # Actions
    def aktif_yap(self, request, queryset):
        """Seçili kategorileri aktif yap"""
        updated = queryset.update(aktif=True)
        self.message_user(
            request,
            f'{updated} kategori aktif yapıldı. 🎉'
        )
    aktif_yap.short_description = _('✅ Seçili kategorileri aktif yap')
    
    def pasif_yap(self, request, queryset):
        """Seçili kategorileri pasif yap"""
        updated = queryset.update(aktif=False)
        self.message_user(
            request,
            f'{updated} kategori pasif yapıldı. ⏸️'
        )
    pasif_yap.short_description = _('❌ Seçili kategorileri pasif yap')
    
    def istatistikleri_guncelle(self, request, queryset):
        """Kategori istatistiklerini güncelle"""
        for kategori in queryset:
            # Bu method hayvan modeli oluşturulduktan sonra implement edilecek
            pass
        
        self.message_user(
            request,
            f'{queryset.count()} kategorinin istatistikleri güncellendi. 📊'
        )
    istatistikleri_guncelle.short_description = _('📊 İstatistikleri güncelle')


class KategoriOzellikInline(admin.TabularInline):
    """
    Kategori özelliklerini inline olarak göster
    """
    model = KategoriOzellik
    extra = 1
    fields = ['ad', 'zorunlu', 'aktif', 'sira']  # alan_tipi kaldırıldı çünkü model'de yok
    ordering = ['sira', 'ad']


@admin.register(KategoriOzellik)
class KategoriOzellikAdmin(admin.ModelAdmin):
    """
    Kategori özellik admin arayüzü
    """
    
    list_display = [
        'ad', 'kategori', 'zorunlu', 'aktif',  # veri_tipi kaldırıldı
        'sira', 'created_at'
    ]
    
    list_filter = ['zorunlu', 'aktif', 'kategori']  # veri_tipi kaldırıldı
    
    search_fields = ['ad', 'kategori__ad']
    
    ordering = ['kategori__ad', 'sira', 'ad']
    
    list_editable = ['zorunlu', 'aktif']  # Bu alanlar list_display'de olmalı
    
    def kategori_link(self, obj):
        """Kategori linkini göster"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:kategoriler_kategori_change', args=[obj.kategori.id]),
            obj.kategori.tam_ad
        )
    kategori_link.short_description = _('📂 Kategori')
    
    def alan_tipi_badge(self, obj):
        """Alan tipi badge"""
        colors = {
            'text': '#6b7280',
            'number': '#3b82f6',
            'select': '#8b5cf6',
            'boolean': '#059669',
            'range': '#f59e0b'
        }
        color = colors.get(obj.alan_tipi, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 8px; font-size: 10px;">{}</span>',
            color,
            obj.get_alan_tipi_display()
        )
    alan_tipi_badge.short_description = _('🔧 Tip')
    
    def zorunlu_badge(self, obj):
        """Zorunlu badge"""
        if obj.zorunlu:
            return format_html('<span style="color: red;">⚠️ Zorunlu</span>')
        return format_html('<span style="color: green;">📝 İsteğe bağlı</span>')
    zorunlu_badge.short_description = _('📋 Zorunluluk')
    
    def aktif_badge(self, obj):
        """Aktif badge"""
        if obj.aktif:
            return format_html('<span style="color: green;">✅</span>')
        return format_html('<span style="color: red;">❌</span>')
    aktif_badge.short_description = _('📊 Durum')


# Kategori admin'e özellikleri inline olarak ekle
KategoriAdmin.inlines = [KategoriOzellikInline]

# Admin site özelleştirmeleri
admin.site.site_header = "🐾 Evcil Hayvan Platformu Yönetimi"
admin.site.site_title = "Pet Platform Admin"
admin.site.index_title = "Platformu yönetin - Her canlı bir hikaye! 💝"
