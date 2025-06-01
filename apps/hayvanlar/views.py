"""
🐾 Evcil Hayvan Platformu - Hayvan Görünümleri
==============================================================================
Hayvanlarla ilgili API endpoint'leri
==============================================================================
"""

from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from rest_framework import viewsets, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.ortak.pagination import StandardPagination
from .models import Hayvan, HayvanFotograf, KopekIrk
from .serializers import (
    HayvanListSerializer, HayvanDetailSerializer, 
    HayvanCreateUpdateSerializer, HayvanFotografEkleSerializer,
    KopekIrkSerializer
)
from .filters import HayvanFilter


class HayvanViewSet(viewsets.ModelViewSet):
    """
    Hayvan ViewSet - Platformdaki hayvanların yönetimi
    
    Her hayvanın kendine özgü hikayesi ve karakteri var.
    """
    queryset = Hayvan.objects.filter(aktif=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HayvanFilter
    search_fields = ['ad', 'aciklama', 'irk__ad', 'kategori__ad']
    ordering_fields = ['created_at', 'ad', 'yas']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return HayvanListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return HayvanCreateUpdateSerializer
        else:
            return HayvanDetailSerializer
    
    def get_queryset(self):
        """Optimizasyonlar ve filtreler"""
        queryset = self.queryset
        
        # Detay görünümü için ilişkileri prefetch et
        if self.action == 'retrieve':
            queryset = queryset.select_related(
                'kategori', 'irk'
            ).prefetch_related('fotograflar')
        
        # Liste görünümü için kapak fotoğrafı prefetch et
        elif self.action == 'list':
            queryset = queryset.select_related('irk')
        
        return queryset
    
    @action(detail=True, methods=['post'], 
            permission_classes=[IsAuthenticated],
            parser_classes=[parsers.MultiPartParser])
    def fotograf_ekle(self, request, pk=None):
        """
        Hayvana fotoğraf ekle
        """
        hayvan = self.get_object()
        serializer = HayvanFotografEkleSerializer(data=request.data)
        
        if serializer.is_valid():
            # Eğer bu kapak fotoğrafı olarak işaretlendiyse diğerlerini kaldır
            if serializer.validated_data.get('kapak_fotografi'):
                HayvanFotograf.objects.filter(
                    hayvan=hayvan, kapak_fotografi=True
                ).update(kapak_fotografi=False)
            
            # Fotoğrafı kaydet
            HayvanFotograf.objects.create(
                hayvan=hayvan,
                **serializer.validated_data
            )
            
            return Response({
                'success': True,
                'message': _('Fotoğraf başarıyla eklendi')
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False)
    def populer(self, request):
        """En popüler hayvanlar"""
        # Burada popülerlik kriterlerine göre hayvanlar listelenebilir
        # Örneğin en çok görüntülenen, favori eklenen vb.
        queryset = self.get_queryset().order_by('-created_at')[:10]
        serializer = HayvanListSerializer(
            queryset, many=True, context={'request': request}
        )
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Popüler hayvanlar listelendi')
        })
    
    @action(detail=False)
    def son_eklenenler(self, request):
        """Son eklenen hayvanlar"""
        queryset = self.get_queryset().order_by('-created_at')[:10]
        serializer = HayvanListSerializer(
            queryset, many=True, context={'request': request}
        )
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Son eklenen hayvanlar listelendi')
        })


class KopekIrkViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Köpek ırkları için ReadOnly ViewSet
    Irk ekleme/değiştirme sadece admin panelinden yapılabilir
    """
    queryset = KopekIrk.objects.filter(aktif=True)
    serializer_class = KopekIrkSerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['ad', 'aciklama']
    ordering_fields = ['ad']
    ordering = ['ad']
    
    @action(detail=False)
    def populer(self, request):
        """Popüler köpek ırkları"""
        queryset = self.queryset.filter(populer=True)
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Popüler köpek ırkları')
        })
    
    @action(detail=False)
    def yerli(self, request):
        """Yerli köpek ırkları"""
        queryset = self.queryset.filter(yerli=True)
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Yerli köpek ırkları')
        })
