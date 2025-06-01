"""
🐾 Evcil Hayvan Platformu - Ortak Sabitler
==============================================================================
Platform genelinde kullanılacak sabit değerler
==============================================================================
"""

from django.utils.translation import gettext_lazy as _
from django.db import models # Bu satırı ekleyin

# ==============================================================================
# 🐾 EVCİL HAYVAN TÜRLERİ - Platformun can dostları
# ==============================================================================

# Hayvan türleri
class PetTypes(models.TextChoices):
    """
    🐾 Evcil Hayvan Türleri
    Platformda desteklenen temel hayvan türleri
    """
    KEDI = 'kedi', _('Kedi')
    KOPEK = 'kopek', _('Köpek')
    KUS = 'kus', _('Kuş')
    BALIK = 'balik', _('Balık')
    KEMIRGEN = 'kemirgen', _('Kemirgen')
    SURUNGEN = 'surungen', _('Sürüngen')
    DIGER = 'diger', _('Diğer') # Bu satırı ekleyin veya güncelleyin

# Hayvan boyutları
class PetSizes:
    EXTRA_SMALL = 'xs'  # 0-5 kg
    SMALL = 'sm'        # 5-10 kg
    MEDIUM = 'md'       # 10-25 kg
    LARGE = 'lg'        # 25-45 kg
    EXTRA_LARGE = 'xl'  # 45+ kg
    
    CHOICES = [
        (EXTRA_SMALL, _('Çok Küçük (0-5 kg)')),
        (SMALL, _('Küçük (5-10 kg)')),
        (MEDIUM, _('Orta (10-25 kg)')),
        (LARGE, _('Büyük (25-45 kg)')),
        (EXTRA_LARGE, _('Çok Büyük (45+ kg)')),
    ]

# Hayvan yaşları
class PetAges:
    BABY = 'baby'        # 0-6 ay
    YOUNG = 'young'      # 6 ay - 2 yaş
    ADULT = 'adult'      # 2-7 yaş
    SENIOR = 'senior'    # 7+ yaş
    
    CHOICES = [
        (BABY, _('Yavru (0-6 ay)')),
        (YOUNG, _('Genç (6 ay - 2 yaş)')),
        (ADULT, _('Yetişkin (2-7 yaş)')),
        (SENIOR, _('Yaşlı (7+ yaş)')),
    ]

# Hayvan cinsiyetleri
class PetGenders:
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'
    
    CHOICES = [
        (MALE, _('Erkek')),
        (FEMALE, _('Dişi')),
        (UNKNOWN, _('Bilinmiyor')),
    ]

# ==============================================================================
# 📋 ADOPTION RELATED CONSTANTS - Sahiplenme ile ilgili sabitler
# ==============================================================================

# İlan durumları
class ListingStatus:
    DRAFT = 'draft'
    ACTIVE = 'active'
    ADOPTED = 'adopted'
    INACTIVE = 'inactive'
    EXPIRED = 'expired'
    
    CHOICES = [
        (DRAFT, _('Taslak')),
        (ACTIVE, _('Aktif')),
        (ADOPTED, _('Sahiplenildi')),
        (INACTIVE, _('Pasif')),
        (EXPIRED, _('Süresi Dolmuş')),
    ]

# Başvuru durumları
class ApplicationStatus:
    PENDING = 'pending'
    UNDER_REVIEW = 'under_review'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    WITHDRAWN = 'withdrawn'
    
    CHOICES = [
        (PENDING, _('Beklemede')),
        (UNDER_REVIEW, _('İnceleniyor')),
        (APPROVED, _('Onaylandı')),
        (REJECTED, _('Reddedildi')),
        (WITHDRAWN, _('Geri Çekildi')),
    ]

# Sahiplenme türleri
class AdoptionTypes:
    ADOPTION = 'adoption'
    FOSTERING = 'fostering'
    TEMPORARY_CARE = 'temporary_care'
    
    CHOICES = [
        (ADOPTION, _('Kalıcı Sahiplenme')),
        (FOSTERING, _('Geçici Bakım')),
        (TEMPORARY_CARE, _('Acil Bakım')),
    ]

# ==============================================================================
# 👤 USER RELATED CONSTANTS - Kullanıcı ile ilgili sabitler
# ==============================================================================

# Kullanıcı rolleri
class UserRoles:
    USER = 'user'
    SHELTER_STAFF = 'shelter_staff'
    VETERINARY = 'veterinary'
    VOLUNTEER = 'volunteer'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    
    CHOICES = [
        (USER, _('Kullanıcı')),
        (SHELTER_STAFF, _('Barınak Çalışanı')),
        (VETERINARY, _('Veteriner')),
        (VOLUNTEER, _('Gönüllü')),
        (MODERATOR, _('Moderatör')),
        (ADMIN, _('Yönetici')),
    ]

# Kullanıcı durumları
class UserStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'
    BANNED = 'banned'
    
    CHOICES = [
        (ACTIVE, _('Aktif')),
        (INACTIVE, _('Pasif')),
        (SUSPENDED, _('Askıya Alınmış')),
        (BANNED, _('Yasaklanmış')),
    ]

# ==============================================================================
# 📱 SYSTEM CONSTANTS - Sistem sabitleri
# ==============================================================================

# Bildirim türleri
class NotificationTypes:
    APPLICATION_RECEIVED = 'application_received'
    APPLICATION_APPROVED = 'application_approved'
    APPLICATION_REJECTED = 'application_rejected'
    NEW_MESSAGE = 'new_message'
    LISTING_EXPIRED = 'listing_expired'
    SYSTEM_ANNOUNCEMENT = 'system_announcement'
    
    CHOICES = [
        (APPLICATION_RECEIVED, _('Başvuru Alındı')),
        (APPLICATION_APPROVED, _('Başvuru Onaylandı')),
        (APPLICATION_REJECTED, _('Başvuru Reddedildi')),
        (NEW_MESSAGE, _('Yeni Mesaj')),
        (LISTING_EXPIRED, _('İlan Süresi Doldu')),
        (SYSTEM_ANNOUNCEMENT, _('Sistem Duyurusu')),
    ]

# Öncelik seviyeleri
class PriorityLevels:
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    URGENT = 'urgent'
    
    CHOICES = [
        (LOW, _('Düşük')),
        (NORMAL, _('Normal')),
        (HIGH, _('Yüksek')),
        (URGENT, _('Acil')),
    ]

# ==============================================================================
# 🔧 CONFIGURATION CONSTANTS - Konfigürasyon sabitleri
# ==============================================================================

# Dosya boyutu limitleri (bytes)
class FileSizeLimits:
    PROFILE_IMAGE = 2 * 1024 * 1024    # 2MB
    PET_IMAGE = 5 * 1024 * 1024        # 5MB
    DOCUMENT = 10 * 1024 * 1024        # 10MB

# Sayfa boyutları
class PageSizes:
    DEFAULT = 20
    SMALL = 10
    LARGE = 50
    MAX = 100

# Rate limiting
class RateLimits:
    LOGIN_ATTEMPTS = 5
    MESSAGE_PER_HOUR = 100
    APPLICATION_PER_DAY = 3
    LISTING_PER_DAY = 5

# ==============================================================================
# 🌍 REGIONAL CONSTANTS - Bölgesel sabitler
# ==============================================================================

# Türkiye şehirleri (öncelik verilenler)
TURKISH_CITIES = [
    ('istanbul', _('İstanbul')),
    ('ankara', _('Ankara')),
    ('izmir', _('İzmir')),
    ('bursa', _('Bursa')),
    ('antalya', _('Antalya')),
    ('konya', _('Konya')),
    ('adana', _('Adana')),
    ('gaziantep', _('Gaziantep')),
    ('other', _('Diğer')),
]

# Dil kodları
LANGUAGE_CODES = [
    ('tr', _('Türkçe')),
    ('en', _('English')),
]

# ==============================================================================
# 🐕 HAYVAN IRKLARI - Tür bazlı ırk listeleri
# ==============================================================================

class KopekIrklari:
    """
    Köpek ırkları enum sınıfı
    Köpek ırklarının id ve adları için standart kodlama
    """
    
    # Köpek ırkları seçenekleri (id, ırk adı)
    choices = [
        ('70', 'Affenpinscher'),
        ('85', 'Afgan Tazısı'),
        ('68', 'Aidi'),
        ('86', 'Ainu'),
        ('69', 'Airedale Terrier'),
        ('88', 'Akbaş'),
        ('71', 'Akita İnu'),
        ('332', 'Aksaray Malaklısı'),
        ('89', 'Alabay (Alabai)'),
        ('72', 'Alaskan Malamute'),
        ('90', 'Alman Av Terrieri'),
        ('73', 'Alman Çoban Köpeği'),
        ('91', 'Alman Kalın Tüylü Pointer'),
        ('74', 'Alman Kısa Tüylü Pointer'),
        ('92', 'Alman Spanieli'),
        ('75', 'Alpine Dachsbracke'),
        ('93', 'Amerikan Bulldog'),
        ('76', 'Amerikan Cocker Spaniel'),
        ('94', 'Amerikan Eskimo'),
        ('77', 'Amerikan Pitbull Terrier'),
        ('95', 'Amerikan Staffordshire Terrier'),
        ('78', 'Amerikan Su Spanieli'),
        ('96', 'Amerikan Tilki Tazısı'),
        ('79', 'Amerikan Tüysüz Terrieri'),
        ('97', 'Amerikan Yerli Köpeği'),
        ('80', 'Appenzell Dağ Köpeği'),
        ('99', 'Ariegeois'),
        ('81', 'Avustralya Çoban Köpeği'),
        ('100', 'Avustralya Sığır Köpeği'),
        ('83', 'Avustralya Terrier'),
        ('101', 'Avustralyalı Kelpie'),
        ('84', 'Avusturya Tazısı'),
        ('102', 'Avusturyalı Pinscher'),
        ('103', 'Bandogge Mastiff'),
        ('119', 'Basenji'),
        ('104', 'Basset Hound'),
        ('120', 'Bavyera Dağ Tazısı'),
        ('105', 'Beagle'),
        ('121', 'Beauceron'),
        ('107', 'Bedlington Terrier'),
        ('122', 'Belçika Groenendael'),
        ('108', 'Belçika Laekenois'),
        ('123', 'Belçika Malinois'),
        ('306', 'Belçika Tervuren'),
        ('124', 'Bergamasco'),
        ('109', 'Bernese Dağ Köpeği'),
        ('125', 'Bichon Frise'),
        ('110', 'Bichon Havanese'),
        ('126', 'Billy'),
        ('111', 'Bloodhound'),
        ('127', 'Border Collie'),
        ('112', 'Border Terrier'),
        ('128', 'Borzoi'),
        ('113', 'Boston Terrier'),
        ('129', 'Bouvier des Ardennes'),
        ('114', 'Bouvier des Flandres'),
        ('130', 'Boxer'),
        ('115', 'Brezilya Mastiff'),
        ('131', 'Briard'),
        ('116', 'Brittany'),
        ('307', 'Brüksel Griffonu'),
        ('117', 'Bull Terrier'),
        ('132', 'Bullmastiff'),
        ('118', 'Büyük İsveç Dağ Köpeği'),
        ('133', 'Cairn Terrier'),
        ('143', 'Canaan Köpeği'),
        ('134', 'Cane Corso Italiano'),
        ('144', 'Cao da Serra da Estrela'),
        ('135', 'Cao de Castro Laboreiro'),
        ('145', 'Cao de Serra de Aires'),
        ('136', 'Cardigan Welsh Corgi'),
        ('146', 'Catahoula Leopar Köpeği'),
        ('151', 'Çatalburun'),
        ('137', 'Cavalier King Charles Spanieli'),
        ('147', 'Cesky Terrier'),
        ('138', 'Chesapeake Bay Retriever'),
        ('148', 'Chiens Francaises'),
        ('139', 'Chihuahua'),
        ('149', 'Chow Chow (çin Aslanı)'),
        ('142', 'Çin Creste Köpeği'),
        ('152', 'Çin Shar Pei'),
        ('140', 'Clumber Spaniel'),
        ('150', 'Collie'),
        ('333', 'Coton De Tulear'),
        ('141', 'Curly Coated Retriever'),
        ('153', 'Dachshund (Sosis)'),
        ('157', 'Dalmatian'),
        ('154', 'Dandie Dinmont Terrier'),
        ('158', 'Dev Schnauzer'),
        ('156', 'Doberman Pinscher'),
        ('159', 'Dogo Arjantin'),
        ('160', 'Entlebucher'),
        ('161', 'Eskimo Köpeği'),
        ('162', 'Field Spaniel'),
        ('166', 'Fin Tazısı'),
        ('163', 'Finnish Spitz'),
        ('167', 'Flat Coated Retriever'),
        ('164', 'Fox Terrier (Smooth)'),
        ('168', 'Fox Terrier (Wire)'),
        ('165', 'Fransız Bulldog'),
        ('169', 'Fransız Mastiff'),
        ('170', 'Glen of Imaal Terrier'),
        ('175', 'Golden Retriever'),
        ('171', 'Gordon Setter'),
        ('176', 'Grand Bleu de Gascogne'),
        ('172', 'Grand Gascon Saintongeois'),
        ('177', 'Great Dane (Danua)'),
        ('173', 'Great Phyrenees'),
        ('178', 'Greyhound'),
        ('174', 'Grönland Köpeği'),
        ('179', 'Hanover Tazısı'),
        ('182', 'Harrier'),
        ('180', 'Hırvat Çoban Köpeği'),
        ('183', 'Hollanda Çoban Köpeği'),
        ('181', 'Hovawart'),
        ('184', 'Ibizan Hound'),
        ('192', 'İlirya çoban Köpeği'),
        ('185', 'İngiliz Bulldog'),
        ('193', 'İngiliz Cocker Spaniel'),
        ('186', 'İngiliz Setter'),
        ('194', 'İngiliz Springer Spaniel'),
        ('329', 'İngiliz Tilki Tazısı'),
        ('195', 'İrlandalı Kurt Tazısı'),
        ('187', 'İrlandalı Setter'),
        ('196', 'İrlandalı Su Spanieli'),
        ('188', 'İrlandalı Terrier'),
        ('197', 'İskoç Geyik Tazısı'),
        ('189', 'İskoç Terrier'),
        ('198', 'İspanyol Mastiff'),
        ('190', 'İsveç çoban köpeği'),
        ('199', 'İsveç Geyik Avcısı'),
        ('191', 'İtalyan Tazısı'),
        ('200', 'İzlanda Köpeği'),
        ('201', 'Jack Russell Terrier'),
        ('202', 'Japon Chin'),
        ('203', 'Kangal'),
        ('208', 'Karelya Ayı Köpeği'),
        ('209', 'Kars Çoban Köpeği'),
        ('204', 'Karst Çoban Köpeği'),
        ('210', 'Katalan Çoban Köpeği'),
        ('205', 'Keeshond'),
        ('211', 'Kerry Blue Terrier'),
        ('206', 'King Charles Spaniel'),
        ('212', 'Komondor'),
        ('207', 'Kuvasz'),
        ('213', 'Kyüshü'),
        ('214', 'Labrador Retriever'),
        ('218', 'Lakeland Terrier'),
        ('215', 'Landseer'),
        ('219', 'Lapphund'),
        ('216', 'Lapponian Çoban Köpeği'),
        ('220', 'Leonberger'),
        ('217', 'Lhasa Apso'),
        ('221', 'Lowchen'),
        ('222', 'Maltese'),
        ('226', 'Manchester Terrier'),
        ('223', 'Maremma Çoban Köpeği'),
        ('227', 'Mastiff'),
        ('224', 'Minyatür Bull Terrier'),
        ('228', 'Minyatür Pinscher'),
        ('225', 'Minyatür Schnauzer'),
        ('229', 'Mudi'),
        ('230', 'Napoliten Mastiff'),
        ('234', 'Newfoundland'),
        ('231', 'Norfolk Terrier'),
        ('235', 'Norrbottenspets'),
        ('232', 'Norsk Buhund'),
        ('236', 'Norveç Geyik Avcısı'),
        ('233', 'Norwich Terrier'),
        ('237', 'Old English Sheepdog'),
        ('239', 'Otterhound'),
        ('240', 'Pappilon'),
        ('251', 'Pekingese'),
        ('241', 'Pembroke Welsh Corgi'),
        ('252', 'Peru Tüysüz Köpeği'),
        ('242', 'Petit Basset Griffon Vendien'),
        ('253', 'Petit Bleu de Gascogne'),
        ('243', 'Pharaoh Hound'),
        ('254', 'Picardy Çoban Köpeği'),
        ('244', 'Plott Tazısı'),
        ('255', 'Pointer'),
        ('245', 'Poitevin'),
        ('256', 'Polonya Tazısı'),
        ('246', 'Pomeranyalı'),
        ('257', 'Poodle (Minyatür Kaniş)'),
        ('247', 'Poodle(Standart Kaniş)'),
        ('258', 'Portekiz Su Köpeği'),
        ('308', 'Presa Canario'),
        ('248', 'Pug'),
        ('259', 'Puli'),
        ('249', 'Pumi'),
        ('260', 'Pyrenees Çoban Köpeği'),
        ('250', 'Pyrenees Mastiff'),
        ('261', 'Rafeiro do Alentejo'),
        ('263', 'Rhodesian Ridgeback'),
        ('262', 'Rottweiler'),
        ('264', 'Russian Spaniel'),
        ('265', 'Sakallı Collie'),
        ('276', 'Saluki'),
        ('266', 'Samoyed'),
        ('277', 'Sanshu'),
        ('267', 'Schipperkee'),
        ('278', 'Sealyham Terrier'),
        ('268', 'Shetland Çoban Köpeği'),
        ('279', 'Shiba Inu'),
        ('269', 'Shih Tzu'),
        ('280', 'Sibirya Kurdu (Husky)'),
        ('270', 'Silky Terrier'),
        ('281', 'Siyah ve Açık Kahverengi Rakun Tazısı'),
        ('271', 'Skye Terrier'),
        ('282', 'Slovak Tchouvatch'),
        ('272', 'Soft Coated Wheaten Terrier'),
        ('283', 'Sokö (Sokak Köpeği)'),
        ('273', 'St. Bernard (Saint Bernard)'),
        ('284', 'Staffordshire Bull Terrier'),
        ('274', 'Standart Schnauzer'),
        ('285', 'Steinbracke'),
        ('275', 'Styrian Dağ Tazısı'),
        ('286', 'Sussex Spanieli'),
        ('287', 'Tatra Çoban Köpeği'),
        ('291', 'Tibet Terrieri'),
        ('288', 'Tibetli Mastiff'),
        ('292', 'Tibetli Spaniel'),
        ('289', 'Tosa'),
        ('293', 'Trigg Tazısı'),
        ('290', 'Türk Tazısı'),
        ('294', 'Tüysüz Collie'),
        ('295', 'Tyrolean Tazısı'),
        ('296', 'Valee Çoban Köpeği'),
        ('297', 'Vizsla'),
        ('298', 'Weimaraner'),
        ('302', 'Welsh Springer Spaniel'),
        ('299', 'Welsh Terrier'),
        ('303', 'West Highland White Terrier'),
        ('300', 'Westphalia Basseti'),
        ('304', 'Whippet'),
        ('301', 'Wirehaired Pointing Griffon'),
        ('305', 'Yorkshire Terrier'),
    ]
    
    # Popüler köpek ırkları (Türkiye için)
    POPULER_IRKLAR = [
        '175',  # Golden Retriever
        '214',  # Labrador Retriever
        '73',   # Alman Çoban Köpeği
        '203',  # Kangal
        '88',   # Akbaş
        '165',  # Fransız Bulldog
        '139',  # Chihuahua
        '280',  # Sibirya Kurdu (Husky)
        '262',  # Rottweiler
        '130',  # Boxer
    ]
    
    # Yerli köpek ırkları
    YERLI_IRKLAR = [
        '203',  # Kangal
        '88',   # Akbaş
        '209',  # Kars Çoban Köpeği
        '151',  # Çatalburun
        '290',  # Türk Tazısı
        '332',  # Aksaray Malaklısı
        '283',  # Sokö (Sokak Köpeği)
    ]
    
    @classmethod
    def get_irk_adi(cls, irk_id):
        """Irk ID'sine göre ırk adını döndürür"""
        for id, ad in cls.choices:
            if id == irk_id:
                return ad
        return None
    
    @classmethod
    def populer_irklar(cls):
        """Popüler köpek ırklarını döndürür"""
        return [(id, cls.get_irk_adi(id)) for id in cls.POPULER_IRKLAR]
    
    @classmethod
    def yerli_irklar(cls):
        """Yerli köpek ırklarını döndürür"""
        return [(id, cls.get_irk_adi(id)) for id in cls.YERLI_IRKLAR]

# Daha sonra kedi, kuş gibi diğer hayvan türlerinin ırk listeleri eklenebilir
# class KediIrklari:
#    ...

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu sabitler, platform genelinde tutarlılık sağlar ve
# magic number kullanımını önler.
# 🐾 Her sabit, daha temiz kod için!

class Iller:
    """
    Türkiye illeri enum sınıfı
    İl kodları ve adları için standart kodlama
    """
    
    # İl seçenekleri (il plaka kodu, il adı)
    choices = [
        ('1', 'Adana'),
        ('2', 'Adıyaman'),
        ('3', 'Afyonkarahisar'),
        ('4', 'Ağrı'),
        ('68', 'Aksaray'),
        ('5', 'Amasya'),
        ('6', 'Ankara'),
        ('7', 'Antalya'),
        ('75', 'Ardahan'),
        ('8', 'Artvin'),
        ('9', 'Aydın'),
        ('10', 'Balıkesir'),
        ('74', 'Bartın'),
        ('72', 'Batman'),
        ('69', 'Bayburt'),
        ('11', 'Bilecik'),
        ('12', 'Bingöl'),
        ('13', 'Bitlis'),
        ('14', 'Bolu'),
        ('15', 'Burdur'),
        ('16', 'Bursa'),
        ('17', 'Çanakkale'),
        ('18', 'Çankırı'),
        ('19', 'Çorum'),
        ('20', 'Denizli'),
        ('21', 'Diyarbakır'),
        ('81', 'Düzce'),
        ('22', 'Edirne'),
        ('23', 'Elazığ'),
        ('24', 'Erzincan'),
        ('25', 'Erzurum'),
        ('26', 'Eskişehir'),
        ('27', 'Gaziantep'),
        ('28', 'Giresun'),
        ('29', 'Gümüşhane'),
        ('30', 'Hakkari'),
        ('31', 'Hatay'),
        ('76', 'Iğdır'),
        ('32', 'Isparta'),
        ('34', 'İstanbul'),
        ('35', 'İzmir'),
        ('46', 'Kahramanmaraş'),
        ('78', 'Karabük'),
        ('70', 'Karaman'),
        ('36', 'Kars'),
        ('37', 'Kastamonu'),
        ('38', 'Kayseri'),
        ('79', 'Kilis'),
        ('71', 'Kırıkkale'),
        ('39', 'Kırklareli'),
        ('40', 'Kırşehir'),
        ('41', 'Kocaeli'),
        ('42', 'Konya'),
        ('43', 'Kütahya'),
        ('44', 'Malatya'),
        ('45', 'Manisa'),
        ('47', 'Mardin'),
        ('33', 'Mersin'),
        ('48', 'Muğla'),
        ('49', 'Muş'),
        ('50', 'Nevşehir'),
        ('51', 'Niğde'),
        ('52', 'Ordu'),
        ('80', 'Osmaniye'),
        ('53', 'Rize'),
        ('54', 'Sakarya'),
        ('55', 'Samsun'),
        ('63', 'Şanlıurfa'),
        ('56', 'Siirt'),
        ('57', 'Sinop'),
        ('58', 'Sivas'),
        ('73', 'Şırnak'),
        ('59', 'Tekirdağ'),
        ('60', 'Tokat'),
        ('61', 'Trabzon'),
        ('62', 'Tunceli'),
        ('64', 'Uşak'),
        ('65', 'Van'),
        ('77', 'Yalova'),
        ('66', 'Yozgat'),
        ('67', 'Zonguldak'),
    ]
    
    # Kolay erişim için il kodları değişkenler olarak tanımlanabilir
    ADANA = '1'
    ADIYAMAN = '2'
    # ...ve diğer iller
    ISTANBUL = '34'
    IZMIR = '35'
    # ...ve diğer iller
    
    @classmethod
    def get_il_adi(cls, il_kodu):
        """İl koduna göre il adını döndürür"""
        for kod, ad in cls.choices:
            if kod == il_kodu:
                return ad
        return None

# Örnek bir views.py dosyasında kullanımı:
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.ortak.constants import Iller

@api_view(['GET'])
def iller_listesi(request):
    """Türkiye'deki illerin listesini döndürür"""
    return Response({
        'success': True,
        'data': Iller.choices,
        'message': 'İller listelendi'
    })

@api_view(['GET'])
def il_detay(request, il_kodu):
    """Belirli bir ilin detaylarını döndürür"""
    il_adi = Iller.get_il_adi(il_kodu)
    if not il_adi:
        return Response({
            'success': False,
            'message': 'İl bulunamadı'
        }, status=404)
    
    return Response({
        'success': True,
        'data': {
            'kod': il_kodu,
            'ad': il_adi
        },
        'message': f'{il_adi} ili bilgileri'
    })

# Örnek bir forms.py dosyasında:
from django import forms
from apps.ortak.constants import Iller

class HayvanKonumForm(forms.Form):
    il = forms.ChoiceField(
        choices=Iller.choices,
        label='İl',
        required=True
    )
    ilce = forms.CharField(
        max_length=100,
        label='İlçe',
        required=True
    )

