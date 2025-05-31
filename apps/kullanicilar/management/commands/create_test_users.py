"""
🐾 Test Kullanıcıları Oluşturma Komutu
==============================================================================
FAZ 1-2 sonrası kullanıcı içeriği doldurma
Kullanım: python manage.py create_test_users
==============================================================================
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.kullanicilar.models import CustomUser


class Command(BaseCommand):
    help = 'Test kullanıcıları ve profilleri oluşturur - FAZ 1-2 içerik doldurma'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            help='Mevcut test kullanıcılarını sil ve yenilerini oluştur',
        )

    def handle(self, *args, **options):
        if options['delete_existing']:
            self.stdout.write('🗑️ Mevcut test kullanıcıları siliniyor...')
            CustomUser.objects.filter(email__contains='test').delete()

        with transaction.atomic():
            self.create_admin_user()
            self.create_sahiplendiren_users()
            self.create_sahiplenmek_isteyen_users()

        self.stdout.write(
            self.style.SUCCESS('✅ Tüm test kullanıcıları başarıyla oluşturuldu!')
        )

    def create_admin_user(self):
        """Admin kullanıcı oluştur"""
        try:
            admin_email = 'admin@test.com'
            user = CustomUser.objects.get(email=admin_email)
            self.stdout.write(
                self.style.WARNING(f'👑 Admin kullanıcı zaten mevcut: {admin_email}')
            )
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(
                email=admin_email,
                password='AdminTest123!',
                first_name='Admin',
                last_name='User',
                rol='admin',
                is_staff=True,
                is_superuser=True,
                email_dogrulanmis=True,
                durum='aktif'
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'👑 Admin kullanıcı oluşturuldu: {admin_email}')
            )
            
        return user

    def create_sahiplendiren_users(self):
        """Sahiplendiren kullanıcıları oluştur"""
        self.stdout.write('🏠 Sahiplendiren kullanıcılar oluşturuluyor...')
        
        sahiplendiren_data = [
            {
                'email': 'esin.yilmaz@test.com',
                'first_name': 'Esin',
                'last_name': 'Yılmaz',
                'telefon': '05551234568',
                'sehir': 'İstanbul',
                'biyografi': '15 yıldır İstanbul\'da köpek bakımevi işletiyorum. Her canlının bir yuva bulması için elimden geleni yapıyorum. Platformda, sevgi dolu evlere kapı aralamak istiyorum. Özellikle yaşlı ve özel bakım gerektiren hayvanlarla ilgileniyorum.',
                'ev_tipi': 'müstakil_ev',
                'deneyim_yil': 15,
                'bahce': True,
                'diger_hayvanlar': '12 köpek (bakımevi)',
                'referans1': 'Ahmet Demir - 05551111111',
                'referans2': 'Fatma Kaya - 05552222222'
            },
            {
                'email': 'can.ozturk@test.com',
                'first_name': 'Can',
                'last_name': 'Öztürk',
                'telefon': '05551234569',
                'sehir': 'Ankara',
                'biyografi': 'Ankara\'da yaşıyorum, geniş bahçeli evimde rescue kedilere bakıyorum. 8 yıldır sokak hayvanları ile ilgileniyorum. Kedilerin davranışları konusunda deneyimliyim ve özellikle çekingen kedilerin rehabilitasyonu ile ilgileniyorum.',
                'ev_tipi': 'müstakil_ev',
                'deneyim_yil': 8,
                'bahce': True,
                'diger_hayvanlar': '6 kedi',
                'referans1': 'Veteriner Dr. Ayşe Tan - 05553333333',
                'referans2': 'Sokak Hayvanları Derneği - 05554444444'
            },
            {
                'email': 'meral.kaplan@test.com',
                'first_name': 'Meral',
                'last_name': 'Kaplan',
                'telefon': '05551234570',
                'sehir': 'İzmir',
                'biyografi': 'İzmir\'de yaşıyorum. Kuş sevgisi ile büyüdüm, evimde çeşitli kuş türleri var. Özellikle el besleme kuş yavrularının bakımında deneyimliyim. Kuşların sağlığı ve beslenme konularında birikimim var.',
                'ev_tipi': 'daire',
                'deneyim_yil': 5,
                'bahce': False,
                'diger_hayvanlar': '4 muhabbet kuşu, 2 kanarya',
                'referans1': 'Kuş Üreticileri Derneği - 05555555555',
                'referans2': 'Komşu Ahmet Bey - 05556666666'
            }
        ]

        for data in sahiplendiren_data:
            user = self.create_sahiplendiren_user(data)
            self.stdout.write(f'   ✅ Sahiplendiren: {user.email}')

    def create_sahiplenmek_isteyen_users(self):
        """Sahiplenmek isteyen kullanıcıları oluştur"""
        self.stdout.write('💝 Sahiplenmek isteyen kullanıcılar oluşturuluyor...')
        
        sahiplenmek_data = [
            {
                'email': 'mehmet.kaya@test.com',
                'first_name': 'Mehmet',
                'last_name': 'Kaya',
                'telefon': '05551234571',
                'sehir': 'Ankara',
                'biyografi': 'Ankara\'da yaşıyorum, evim büyük ama sessiz. Yıllardır bir dostum olsun istiyorum. Özellikle yaşlı kedilere özel ilgim var - onlar da sevgiyi hak ediyor. Emekli öğretmenim, evde çok zamanım var.',
                'ev_tipi': 'daire',
                'deneyim_yil': 0,
                'bahce': False,
                'diger_hayvanlar': 'Yok',
                'referans1': 'Komşu Ayşe Hanım - 05557777777',
                'referans2': 'Kardeşim Ali Kaya - 05558888888'
            },
            {
                'email': 'zeynep.arslan@test.com',
                'first_name': 'Zeynep',
                'last_name': 'Arslan',
                'telefon': '05551234572',
                'sehir': 'İstanbul',
                'biyografi': 'İstanbul\'da yaşan genç bir mimar. Apartman dairesinde küçük bir köpek sahiplenmek istiyorum. Çalışma saatlerim düzenli, evde köpeğimle vakit geçirebilirim. İlk kez pet sahipleniyorum ama çok heyecanlıyım.',
                'ev_tipi': 'daire',
                'deneyim_yil': 0,
                'bahce': False,
                'diger_hayvanlar': 'Yok',
                'referans1': 'İş arkadaşım Burak - 05559999999',
                'referans2': 'Veteriner Dr. Cem Özkan - 05551010101'
            },
            {
                'email': 'ahmet.yildiz@test.com',
                'first_name': 'Ahmet',
                'last_name': 'Yıldız',
                'telefon': '05551234573',
                'sehir': 'Bursa',
                'biyografi': 'Bursa\'da bahçeli evde yaşıyorum. Çocuklarım büyüdü, ev biraz boş kaldı. Orta büyüklükte, aile dostu bir köpek sahiplenmek istiyorum. Köpek bakımında tecrübem var, çocukluğumda köpeğimiz vardı.',
                'ev_tipi': 'müstakil_ev',
                'deneyim_yil': 2,
                'bahce': True,
                'diger_hayvanlar': 'Yok (geçmişte köpek)',
                'referans1': 'Eşim Fatma Yıldız - 05551111100',
                'referans2': 'Veteriner Dr. Murat Can - 05552222200'
            }
        ]

        for data in sahiplenmek_data:
            user = self.create_sahiplenmek_isteyen_user(data)
            self.stdout.write(f'   ✅ Sahiplenmek isteyen: {user.email}')

    def create_sahiplendiren_user(self, data):
        """Sahiplendiren kullanıcı oluştur"""
        user_data = {
            'email': data['email'],
            'password': 'TestUser123!',
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'telefon': data['telefon'],
            'sehir': data['sehir'],
            'biyografi': data['biyografi'],
            'rol': 'user',
            'durum': 'active',
            'email_dogrulanmis': True,
            'sahiplendiren_mi': True,
            'sahiplenmek_istiyor_mu': False
        }

        user = CustomUser.objects.create_user(**user_data)
        

        return user

    def create_sahiplenmek_isteyen_user(self, data):
        """Sahiplenmek isteyen kullanıcı oluştur"""
        user_data = {
            'email': data['email'],
            'password': 'TestUser123!',
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'telefon': data['telefon'],
            'sehir': data['sehir'],
            'biyografi': data['biyografi'],
            'rol': 'user',
            'durum': 'active',
            'email_dogrulanmis': True,
            'sahiplendiren_mi': False,
            'sahiplenmek_istiyor_mu': True
        }

        user = CustomUser.objects.create_user(**user_data)
        

        return user

    def create_test_users(self):
        """Test kullanıcıları oluştur"""
        test_users = [
            {
                'email': 'esin.yilmaz@test.com',
                'first_name': 'Esin',
                'last_name': 'Yılmaz',
                'sahiplendiren_mi': True,
            },
            {
                'email': 'can.ozturk@test.com',
                'first_name': 'Can',
                'last_name': 'Öztürk',
                'sahiplendiren_mi': True,
            },
            {
                'email': 'meral.kaplan@test.com',
                'first_name': 'Meral',
                'last_name': 'Kaplan',
                'sahiplendiren_mi': True,
            },
            {
                'email': 'mehmet.kaya@test.com',
                'first_name': 'Mehmet',
                'last_name': 'Kaya',
                'sahiplenmek_istiyor_mu': True,
            },
            {
                'email': 'zeynep.arslan@test.com',
                'first_name': 'Zeynep',
                'last_name': 'Arslan',
                'sahiplenmek_istiyor_mu': True,
            },
            {
                'email': 'ahmet.yildiz@test.com',
                'first_name': 'Ahmet',
                'last_name': 'Yıldız',
                'sahiplenmek_istiyor_mu': True,
            }
        ]
        
        for user_data in test_users:
            try:
                user = CustomUser.objects.get(email=user_data['email'])
                self.stdout.write(
                    self.style.WARNING(f'👤 Kullanıcı zaten mevcut: {user_data["email"]}')
                )
            except CustomUser.DoesNotExist:
                email = user_data.pop('email')
                
                user = CustomUser.objects.create_user(
                    email=email,
                    password='TestUser123!',
                    email_dogrulanmis=True,
                    durum='aktif',
                    **user_data
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'👤 Test kullanıcı oluşturuldu: {email}')
                )
