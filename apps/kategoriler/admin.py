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
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Kategori, KategoriOzellik


class KategoriOzellikInline(admin.TabularInline):
    """
    Kategori özelliklerini inline olarak göster
    """
    model = KategoriOzellik
    extra = 1
    fields = ['ad', 'alan_tipi', 'zorunlu', 'aktif', 'sira']
    classes = ['collapse']
    verbose_name = _("Özellik")
    verbose_name_plural = _("Kategori Özellikleri")


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    """
    Kategori admin arayüzü - Standart Django görünümüne yakın
    """
    # Standart liste görünümü
    list_display = [
        'ad', 'parent', 'pet_type_display', 'alt_kategori_sayisi_display',
        'kullanim_sayisi', 'sira', 'aktif'
    ]
    
    list_display_links = ['ad']
    
    # Daha iyi filtreleme seçenekleri
    list_filter = [
        'aktif',
        ('parent', admin.RelatedOnlyFieldListFilter),
        'pet_type',
        ('created_at', admin.DateFieldListFilter),
    ]
    
    # Filtreleme panelinin pozisyonunu değiştir - daha kolay erişim için
    list_filter_position = 'right'
    
    search_fields = ['ad', 'aciklama', 'slug']
    prepopulated_fields = {'slug': ('ad',)}
    
    # Ana kategorilere göre gruplama
    ordering = ['parent__ad', 'sira', 'ad']
    
    # Kategorileri yerinde düzenleme
    list_editable = ['sira', 'aktif']
    
    # Sayfa başına daha az öğe göster (kategoriler artık daha detaylı)
    list_per_page = 25
    
    # İnline kategori özellikleri gösterimi
    inlines = [KategoriOzellikInline]
    
    # Daha mantıklı bir alan gruplaması
    fieldsets = (
        (_('Temel Bilgiler'), {
            'fields': ('ad', 'slug', 'aciklama', 'parent'),
            'classes': ('wide',)
        }),
        (_('Görsel Kimlik'), {
            'fields': ('pet_type', 'ikon_adi', 'renk_kodu'),
            'description': _("Kategorinin görsel kimliğini tanımlayan ayarlar"),
        }),
        (_('Yapılandırma'), {
            'fields': ('aktif', 'sira'),
            'description': _("Kategori davranış ayarları")
        }),
        (_('İstatistikler'), {
            'fields': ('kullanim_sayisi',),
            'classes': ('collapse',),
            'description': _("Bu alanlar otomatik olarak güncellenir")
        }),
    )
    
    readonly_fields = ['kullanim_sayisi']
    
    # Toplu işlemler
    actions = ['aktif_yap', 'pasif_yap', 'istatistikleri_guncelle', 'kopek_irklari_esitle']
    
    def pet_type_display(self, obj):
        """Hayvan türü göster - Türkçe görüntüleme"""
        return obj.get_pet_type_display()
    pet_type_display.short_description = _('Hayvan Türü')
    pet_type_display.admin_order_field = 'pet_type'
    
    def alt_kategori_sayisi_display(self, obj):
        """Alt kategori sayısı göster"""
        count = obj.alt_kategoriler.count()
        if count > 0:
            return format_html(
                '<a href="{}?parent__id__exact={}">{}</a>',
                reverse('admin:kategoriler_kategori_changelist'),
                obj.id, count
            )
        return '-'
    alt_kategori_sayisi_display.short_description = _('Alt Kategori')
    
    # Optimize edilmiş queryset (hız için)
    def get_queryset(self, request):
        return (super().get_queryset(request)
                .select_related('parent')
                .prefetch_related('alt_kategoriler')
                .annotate(
                    alt_kategori_count=Count('alt_kategoriler')
                ))
    
    # Yönetici işlemleri
    def aktif_yap(self, request, queryset):
        updated = queryset.update(aktif=True)
        self.message_user(
            request, 
            _('{} kategori aktif edildi').format(updated)
        )
    aktif_yap.short_description = _('Seçili kategorileri aktifleştir')
    
    def pasif_yap(self, request, queryset):
        updated = queryset.update(aktif=False)
        self.message_user(
            request, 
            _('{} kategori pasif edildi').format(updated)
        )
    pasif_yap.short_description = _('Seçili kategorileri pasifleştir')
    
    def istatistikleri_guncelle(self, request, queryset):
        for kategori in queryset:
            from .servisler import KategoriService
            KategoriService.kategori_kullanim_guncelle(kategori.id)
            
        self.message_user(
            request,
            _('{} kategorinin istatistikleri güncellendi').format(queryset.count())
        )
    istatistikleri_guncelle.short_description = _('İstatistikleri güncelle')
    
    def kopek_irklari_esitle(self, request, queryset):
        """Köpek ırkları ile kategorileri eşitler"""
        # Sadece Köpekler kategorisi ve alt kategorileri için çalışır
        kopekler = queryset.filter(ad__iexact='Köpekler', parent__isnull=True).first()
        if not kopekler:
            self.message_user(request, _("Lütfen 'Köpekler' ana kategorisini seçin"), level='WARNING')
            return
        
        try:
            from apps.hayvanlar.models import KopekIrk
            
            # Popüler köpek ırklarını getir ve alt kategoriler olarak ekle
            populer_irklar = KopekIrk.objects.filter(aktif=True, populer=True)
            added = 0
            
            for irk in populer_irklar:
                # Bu ırk için kategori var mı?
                alt_kategori = Kategori.objects.filter(
                    parent=kopekler,
                    ad__iexact=irk.ad
                ).first()
                
                if not alt_kategori:
                    # Oluştur - pet_type değerini düzelt
                    from django.utils.text import slugify
                    Kategori.objects.create(
                        ad=irk.ad,
                        slug=f"kopekler-{slugify(irk.ad)}",
                        parent=kopekler,
                        pet_type='kopek',  # 'dog' yerine 'kopek' kullan
                        renk_kodu=kopekler.renk_kodu,
                        aciklama=irk.aciklama or f"{irk.ad} ırkı köpekler",
                        aktif=True
                    )
                    added += 1
            
            self.message_user(
                request, 
                _(f"{added} yeni köpek ırkı kategorilere eklendi. Toplam {populer_irklar.count()} popüler ırk var.")
            )
            
        except Exception as e:
            self.message_user(
                request, 
                _(f"Bir hata oluştu: {str(e)}"), 
                level='ERROR'
            )
    
    kopek_irklari_esitle.short_description = _("Popüler köpek ırklarını kategorilere ekle")
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Form alanı özelleştirme - Ana kategorileri filtreleme"""
        if db_field.name == "parent":
            # Sadece ana kategorileri veya hiç kategoriyi göster
            kwargs["queryset"] = Kategori.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Ana kategori veya alt kategori olmasına göre form alanlarını düzenle
        if obj and obj.parent is None:
            # Ana kategori ise
            form.base_fields['pet_type'].help_text = _("Ana kategori için hayvan türü belirleyiniz.")
        else:
            # Alt kategori ise
            if 'pet_type' in form.base_fields:
                form.base_fields['pet_type'].disabled = True
                form.base_fields['pet_type'].help_text = _("Alt kategorilerde tür ana kategoriden otomatik devralınır.")
        
        return form
    
    # Kategori eklerken daha iyi bir kullanıcı deneyimi için yardımcı metin
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _('Yeni Kategori Ekle')
        extra_context['help_text'] = _(
            """<div class="help" style="margin: 10px 0; padding: 10px; background: #f7f7f7; border-left: 4px solid #79aec8;">
            <h3 style="margin-top: 0;">Kategori Oluşturma Rehberi</h3>
            <p><strong>Ana kategori eklemek için:</strong> "Ana Kategori" alanını boş bırakın ve "Hayvan Türü" seçin.</p>
            <p><strong>Alt kategori (ırk/cins) eklemek için:</strong> "Ana Kategori" seçin. Tür otomatik devralınacaktır.</p>
            <p>Örnek: "Köpekler" (Ana kategori) > "Golden Retriever" (Alt kategori)</p>
            </div>"""
        )
        return super().add_view(request, form_url, extra_context)
    

@admin.register(KategoriOzellik)
class KategoriOzellikAdmin(admin.ModelAdmin):
    """
    Kategori özellik admin arayüzü
    """
    
    list_display = [
        'ad', 'kategori', 'alan_tipi', 'zorunlu', 'aktif',
        'sira', 'created_at'
    ]
    
    list_filter = [
        'zorunlu', 
        'aktif', 
        ('kategori', admin.RelatedOnlyFieldListFilter),  # Sadece ilişkili kategorileri göster
        'alan_tipi'
    ]
    
    search_fields = ['ad', 'kategori__ad']
    
    ordering = ['kategori__ad', 'sira', 'ad']
    
    list_editable = ['zorunlu', 'aktif']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Form alanlarında sadece ana kategorileri göster"""
        if db_field.name == "kategori":
            # Sadece ana kategorileri (parent=None) göster
            kwargs["queryset"] = Kategori.objects.filter(
                parent__isnull=True,
                aktif=True
            ).order_by('sira', 'ad')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        """Form özelleştirmeleri"""
        form = super().get_form(request, obj, **kwargs)
        
        # Kategori seçimi için yardım metni
        if 'kategori' in form.base_fields:
            form.base_fields['kategori'].help_text = _(
                "Sadece ana kategoriler görüntülenir. Alt kategoriler için özellik tanımlanamaz."
            )
        
        return form


# Admin site özelleştirmeleri
admin.site.site_header = "🐾 Evcil Hayvan Platformu Yönetimi"
admin.site.site_title = "Pet Platform"
admin.site.index_title = "Platform Yönetimi"
