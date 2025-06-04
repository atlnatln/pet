"""
🏷️ Evcil Hayvan Platformu - Etiketler Views
==============================================================================
Etiket API görünümleri ve viewsetler
==============================================================================
"""

from rest_framework import viewsets, mixins, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Etiket
from .serializers import (
    EtiketSerializer, 
    EtiketCreateUpdateSerializer, 
    EtiketDetailSerializer
)
from .filters import EtiketFilter

from .models import Etiket
from .serializers import (
    EtiketSerializer, 
    EtiketCreateUpdateSerializer, 
    EtiketDetailSerializer
)


@extend_schema_view(
    list=extend_schema(summary="Etiketleri listele", description="Tüm aktif etiketleri listeler."),
    retrieve=extend_schema(summary="Etiket detayını getir", description="Belirtilen ID'ye sahip etiketin detay bilgilerini getirir."),
    create=extend_schema(summary="Yeni etiket oluştur", description="Yeni bir etiket oluşturur."),
    update=extend_schema(summary="Etiketi güncelle", description="Belirtilen ID'ye sahip etiketi günceller."),
    partial_update=extend_schema(summary="Etiketi kısmi güncelle", description="Belirtilen ID'ye sahip etiketi kısmen günceller."),
    destroy=extend_schema(summary="Etiketi sil", description="Belirtilen ID'ye sahip etiketi siler."),
)
class EtiketViewSet(viewsets.ModelViewSet):
    """Etiketler için API endpoint'leri"""
    queryset = Etiket.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ad', 'aciklama']
    ordering_fields = ['ad', 'olusturma_tarihi', 'kullanim_sayisi']
    ordering = ['ad']
    
    def get_serializer_class(self):
        """İşleme göre uygun serializer seç"""
        if self.action == 'retrieve':
            return EtiketDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EtiketCreateUpdateSerializer
        return EtiketSerializer
    
    def get_queryset(self):
        """Etiketleri kullanım sayısı bilgisiyle birlikte getir"""
        queryset = Etiket.objects.annotate(
            kullanim_sayisi=Count('hayvanlar', distinct=True) + Count('ilanlar', distinct=True)
        )
        return queryset
    
    @extend_schema(summary="Popüler etiketleri listele")
    @action(detail=False, methods=['get'])
    def populer(self, request):
        """En popüler etiketleri döndürür"""
        populer_etiketler = Etiket.objects.en_populer(limit=10)
        serializer = self.get_serializer(populer_etiketler, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary="Harfe göre etiketleri listele")
    @action(detail=False, methods=['get'])
    def harfe_gore(self, request):
        """Belirli bir harfle başlayan etiketleri döndürür"""
        harf = request.query_params.get('harf', 'a')
        # Sadece tek harf kabul et
        if len(harf) > 1:
            harf = harf[0]
            
        etiketler = Etiket.objects.harf_ile_baslayan(harf)
        serializer = self.get_serializer(etiketler, many=True)
        return Response({
            'harf': harf,
            'etiketler': serializer.data
        })
        
    @extend_schema(summary="Pasif etiketleri aktifleştir")
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def aktiflestir(self, request, pk=None):
        """Pasif etiketi aktif hale getirir"""
        etiket = self.get_object()
        if etiket.aktif:
            return Response(
                {'detail': _("Bu etiket zaten aktif.")},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        etiket.aktif = True
        etiket.save()
        return Response({'detail': _("Etiket başarıyla aktifleştirildi.")})
    
    @extend_schema(summary="Etiketi pasifleştir")
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def pasif_yap(self, request, pk=None):
        """Aktif etiketi pasif hale getirir"""
        etiket = self.get_object()
        if not etiket.aktif:
            return Response(
                {'detail': _("Bu etiket zaten pasif.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Etiket kullanımda mı kontrol et
        if etiket.kullanim_sayisi > 0:
            return Response(
                {'detail': _("Bu etiket kullanımda olduğu için pasifleştirilemez.")},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        etiket.aktif = False
        etiket.save()
        return Response({'detail': _("Etiket başarıyla pasifleştirildi.")})