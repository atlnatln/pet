"""
🐾 Kullanıcılar API Views
==============================================================================
Kullanıcı endpoint'leri - Her kullanıcının dijital hikayesi API'de yaşar
==============================================================================
"""

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, logout
from django.db.models import Q, Count
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.ortak.pagination import StandardPagination
from .models import CustomUser, KullaniciProfil
from .permissions import IsProfileOwner, IsVerifiedUser, IsModeratorOrAdmin
from .serializers import (
    UserBasicSerializer, UserDetailSerializer, UserRegistrationSerializer,
    UserLoginSerializer, UserProfileUpdateSerializer, PasswordChangeSerializer,
    PasswordResetRequestSerializer, EmailVerificationSerializer, 
    UserStatsSerializer, KullaniciProfilSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    Kullanıcı ViewSet - Dijital kimliklerin yönetimi
    
    Her kullanıcı, platformun kendine özel bir hikayesidir.
    Bu ViewSet ile kullanıcıları yönet, profilleri keşfet ve güvenli işlemler yap.
    """
    
    queryset = CustomUser.objects.aktif_kullanicilar().select_related('profil_detay')
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'sehir']
    ordering_fields = ['first_name', 'last_name', 'uyelik_tarihi']
    ordering = ['-uyelik_tarihi']
    
    def get_serializer_class(self):
        """Her action için uygun serializer seç"""
        if self.action == 'list':
            return UserBasicSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return UserProfileUpdateSerializer
        else:
            return UserDetailSerializer
    
    def get_permissions(self):
        """Action bazlı permission"""
        if self.action in ['register', 'login', 'verify_email', 'request_password_reset']:
            permission_classes = [AllowAny]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsVerifiedUser]
        elif self.action == 'me':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'change_password']:
            permission_classes = [IsProfileOwner]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Kullanıcı rol bazlı queryset"""
        if self.request.user.is_authenticated:
            if self.request.user.rol in ['admin', 'moderator']:
                return CustomUser.objects.all().select_related('profil_detay')
            else:
                return CustomUser.objects.aktif_kullanicilar().select_related('profil_detay')
        return CustomUser.objects.none()
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Kullanıcı kayıt
        
        Yeni kullanıcı hesabı oluştur ve hoş geldin sürecini başlat.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        # Token oluştur
        token, created = Token.objects.get_or_create(user=user)
        
        # E-posta doğrulama servisi burada çağrılacak
        # await EmailService.send_verification_email(user)
        
        return Response({
            'success': True,
            'message': _('Hesabınız başarıyla oluşturuldu! E-posta adresinizi doğrulamayı unutmayın.'),
            'data': {
                'user': UserDetailSerializer(user).data,
                'token': token.key
            }
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Kullanıcı giriş
        
        E-posta ve şifre ile güvenli giriş yapın.
        """
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Django session login
        login(request, user)
        
        # Son giriş bilgilerini güncelle
        user.son_giris_guncelle()
        
        # Token al veya oluştur
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'message': _(f'Hoş geldin {user.get_display_name()}! 🐾'),
            'data': {
                'user': UserDetailSerializer(user).data,
                'token': token.key
            }
        })
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Kullanıcı çıkış
        """
        # Token'ı sil
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        # Django session logout
        logout(request)
        
        return Response({
            'success': True,
            'message': _('Başarıyla çıkış yaptınız. Tekrar görüşmek üzere! 👋')
        })
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Mevcut kullanıcı bilgileri
        
        Giriş yapmış kullanıcının kendi profil bilgilerini getir.
        """
        serializer = UserDetailSerializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        Profil güncelleme
        
        Kullanıcı profil bilgilerini güncelle.
        """
        serializer = UserProfileUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'success': True,
            'message': _('Profil bilgileriniz başarıyla güncellendi! ✨'),
            'data': UserDetailSerializer(request.user).data
        })
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Şifre değiştirme
        """
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'success': True,
            'message': _('Şifreniz başarıyla değiştirildi! 🔐')
        })
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def request_password_reset(self, request):
        """
        Şifre sıfırlama talebi
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Şifre sıfırlama servisi burada çağrılacak
        # await EmailService.send_password_reset_email(email)
        
        return Response({
            'success': True,
            'message': _('Şifre sıfırlama bağlantısı e-posta adresinize gönderildi. 📧')
        })
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """
        E-posta doğrulama
        """
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.context['user']
        user.email_dogrula()
        
        return Response({
            'success': True,
            'message': _('E-posta adresiniz başarıyla doğrulandı! Hoş geldiniz! 🎉'),
            'data': UserDetailSerializer(user).data
        })
    
    @action(detail=False, methods=['get'])
    def sahiplendirenler(self, request):
        """
        Sahiplendiren kullanıcılar
        
        Hayvan sahiplendiren aktif kullanıcıları listele.
        """
        sahiplendirenler = CustomUser.objects.sahiplendirenler()
        
        # Sayfalama uygula
        page = self.paginate_queryset(sahiplendirenler)
        if page is not None:
            serializer = UserBasicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = UserBasicSerializer(sahiplendirenler, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Sahiplendiren kullanıcılar listelendi'),
            'count': len(serializer.data)
        })
    
    @action(detail=False, methods=['get'])
    def sahiplenmek_isteyenler(self, request):
        """
        Sahiplenmek isteyen kullanıcılar
        """
        sahiplenmek_isteyenler = CustomUser.objects.sahiplenmek_isteyenler()
        
        page = self.paginate_queryset(sahiplenmek_isteyenler)
        if page is not None:
            serializer = UserBasicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = UserBasicSerializer(sahiplenmek_isteyenler, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Sahiplenmek isteyen kullanıcılar listelendi'),
            'count': len(serializer.data)
        })
    
    @action(detail=False, methods=['get'])
    def istatistikler(self, request):
        """
        Platform kullanıcı istatistikleri
        """
        cache_key = "kullanici_istatistikleri"
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = {
                'toplam_kullanici': CustomUser.objects.count(),
                'aktif_kullanici': CustomUser.objects.aktif_kullanicilar().count(),
                'dogrulanmis_kullanici': CustomUser.objects.filter(email_dogrulanmis=True).count(),
                'sahiplendiren_sayisi': CustomUser.objects.sahiplendirenler().count(),
                'sahiplenmek_isteyen_sayisi': CustomUser.objects.sahiplenmek_isteyenler().count(),
                'sehir_dagilimi': dict(
                    CustomUser.objects.aktif_kullanicilar()
                    .exclude(sehir='')
                    .values('sehir')
                    .annotate(count=Count('id'))
                    .values_list('sehir', 'count')[:10]
                )
            }
            cache.set(cache_key, stats, 3600)  # 1 saat
        
        serializer = UserStatsSerializer(stats)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': _('Platform istatistikleri getirildi')
        })
    
    @action(detail=True, methods=['get'])
    def profil_detay(self, request, pk=None):
        """
        Kullanıcı profil detayları
        """
        user = self.get_object()
        
        try:
            profil_detay = user.profil_detay
            serializer = KullaniciProfilSerializer(profil_detay)
            
            return Response({
                'success': True,
                'data': serializer.data
            })
        except KullaniciProfil.DoesNotExist:
            return Response({
                'success': False,
                'message': _('Profil detayı bulunamadı')
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def arama(self, request):
        """
        Kullanıcı arama
        """
        query = request.data.get('query', '').strip()
        
        if len(query) < 2:
            return Response({
                'success': False,
                'message': _('Arama terimi en az 2 karakter olmalıdır')
            }, status=status.HTTP_400_BAD_REQUEST)
        
        users = CustomUser.objects.arama_yap(query)
        
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserBasicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = UserBasicSerializer(users, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f'{len(serializer.data)} kullanıcı bulundu',
            'query': query
        })
    
    # Moderasyon actions
    @action(detail=True, methods=['post'], permission_classes=[IsModeratorOrAdmin])
    def verify_identity(self, request, pk=None):
        """
        Kimlik doğrulama (Moderatör/Admin)
        """
        user = self.get_object()
        
        try:
            profil_detay = user.profil_detay
            profil_detay.kimlik_dogrulandi_mi = True
            profil_detay.save()
            
            return Response({
                'success': True,
                'message': f'{user.tam_ad} kullanıcısının kimliği doğrulandı ✅'
            })
        except KullaniciProfil.DoesNotExist:
            return Response({
                'success': False,
                'message': _('Profil detayı bulunamadı')
            }, status=status.HTTP_404_NOT_FOUND)

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu ViewSet, kullanıcı sisteminin tüm API ihtiyaçlarını karşılar.
# Güvenli authentication, profil yönetimi ve sosyal özellikler bir arada.
# 🐾 Her endpoint, kullanıcının dijital hikayesine katkı sağlar!
