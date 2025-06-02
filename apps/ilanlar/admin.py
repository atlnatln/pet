"""
📢 İlanlar Admin Interface
==============================================================================
İlan yönetimi için admin arayüzü
==============================================================================
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Ilan, IlanFotograf, IlanBasvuru


class IlanFotografInline(admin.TabularInline):
    """İlan fotoğrafları inline"""
    model = IlanFotograf
    extra = 1
    fields = ['fotograf', 'aciklama', 'sira']


@admin.register(Ilan)
class IlanAdmin(admin.ModelAdmin):
    """İlan admin"""
    
    list_display = [
        'baslik', 'ilan_turu_badge', 'hayvan_adi', 'durum_badge',
        'il', 'acil_badge', 'ucretsiz_badge', 'yayinlanma_tarihi', 'durum'
    ]
    
    list_filter = [
        'ilan_turu', 'durum', 'acil', 'ucretsiz',
        ('il', admin.AllValuesFieldListFilter),
        ('yayinlanma_tarihi', admin.DateFieldListFilter)
    ]
    
    search_fields = ['baslik', 'aciklama', 'ilan_veren_adi', 'hayvan__ad']
    
    list_editable = ['durum']
    
    inlines = [IlanFotografInline]
    
    fieldsets = (
        (_('İlan Bilgileri'), {
            'fields': ('baslik', 'aciklama', 'ilan_turu', 'hayvan')
        }),
        (_('İletişim'), {
            'fields': ('ilan_veren_adi', 'ilan_veren_telefon', 'ilan_veren_email')
        }),
        (_('Konum'), {
            'fields': ('il', 'ilce', 'adres_detay')
        }),
        (_('Özellikler'), {
            'fields': ('acil', 'ucretsiz', 'fiyat')
        }),
        (_('Yayın'), {
            'fields': ('durum', 'yayinlanma_tarihi', 'bitis_tarihi')
        })
    )
    
    def ilan_turu_badge(self, obj):
        colors = {
            'sahiplendirme': '#10b981',
            'kayip': '#ef4444',
            'bulundu': '#3b82f6'
        }
        color = colors.get(obj.ilan_turu, '#6b7280')
        return format_html(
            '<span style="background-color:{}; color:white; padding:2px 8px; border-radius:12px;">{}</span>',
            color, obj.get_ilan_turu_display()
        )
    ilan_turu_badge.short_description = _('Tür')
    
    def hayvan_adi(self, obj):
        return obj.hayvan.ad if obj.hayvan else '-'
    hayvan_adi.short_description = _('Hayvan')
    
    def durum_badge(self, obj):
        colors = {
            'taslak': '#6b7280',
            'aktif': '#10b981',
            'pasif': '#ef4444',
            'tamamlandi': '#3b82f6'
        }
        color = colors.get(obj.durum, '#6b7280')
        return format_html(
            '<span style="background-color:{}; color:white; padding:2px 8px; border-radius:12px;">{}</span>',
            color, obj.get_durum_display()
        )
    durum_badge.short_description = _('Durum')
    
    def acil_badge(self, obj):
        if obj.acil:
            return format_html('<span style="color:#ef4444;">🚨 Acil</span>')
        return ''
    acil_badge.short_description = _('Acil')
    
    def ucretsiz_badge(self, obj):
        if obj.ucretsiz:
            return format_html('<span style="color:#10b981;">💝 Ücretsiz</span>')
        return format_html('<span style="color:#f59e0b;">💰 {}</span>', obj.fiyat or '-')
    ucretsiz_badge.short_description = _('Fiyat')


@admin.register(IlanBasvuru)
class IlanBasvuruAdmin(admin.ModelAdmin):
    """İlan başvuru admin"""
    
    list_display = [
        'ilan_baslik', 'basvuran_adi', 'basvuran_telefon',
        'durum_badge', 'created_at'
    ]
    
    list_filter = [
        'durum',
        ('created_at', admin.DateFieldListFilter)
    ]
    
    search_fields = ['basvuran_adi', 'basvuran_email', 'ilan__baslik']
    
    readonly_fields = ['created_at']
    
    def ilan_baslik(self, obj):
        return obj.ilan.baslik
    ilan_baslik.short_description = _('İlan')
    
    def durum_badge(self, obj):
        colors = {
            'beklemede': '#f59e0b',
            'onaylandi': '#10b981',
            'reddedildi': '#ef4444'
        }
        color = colors.get(obj.durum, '#6b7280')
        return format_html(
            '<span style="background-color:{}; color:white; padding:2px 8px; border-radius:12px;">{}</span>',
            color, obj.get_durum_display()
        )
    durum_badge.short_description = _('Durum')
