"""
🐾 Kullanıcılar Admin Interface
==============================================================================
Kullanıcı yönetimi için kapsamlı admin arayüzü
==============================================================================
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import CustomUser, KullaniciProfil


class KullaniciProfilInline(admin.StackedInline):
    """
    Kullanıcı profil detaylarını inline olarak göster
    """
    model = KullaniciProfil
    can_delete = False
    verbose_name_plural = _('Profil Detayları')
    
    fieldsets = (
        (_('🏠 Konut Bilgileri'), {
            'fields': ('ev_tipi', 'bahce_var_mi', 'diger_hayvanlar')
        }),
        (_('🐾 Deneyim Bilgileri'), {
            'fields': ('hayvan_deneyimi_yil', 'daha_once_sahiplendin_mi', 'veteriner_referansi')
        }),
        (_('📱 Sosyal Medya'), {
            'fields': ('instagram_hesabi', 'facebook_hesabi'),
            'classes': ('collapse',)
        }),
        (_('👥 Referanslar'), {
            'fields': ('referans_kisi_1', 'referans_kisi_2'),
            'classes': ('collapse',)
        }),
        (_('✅ Doğrulama'), {
            'fields': ('kimlik_dogrulandi_mi',),
            'classes': ('collapse',)
        }),
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Özel kullanıcı admin arayüzü
    """
    
    list_display = [
        'email', 'first_name', 'last_name', 'rol',  # rol eklendi
        'durum', 'email_dogrulanmis', 'uyelik_tarihi'
    ]
    
    list_filter = [
        'rol', 'durum', 'email_dogrulanmis', 'sahiplendiren_mi',
        'sahiplenmek_istiyor_mu', 'uyelik_tarihi'
    ]
    
    search_fields = ['first_name', 'last_name', 'email', 'telefon']
    
    ordering = ['-uyelik_tarihi']
    
    list_editable = ['rol']  # Bu alan list_display'de olmalı
    
    list_per_page = 25
    
    readonly_fields = [
        'id', 'uyelik_tarihi', 'guncelleme_tarihi', 'son_giris_tarihi',
        'giris_sayisi', 'email_dogrulama_tarihi', 'profil_tamamlama_widget'
    ]
    
    fieldsets = (
        (_('👤 Temel Bilgiler'), {
            'fields': ('id', 'email', 'password')
        }),
        (_('🏷️ Kişisel Bilgiler'), {
            'fields': ('first_name', 'last_name', 'telefon', 'sehir', 'biyografi')
        }),
        (_('🖼️ Profil'), {
            'fields': ('profil_resmi', 'profil_tamamlama_widget'),
            'classes': ('collapse',)
        }),
        (_('🔐 Yetki ve Durum'), {
            'fields': ('rol', 'durum', 'is_active', 'is_staff', 'is_superuser')
        }),
        (_('📧 E-posta Doğrulama'), {
            'fields': ('email_dogrulanmis', 'email_dogrulama_tarihi'),
            'classes': ('collapse',)
        }),
        (_('🐾 Platform Tercihleri'), {
            'fields': ('sahiplendiren_mi', 'sahiplenmek_istiyor_mu')
        }),
        (_('🔔 Bildirim Tercihleri'), {
            'fields': ('email_bildirimleri', 'push_bildirimleri'),
            'classes': ('collapse',)
        }),
        (_('📊 İstatistikler'), {
            'fields': ('uyelik_tarihi', 'guncelleme_tarihi', 'son_giris_tarihi', 'giris_sayisi'),
            'classes': ('collapse',)
        }),
        (_('👥 Grup Üyelikleri'), {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (_('👤 Temel Bilgiler'), {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
        (_('🏷️ Ek Bilgiler'), {
            'classes': ('wide',),
            'fields': ('rol', 'telefon', 'sehir'),
        }),
    )
    
    actions = [
        'email_dogrula', 'email_dogrulama_iptal', 'kullanici_aktif_et',
        'kullanici_pasif_et', 'moderator_yap', 'normal_kullanici_yap'
    ]
    
    inlines = [KullaniciProfilInline]
    
    def kullanici_avatar(self, obj):
        """Kullanıcı avatar veya baş harfleri"""
        if obj.profil_resmi:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;">',
                obj.profil_resmi.url
            )
        else:
            initials = obj.get_initials()
            return format_html(
                '<div style="width: 40px; height: 40px; border-radius: 50%; background: #6366f1; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold;">{}</div>',
                initials
            )
    kullanici_avatar.short_description = _('👤')
    
    def rol_badge(self, obj):
        """Kullanıcı rol badge"""
        colors = {
            'user': '#10b981',
            'moderator': '#f59e0b', 
            'veterinary': '#8b5cf6',
            'admin': '#ef4444'
        }
        color = colors.get(obj.rol, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            color,
            obj.get_rol_display()
        )
    rol_badge.short_description = _('🏷️ Rol')
    
    def durum_badge(self, obj):
        """Kullanıcı durum badge"""
        if obj.durum == 'active':
            return format_html('<span style="color: green;">✅ Aktif</span>')
        elif obj.durum == 'inactive':
            return format_html('<span style="color: orange;">⏸️ Pasif</span>')
        elif obj.durum == 'banned':
            return format_html('<span style="color: red;">🚫 Yasaklı</span>')
        else:
            return format_html('<span style="color: gray;">❓ Bilinmiyor</span>')
    durum_badge.short_description = _('📊 Durum')
    
    def email_dogrulama_badge(self, obj):
        """E-posta doğrulama durumu"""
        if obj.email_dogrulanmis:
            return format_html('<span style="color: green;">✅ Doğrulandı</span>')
        else:
            return format_html('<span style="color: red;">❌ Bekliyor</span>')
    email_dogrulama_badge.short_description = _('📧 E-posta')
    
    def profil_tamamlama(self, obj):
        """Profil tamamlama yüzdesi"""
        percentage = obj.profil_tamamlama_yuzdesi
        color = 'green' if percentage >= 80 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<div style="width: 60px; background: #e5e7eb; border-radius: 8px; overflow: hidden;">'
            '<div style="width: {}%; background: {}; color: white; text-align: center; padding: 2px; font-size: 10px;">{}</div>'
            '</div>',
            percentage, color, f'{percentage}%'
        )
    profil_tamamlama.short_description = _('📊 Profil')
    
    def profil_tamamlama_widget(self, obj):
        """Profil tamamlama detaylı widget"""
        percentage = obj.profil_tamamlama_yuzdesi
        fields = {
            'Ad': obj.first_name,
            'Soyad': obj.last_name,
            'Telefon': obj.telefon,
            'Şehir': obj.sehir,
            'Biyografi': obj.biyografi,
            'Profil Resmi': obj.profil_resmi
        }
        
        html = f'<div style="margin: 10px 0;"><strong>Profil Tamamlama: %{percentage}</strong></div>'
        html += '<ul style="margin: 5px 0;">'
        
        for field_name, field_value in fields.items():
            icon = '✅' if field_value else '❌'
            html += f'<li>{icon} {field_name}</li>'
        
        html += '</ul>'
        return format_html(html)
    profil_tamamlama_widget.short_description = _('📋 Profil Detayı')
    
    def get_queryset(self, request):
        """Optimize edilmiş queryset"""
        return super().get_queryset(request).select_related('profil_detay')
    
    # Actions
    def email_dogrula(self, request, queryset):
        """Seçili kullanıcıların e-postalarını doğrula"""
        count = 0
        for user in queryset:
            if not user.email_dogrulanmis:
                user.email_dogrula()
                count += 1
        
        self.message_user(
            request,
            f'{count} kullanıcının e-postası doğrulandı. ✅'
        )
    email_dogrula.short_description = _('📧 E-postaları doğrula')
    
    def email_dogrulama_iptal(self, request, queryset):
        """E-posta doğrulamalarını iptal et"""
        updated = queryset.update(email_dogrulanmis=False)
        self.message_user(
            request,
            f'{updated} kullanıcının e-posta doğrulaması iptal edildi. ❌'
        )
    email_dogrulama_iptal.short_description = _('❌ E-posta doğrulamalarını iptal et')
    
    def kullanici_aktif_et(self, request, queryset):
        """Kullanıcıları aktif et"""
        updated = queryset.update(durum='active', is_active=True)
        self.message_user(
            request,
            f'{updated} kullanıcı aktif edildi. ✅'
        )
    kullanici_aktif_et.short_description = _('✅ Kullanıcıları aktif et')
    
    def kullanici_pasif_et(self, request, queryset):
        """Kullanıcıları pasif et"""
        updated = queryset.update(durum='inactive', is_active=False)
        self.message_user(
            request,
            f'{updated} kullanıcı pasif edildi. ⏸️'
        )
    kullanici_pasif_et.short_description = _('⏸️ Kullanıcıları pasif et')
    
    def moderator_yap(self, request, queryset):
        """Seçili kullanıcıları moderatör yap"""
        updated = queryset.update(rol='moderator')
        self.message_user(
            request,
            f'{updated} kullanıcı moderatör yapıldı. 🛡️'
        )
    moderator_yap.short_description = _('🛡️ Moderatör yap')
    
    def normal_kullanici_yap(self, request, queryset):
        """Seçili kullanıcıları normal kullanıcı yap"""
        updated = queryset.update(rol='user')
        self.message_user(
            request,
            f'{updated} kullanıcı normal kullanıcı yapıldı. 👤'
        )
    normal_kullanici_yap.short_description = _('👤 Normal kullanıcı yap')


@admin.register(KullaniciProfil)
class KullaniciProfilAdmin(admin.ModelAdmin):
    """
    Kullanıcı profil detayları admin
    """
    
    list_display = [
        'kullanici_link', 'hayvan_deneyimi_yil', 'ev_tipi',
        'bahce_badge', 'kimlik_dogrulama_badge', 'daha_once_sahiplendi'
    ]
    
    list_filter = [
        'ev_tipi', 'bahce_var_mi', 'daha_once_sahiplendin_mi',
        'kimlik_dogrulandi_mi', 'hayvan_deneyimi_yil'
    ]
    
    search_fields = ['kullanici__first_name', 'kullanici__last_name', 'kullanici__email']
    
    def kullanici_link(self, obj):
        """Kullanıcı linkini göster"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:kullanicilar_customuser_change', args=[obj.kullanici.id]),
            obj.kullanici.tam_ad
        )
    kullanici_link.short_description = _('👤 Kullanıcı')
    
    def bahce_badge(self, obj):
        """Bahçe durumu badge"""
        if obj.bahce_var_mi:
            return format_html('<span style="color: green;">🏡 Var</span>')
        return format_html('<span style="color: orange;">🏠 Yok</span>')
    bahce_badge.short_description = _('🏡 Bahçe')
    
    def kimlik_dogrulama_badge(self, obj):
        """Kimlik doğrulama badge"""
        if obj.kimlik_dogrulandi_mi:
            return format_html('<span style="color: green;">✅ Doğrulandı</span>')
        return format_html('<span style="color: red;">❌ Bekliyor</span>')
    kimlik_dogrulama_badge.short_description = _('🆔 Kimlik')
    
    def daha_once_sahiplendi(self, obj):
        """Daha önce sahiplenme durumu"""
        if obj.daha_once_sahiplendin_mi:
            return format_html('<span style="color: green;">✅ Evet</span>')
        return format_html('<span style="color: orange;">❌ İlk kez</span>')
    daha_once_sahiplendi.short_description = _('🐾 Deneyim')


# Admin site özelleştirmeleri
admin.site.site_header = "🐾 Evcil Hayvan Platformu"
admin.site.site_title = "Pet Platform"
admin.site.index_title = "Platform Yönetimi - Her kullanıcı bir hikaye! 💝"

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu admin interface, kullanıcı yönetiminin tüm ihtiyaçlarını karşılar.
# Görsel feedback, detaylı bilgiler ve toplu işlemlerle verimli yönetim.
# 🐾 Her kullanıcının hikayesi, admin panelinde görünür!
