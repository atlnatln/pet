"""
🐾 Kategoriler API Views
==============================================================================
Kategori endpoint'leri - Her kategorinin hikayesini API'de anlatıyoruz
==============================================================================
"""

from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Count, Prefetch
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.ortak.pagination import StandardPagination
from apps.ortak.permissions import IsOwnerOrReadOnly
from .models import Kategori, KategoriOzellik
from .serializers import (
    KategoriBasicSerializer, KategoriDetailSerializer, 
    KategoriTreeSerializer, KategoriStatsSerializer,
    KategoriCreateUpdateSerializer, KategoriFilterSerializer
)


class KategoriViewSet(viewsets.ModelViewSet):
    """
    Kategori ViewSet - Hayvan türlerinin dijital yönetimi
    
    Kategoriler, platformdaki her hayvanın hikayesinin başlığıdır.
    Bu ViewSet ile kategorileri keşfet, yönet ve filtrele.
    """
    
    queryset = Kategori.objects.aktif().select_related('parent').prefetch_related('alt_kategoriler')
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['ad', 'aciklama']
    ordering_fields = ['ad', 'sira', 'kullanim_sayisi', 'olusturulma_tarihi']
    ordering = ['sira', 'ad']
    
    def get_serializer_class(self):
        """Her action için uygun serializer seç"""
        if self.action == 'list':
            return KategoriBasicSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return KategoriCreateUpdateSerializer
        else:
            return KategoriDetailSerializer
    
    def get_queryset(self):
        """Optimize edilmiş queryset"""
        queryset = self.queryset
        
        # Prefetch optimizasyonları
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related(
                'ozellikler',
                Prefetch('alt_kategoriler', queryset=Kategori.objects.aktif())
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Kategori listesi
        
        Tüm aktif kategorileri listele. Filtreleme ve arama destekli.
        """
        # Cache key oluştur
        cache_key = f"kategoriler:list:{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        
        # Başarılı response'u cache'le
        if response.status_code == 200:
            cache.set(cache_key, response.data, 900)  # 15 dakika
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """
        Kategori detayı
        
        Belirli bir kategorinin tüm detaylarını getir.
        Alt kategoriler ve özellikler dahil.
        """
        instance = self.get_object()
        
        # Cache key
        cache_key = f"kategori:detail:{instance.slug}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        
        # Cache'le
        cache.set(cache_key, response_data, 1800)  # 30 dakika
        
        return Response(response_data)
    
    @action(detail=False, methods=['get'])
    def ana_kategoriler(self, request):
        """
        Ana kategoriler
        
        Sadece ana kategorileri (parent=None) getir.
        Hızlı kategori seçimi için optimize edilmiş.
        """
        ana_kategoriler = Kategori.objects.ana_kategoriler()
        
        # Cache'den kontrol et
        cache_key = "kategoriler:ana_kategoriler:api"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response({
                'success': True,
                'data': cached_data,
                'message': _('Ana kategoriler listelendi')
            })
        
        serializer = KategoriBasicSerializer(ana_kategoriler, many=True)
        
        # Cache'le
        cache.set(cache_key, serializer.data, 3600)  # 1 saat
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Ana kategoriler listelendi'),
            'count': len(serializer.data)
        })
    
    @action(detail=False, methods=['get'])
    def kategori_agaci(self, request):
        """
        Kategori ağacı
        
        Tüm kategorileri hiyerarşik yapıda getir.
        Alt kategoriler ana kategorilerin altında nested.
        """
        cache_key = "kategoriler:agac:api"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response({
                'success': True,
                'data': cached_data,
                'message': _('Kategori ağacı getirildi')
            })
        
        # Ana kategorileri ve alt kategorilerini prefetch ile getir
        ana_kategoriler = (
            Kategori.objects.aktif()
            .ana_kategoriler()
            .prefetch_related(
                Prefetch('alt_kategoriler', queryset=Kategori.objects.aktif())
            )
            .order_by('sira', 'ad')
        )
        
        serializer = KategoriTreeSerializer(ana_kategoriler, many=True)
        
        # Cache'le
        cache.set(cache_key, serializer.data, 1800)  # 30 dakika
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Kategori ağacı getirildi'),
            'count': len(serializer.data)
        })
    
    @action(detail=True, methods=['get'])
    def alt_kategoriler(self, request, pk=None):
        """
        Belirli kategorinin alt kategorileri
        
        Bir ana kategorinin altındaki tüm alt kategorileri getir.
        """
        kategori = self.get_object()
        
        cache_key = f"kategori:{kategori.slug}:alt_kategoriler"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response({
                'success': True,
                'data': cached_data,
                'message': _('Alt kategoriler listelendi')
            })
        
        alt_kategoriler = kategori.alt_kategoriler.filter(aktif=True).order_by('sira', 'ad')
        serializer = KategoriBasicSerializer(alt_kategoriler, many=True)
        
        # Cache'le
        cache.set(cache_key, serializer.data, 1800)  # 30 dakika
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _(f'{kategori.ad} kategorisinin alt kategorileri'),
            'parent': {
                'id': kategori.id,
                'ad': kategori.ad,
                'slug': kategori.slug
            },
            'count': len(serializer.data)
        })
    
    @action(detail=False, methods=['get'])
    def populer(self, request):
        """
        Popüler kategoriler
        
        En çok kullanılan kategorileri getir.
        Kullanım sayısına göre sıralı.
        """
        limit = int(request.query_params.get('limit', 10))
        populer_kategoriler = Kategori.objects.populer_kategoriler(limit)
        
        return Response({
            'success': True,
            'data': populer_kategoriler,
            'message': _('Popüler kategoriler listelendi'),
            'count': len(populer_kategoriler)
        })
    
    @action(detail=False, methods=['get'])
    def istatistikler(self, request):
        """
        Kategori istatistikleri
        
        Platform genelindeki kategori istatistiklerini getir.
        """
        cache_key = "kategoriler:istatistikler"
        cached_stats = cache.get(cache_key)
        
        if cached_stats:
            return Response({
                'success': True,
                'data': cached_stats,
                'message': _('Kategori istatistikleri getirildi')
            })
        
        # İstatistikleri hesapla
        total_kategoriler = Kategori.objects.aktif().count()
        ana_kategoriler = Kategori.objects.aktif().ana_kategoriler().count()
        alt_kategoriler = Kategori.objects.aktif().alt_kategoriler().count()
        
        # Pet type dağılımı
        pet_type_dagilimi = dict(
            Kategori.objects.aktif()
            .values('pet_type')
            .annotate(count=Count('id'))
            .values_list('pet_type', 'count')
        )
        
        # Popüler kategoriler
        populer = Kategori.objects.populer_kategoriler(5)
        
        stats_data = {
            'toplam_kategori': total_kategoriler,
            'ana_kategori_sayisi': ana_kategoriler,
            'alt_kategori_sayisi': alt_kategoriler,
            'pet_type_dagilimi': pet_type_dagilimi,
            'populer_kategoriler': populer
        }
        
        serializer = KategoriStatsSerializer(stats_data)
        
        # Cache'le
        cache.set(cache_key, serializer.data, 3600)  # 1 saat
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Kategori istatistikleri getirildi')
        })
    
    @action(detail=False, methods=['post'])
    def filtrele(self, request):
        """
        Gelişmiş kategori filtreleme
        
        POST ile gönderilen filtrelere göre kategorileri getir.
        """
        filter_serializer = KategoriFilterSerializer(data=request.data)
        filter_serializer.is_valid(raise_exception=True)
        
        filters = filter_serializer.validated_data
        queryset = Kategori.objects.aktif()
        
        # Filtreleri uygula
        if filters.get('pet_type'):
            queryset = queryset.filter(pet_type=filters['pet_type'])
        
        if filters.get('parent') is not None:
            queryset = queryset.filter(parent_id=filters['parent'])
        
        if filters.get('arama'):
            search_term = filters['arama']
            queryset = queryset.filter(
                Q(ad__icontains=search_term) |
                Q(aciklama__icontains=search_term)
            )
        
        # Sayfalama uygula
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = KategoriBasicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = KategoriBasicSerializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Filtreleme tamamlandı'),
            'count': len(serializer.data)
        })
    
    def perform_create(self, serializer):
        """Kategori oluştururken cache temizle"""
        serializer.save()
        self._clear_category_cache()
    
    def perform_update(self, serializer):
        """Kategori güncellerken cache temizle"""
        serializer.save()
        self._clear_category_cache()
    
    def perform_destroy(self, instance):
        """Kategori silerken cache temizle"""
        super().perform_destroy(instance)
        self._clear_category_cache()
    
    def _clear_category_cache(self):
        """Kategori cache'lerini temizle"""
        cache_patterns = [
            "kategoriler:*",
            "kategori:*"
        ]
        
        # Redis backend kullanıyorsak pattern ile temizle
        try:
            from django_redis import get_redis_connection
            conn = get_redis_connection("default")
            for pattern in cache_patterns:
                keys = conn.keys(pattern)
                if keys:
                    conn.delete(*keys)
        except:
            # Fallback: tüm cache'i temizle
            cache.clear()

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu ViewSet, kategori sisteminin tüm API ihtiyaçlarını karşılar.
# Cache stratejileri ile hızlı, filtreleme ile esnek, 
# hiyerarşik yapı ile kullanıcı dostu bir API sunar.
# 🐾 Her endpoint, kategorilerin hikayesini anlatır!
