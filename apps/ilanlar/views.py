"""
📢 İlanlar Views
==============================================================================
Sahiplendirme ilanları için API endpoint'leri
==============================================================================
"""

from django.utils.translation import gettext_lazy as _
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.ortak.pagination import StandardPagination
from .models import Ilan, IlanBasvuru
from .serializers import (
    IlanListSerializer, IlanDetailSerializer, IlanCreateSerializer,
    IlanBasvuruSerializer
)
from .filters import IlanFilter


class IlanViewSet(viewsets.ModelViewSet):
    """İlan ViewSet - Yuva arayan dostların dijital vitrinleri"""
    
    queryset = Ilan.objects.filter(durum='aktif')
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = IlanFilter
    search_fields = ['baslik', 'aciklama', 'ilan_veren_adi']
    ordering_fields = ['created_at', 'yayinlanma_tarihi', 'goruntulenme_sayisi']
    ordering = ['-acil', '-yayinlanma_tarihi']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return IlanListSerializer
        elif self.action == 'create':
            return IlanCreateSerializer
        else:
            return IlanDetailSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        
        if self.action == 'retrieve':
            queryset = queryset.select_related('hayvan').prefetch_related('fotograflar')
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """İlan detayını getir ve görüntülenme sayısını artır"""
        instance = self.get_object()
        
        # Görüntülenme sayısını artır
        Ilan.objects.filter(id=instance.id).update(
            goruntulenme_sayisi=models.F('goruntulenme_sayisi') + 1
        )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False)
    def acil_ilanlar(self, request):
        """Acil sahiplendirme ilanları"""
        queryset = self.get_queryset().filter(acil=True)[:10]
        serializer = IlanListSerializer(queryset, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Acil ilanlar listelendi')
        })
    
    @action(detail=False)
    def son_ilanlar(self, request):
        """Son eklenen ilanlar"""
        queryset = self.get_queryset().order_by('-yayinlanma_tarihi')[:10]
        serializer = IlanListSerializer(queryset, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Son ilanlar listelendi')
        })
    
    @action(detail=True, methods=['post'])
    def basvuru_yap(self, request, pk=None):
        """İlana başvuru yap"""
        ilan = self.get_object()
        
        # Başvuru verilerini hazırla
        basvuru_data = request.data.copy()
        basvuru_data['ilan'] = ilan.id
        
        serializer = IlanBasvuruSerializer(data=basvuru_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': _('Başvurunuz alınmıştır')
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IlanBasvuruViewSet(viewsets.ReadOnlyModelViewSet):
    """İlan başvuruları için read-only ViewSet"""
    
    queryset = IlanBasvuru.objects.all()
    serializer_class = IlanBasvuruSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        # Kullanıcı sadece kendi başvurularını görebilir
        if self.request.user.is_authenticated:
            return self.queryset.filter(basvuran_email=self.request.user.email)
        return self.queryset.none()
