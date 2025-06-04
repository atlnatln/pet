"""
🏷️ Evcil Hayvan Platformu - Etiketler Admin
==============================================================================
Etiket modelinin yönetici panelinde görüntülenmesi ve düzenlenmesi
==============================================================================
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.utils.safestring import mark_safe

from .models import Etiket


@admin.register(Etiket)
class EtiketAdmin(admin.ModelAdmin):
    list_display = ('ad', 'slug', 'renk_renkli', 'kullanim_sayisi_goster', 'aktif', 'olusturma_tarihi')
    list_filter = ('aktif', 'olusturma_tarihi')
    search_fields = ('ad', 'aciklama', 'slug')
    prepopulated_fields = {'slug': ('ad',)}
    readonly_fields = ('kullanim_sayisi_goster', 'olusturma_tarihi', 'guncelleme_tarihi')
    fieldsets = (
        (_('Temel Bilgiler'), {
            'fields': ('ad', 'slug', 'aciklama')
        }),
        (_('Görsel Özellikler'), {
            'fields': ('renk_kodu', 'ikon'),
            'description': _('Etiketin görsel özelliklerini yapılandırın.')
        }),
        (_('Durum'), {
            'fields': ('aktif',)
        }),
        (_('Kullanım Bilgileri'), {
            'fields': ('kullanim_sayisi_goster',),
            'classes': ('collapse',)
        }),
        (_('Zaman Bilgileri'), {
            'fields': ('olusturma_tarihi', 'guncelleme_tarihi'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Tüm etiketleri göster, aktif olmayanlar dahil"""
        return Etiket.tum_etiketler.all()
    
    def kullanim_sayisi_goster(self, obj):
        """Etiketin kullanım sayısını gösterir"""
        return obj.kullanim_sayisi
    kullanim_sayisi_goster.short_description = _("Kullanım Sayısı")
    
    def renk_renkli(self, obj):
        """Renk kodunun önizlemesini gösterir"""
        return mark_safe(
            f'<span style="display:inline-block; width:20px; height:20px; ' 
            f'background-color:{obj.renk_kodu}; border-radius:4px;"></span> '
            f'{obj.renk_kodu}'
        )
    renk_renkli.short_description = _("Renk")
    
    class Media:
        css = {
            'all': ('css/admin/etiket_admin.css',)
        }