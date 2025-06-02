"""
🐾 Evcil Hayvan Platformu - Hayvan Admin Modülü
==============================================================================
Hayvan kayıtları ve köpek ırkları yönetim arayüzü
==============================================================================
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django import forms  # Bu import'u ekle
from .models import KopekIrk, Hayvan, HayvanFotograf


class HayvanFotografInline(admin.TabularInline):
    """Hayvan fotoğrafları için inline admin"""
    model = HayvanFotograf
    extra = 1
    fields = ['fotograf', 'thumbnail', 'kapak_fotografi', 'sira']
    readonly_fields = ['thumbnail']
    classes = ['collapse']


class HayvanlarAppAdminSite(admin.AdminSite):
    """Özel admin site için hayvan yönetim alanı"""
    site_header = "🐾 Evcil Hayvan Kayıtları Yönetimi"
    site_title = "Hayvan Kayıtları"
    index_title = "Hayvan Yönetimi"


@admin.register(KopekIrk)
class KopekIrkAdmin(admin.ModelAdmin):
    """
    Köpek ırkları admin arayüzü - İyileştirilmiş
    """
    # list_editable içindeki alanları list_display'e de eklemeliyiz
    list_display = [
        'id', 'irk_adi_display', 'populer', 'yerli', 'aktif',
        'populer_badge', 'yerli_badge', 'aktif_badge'
    ]
    list_filter = [
        'populer', 
        'yerli', 
        'aktif',
        # Alfabetik filtreleme ekle
        ('ad', admin.AllValuesFieldListFilter)
    ]
    search_fields = ['ad', 'aciklama']
    list_editable = ['populer', 'yerli', 'aktif']
    list_per_page = 25
    
    # Arama performansını artır
    search_help_text = "Irk adı veya açıklamada arama yapın"
    
    fieldsets = (
        (_('Temel Bilgiler'), {
            'fields': ('id', 'ad', 'aciklama'),
            'classes': ('wide',)
        }),
        (_('Özellikler'), {
            'fields': ('populer', 'yerli', 'aktif'),
            'description': _("Bu özellikler, ırkın platform üzerinde nasıl gösterileceğini belirler.")
        })
    )
    
    actions = ['populer_yap', 'yerli_yap', 'aktif_yap', 'pasif_yap']
    
    # Görsel iyileştirmeler
    def irk_adi_display(self, obj):
        """Irk adını vurgulu göster"""
        return format_html('<strong>{}</strong>', obj.ad)
    irk_adi_display.short_description = _("Irk Adı")
    irk_adi_display.admin_order_field = 'ad'
    
    def populer_badge(self, obj):
        """Popüler durumunu rozet olarak göster"""
        if obj.populer:
            return format_html('<span style="background-color:#fbbf24; color:#000; padding:2px 8px; border-radius:12px;">Popüler</span>')
        return ""
    populer_badge.short_description = _("Popüler")
    
    def yerli_badge(self, obj):
        """Yerli durumunu rozet olarak göster"""
        if obj.yerli:
            return format_html('<span style="background-color:#ef4444; color:#fff; padding:2px 8px; border-radius:12px;">Yerli</span>')
        return ""
    yerli_badge.short_description = _("Yerli")
    
    def aktif_badge(self, obj):
        """Aktif durumunu rozet olarak göster"""
        if obj.aktif:
            return format_html('<span style="color:green;">✓</span>')
        return format_html('<span style="color:red;">✗</span>')
    aktif_badge.short_description = _("Aktif")
    
    # Yeni action'lar
    def aktif_yap(self, request, queryset):
        """Seçili ırkları aktif yap"""
        updated = queryset.update(aktif=True)
        self.message_user(request, f'{updated} ırk aktif olarak işaretlendi.')
    aktif_yap.short_description = _("Seçili ırkları aktif yap")
    
    def pasif_yap(self, request, queryset):
        """Seçili ırkları pasif yap"""
        updated = queryset.update(aktif=False)
        self.message_user(request, f'{updated} ırk pasif olarak işaretlendi.')
    pasif_yap.short_description = _("Seçili ırkları pasif yap")
    
    def populer_yap(self, request, queryset):
        """Seçili ırkları popüler yap"""
        updated = queryset.update(populer=True)
        self.message_user(request, f'{updated} ırk popüler olarak işaretlendi.')
    populer_yap.short_description = "Seçili ırkları popüler yap"
    
    def yerli_yap(self, request, queryset):
        """Seçili ırkları yerli yap"""
        updated = queryset.update(yerli=True)
        self.message_user(request, f'{updated} ırk yerli olarak işaretlendi.')
    yerli_yap.short_description = "Seçili ırkları yerli olarak işaretle"

@admin.register(Hayvan)
class HayvanAdmin(admin.ModelAdmin):
    """
    Hayvanlar ana modeli admin arayüzü - İyileştirilmiş
    """
    list_display = [
        'ad', 'kapak_foto', 'tur_badge', 'cins_bilgisi',
        'cinsiyet_badge', 'yas_bilgisi', 'sahiplenildi_badge'
    ]
    list_filter = [
        'tur', 
        'cinsiyet',
        'yas', 
        'sahiplenildi',
        'aktif',
        ('kategori', admin.RelatedOnlyFieldListFilter),
        ('il', admin.AllValuesFieldListFilter),  # İl filtresini güncelle
        ('ilce', admin.AllValuesFieldListFilter)  # İlçe filtresi de ekle
    ]
    
    search_fields = ['ad', 'aciklama', 'irk__ad', 'il', 'ilce']
    
    # Hızlı arama yardımcı metni
    search_help_text = "Hayvan adı, açıklama, ırk, il veya ilçede arama yapın"
    
    # İnline fotoğraflar
    inlines = [HayvanFotografInline]
    
    # Daha mantıksal bir alan gruplaması
    fieldsets = (
        (_('📋 Temel Bilgiler'), {
            'fields': ('ad', 'tur', 'kategori', 'irk'),
            'classes': ('wide',),
        }),
        (_('🐾 Hayvan Detayları'), {
            'fields': ('yas', 'cinsiyet', 'boyut', 'renk'),
            'classes': ('wide',),
        }),
        (_('💉 Sağlık Bilgileri'), {
            'fields': ('kisirlastirilmis', 'asilar_tamam', 'mikrocipli'),
            'classes': ('collapse',),
        }),
        (_('💭 Karakteristikler'), {
            'fields': ('karakter_ozellikleri', 'aciklama'),
            'classes': ('collapse',),
        }),
        (_('📍 Konum Bilgisi'), {
            'fields': ('il', 'ilce'),
            'classes': ('collapse',),
        }),
        (_('⚙️ Durum'), {
            'fields': ('aktif', 'sahiplenildi'),
            'classes': ('collapse',),
        })
    )
    
    # Salt-okunur alanlar ve otomatik slug (prepopulated_fields kaldırıldı)
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    # UI İyileştirmeleri
    def kapak_foto(self, obj):
        """Kapak fotoğrafını thumbnail olarak göster"""
        if obj.kapak_fotografi:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:8px;" />',
                obj.kapak_fotografi.thumbnail.url if obj.kapak_fotografi.thumbnail else obj.kapak_fotografi.fotograf.url
            )
        return format_html('<span style="color:#888;">🖼️</span>')
    kapak_foto.short_description = ""
    
    def tur_badge(self, obj):
        """Hayvan türünü renkli rozetle göster"""
        tur_renkler = {
            'kopek': '#f59e0b',
            'kedi': '#8b5cf6',
            'kus': '#06b6d4',
            'balik': '#3b82f6',
            'kemirgen': '#f97316',
            'surungen': '#059669',
            'diger': '#6b7280'
        }
        renk = tur_renkler.get(obj.tur, '#6b7280')
        return format_html(
            '<span style="background-color:{}; color:white; padding:2px 8px; border-radius:12px;">{}</span>',
            renk,
            obj.get_tur_display()
        )
    tur_badge.short_description = _("Tür")
    
    def cins_bilgisi(self, obj):
        """Irk ve kategori bilgisini birleştir"""
        if obj.irk:
            return format_html('{} / <span style="color:#666;">{}</span>', obj.irk.ad, obj.kategori.ad if obj.kategori else '-')
        return obj.kategori.ad if obj.kategori else '-'
    cins_bilgisi.short_description = _("Cins / Kategori")
    
    def cinsiyet_badge(self, obj):
        """Cinsiyeti görsel olarak göster"""
        if obj.cinsiyet == 'male':
            return format_html('<span style="color:#3b82f6;">♂️ Erkek</span>')
        elif obj.cinsiyet == 'female':
            return format_html('<span style="color:#ec4899;">♀️ Dişi</span>')
        return format_html('<span style="color:#6b7280;">❓</span>')
    cinsiyet_badge.short_description = _("Cinsiyet")
    
    def yas_bilgisi(self, obj):
        """Yaş bilgisini göster"""
        if obj.yas:
            return obj.get_yas_display()
        return "-"
    yas_bilgisi.short_description = _("Yaş")
    
    def sahiplenildi_badge(self, obj):
        """Sahiplenilme durumunu rozet olarak göster"""
        if obj.sahiplenildi:
            return format_html('<span style="background-color:#10b981; color:white; padding:2px 8px; border-radius:12px;">Sahiplenildi</span>')
        return format_html('<span style="background-color:#6b7280; color:white; padding:2px 8px; border-radius:12px;">Sahiplendirme</span>')
    sahiplenildi_badge.short_description = _("Durum")
    
    # Köpek ırkı ve kategori ilişkisi için otomatik doldur
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # İl seçimi için Türkiye illeri dropdown
        if 'il' in form.base_fields:
            # Basit il seçenekleri
            il_choices = [
                ('', '------'),
                ('istanbul', 'İstanbul'),
                ('ankara', 'Ankara'),
                ('izmir', 'İzmir'),
                ('bursa', 'Bursa'),
                ('antalya', 'Antalya'),
                ('konya', 'Konya'),
                ('adana', 'Adana'),
                ('gaziantep', 'Gaziantep'),
                ('mersin', 'Mersin'),
                ('kayseri', 'Kayseri'),
            ]
            form.base_fields['il'] = forms.ChoiceField(
                choices=il_choices,
                required=False,
                label='İl'
            )
        
        return form
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        
        # Köpek ırkları ve kategoriler arasındaki eşleşmeyi gösteren JavaScript ekle
        extra_context['media'] = (extra_context.get('media', '') + 
        '''
        <script>
        function updateCategoryBasedOnBreed(breedId) {
            if (!breedId) return;
            
            // AJAX ile ırka uygun kategoriyi sor
            fetch('/api/v1/hayvanlar/kopek-irklari/' + breedId + '/')
                .then(response => response.json())
                .then(data => {
                    // Köpekler kategorisini bul
                    fetch('/api/v1/kategoriler/ana_kategoriler/')
                        .then(resp => resp.json())
                        .then(cats => {
                            const dogCat = cats.data.find(c => c.ad === 'Köpekler');
                            if (dogCat) {
                                // Alt kategorileri getir
                                fetch('/api/v1/kategoriler/' + dogCat.id + '/alt_kategoriler/')
                                    .then(resp => resp.json())
                                    .then(subs => {
                                        // Irkla eşleşen kategoriyi bul
                                        const matchingCat = subs.data.find(
                                            s => s.ad.toLowerCase() === data.ad.toLowerCase()
                                        );
                                        
                                        if (matchingCat) {
                                            // Kategori select'i güncelle
                                            const catSelect = document.getElementById('id_kategori');
                                            for (let i=0; i < catSelect.options.length; i++) {
                                                if (catSelect.options[i].value == matchingCat.id) {
                                                    catSelect.selectedIndex = i;
                                                    break;
                                                }
                                            }
                                        }
                                    });
                            }
                        });
                });
        }
        </script>
        ''')
        
        return super().change_view(request, object_id, form_url, extra_context)
# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu admin arayüzü, köpek ırklarının yönetimini kolaylaştırır.
# Her ırkın kendine özgü özellikleri ve hikayesi var.
# 🐾 Köpek ırkları, platformun sadık dostlarının dijital temsilcileri!