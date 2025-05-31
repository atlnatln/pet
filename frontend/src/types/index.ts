export interface Kullanici {
  id: number;
  kullanici_adi: string;
  email: string;
  ad: string;
  soyad: string;
  telefon?: string;
  adres?: string;
  profil_resmi?: string;
  hesap_dogrulandi: boolean;
  olusturma_tarihi: string;
}

export interface Hayvan {
  id: number;
  ad: string;
  tur: string;
  cins: string;
  yas: number;
  cinsiyet: 'E' | 'D';
  renk: string;
  agirlik?: number;
  aciklama: string;
  saglik_durumu: string;
  asi_durumu: boolean;
  kisirlaştirma_durumu: boolean;
  resimler: string[];
  konum: string;
  sahiplendirme_durumu: 'MEVCUT' | 'SAHIPLENDI' | 'BEKLEMEDE';
  olusturma_tarihi: string;
  sahip: Kullanici;
  kategoriler: Kategori[];
}

export interface Kategori {
  id: number;
  ad: string;
  aciklama?: string;
  ust_kategori?: number;
}

export interface Ilan {
  id: number;
  baslik: string;
  aciklama: string;
  fiyat?: number;
  konum: string;
  durumu: 'AKTIF' | 'PASIF' | 'TAMAMLANDI';
  ilan_tipi: 'SAHIPLENDIRME' | 'KAYIP' | 'BULUNDU' | 'BARINMA';
  olusturma_tarihi: string;
  guncellenme_tarihi: string;
  olusturan: Kullanici;
  hayvan: Hayvan;
}

export interface Basvuru {
  id: number;
  aciklama: string;
  durum: 'BEKLIYOR' | 'ONAYLANDI' | 'REDDEDILDI';
  olusturma_tarihi: string;
  basvuran: Kullanici;
  ilan: Ilan;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  results: T[];
  count: number;
  next?: string;
  previous?: string;
}

export interface Blog {
  id: number;
  baslik: string;
  icerik: string;
  ozet: string;
  kapak_resmi?: string;
  yazar: Kullanici;
  kategori?: Kategori;
  etiketler: string[];
  yayinlanma_tarihi: string;
  guncellenme_tarihi: string;
  goruntulenme_sayisi: number;
  begeni_sayisi: number;
  yorum_sayisi: number;
}

export interface Mesaj {
  id: number;
  gonderen: Kullanici;
  alici: Kullanici;
  icerik: string;
  okundu: boolean;
  gonderilme_tarihi: string;
  konusma_id: number;
}

export interface Etiket {
  id: number;
  ad: string;
  renk?: string;
  aciklama?: string;
}

export interface Bildirim {
  id: number;
  baslik: string;
  mesaj: string;
  tip: 'bilgi' | 'basari' | 'uyari' | 'hata';
  okundu: boolean;
  olusturma_tarihi: string;
  alici: Kullanici;
  ilgili_nesne_tipi?: string;
  ilgili_nesne_id?: number;
}

// Redux State tipleri
export interface RootState {
  hayvanlar: HayvanState;
  ilanlar: IlanState;
  blog: BlogState;
  favoriler: FavorilerState;
  bildirimler: BildirimState;
}

export interface HayvanState {
  liste: Hayvan[];
  yukleniyor: boolean;
  hata: string | null;
  toplamSayfa: number;
  mevcutSayfa: number;
  toplam: number;
  seciliHayvan: Hayvan | null;
  filtreler: any;
}

export interface IlanState {
  liste: Ilan[];
  yukleniyor: boolean;
  hata: string | null;
  seciliIlan: Ilan | null;
}

export interface BlogState {
  liste: Blog[];
  yukleniyor: boolean;
  hata: string | null;
  seciliBlog: Blog | null;
}

export interface FavorilerState {
  liste: number[];
  yukleniyor: boolean;
}

export interface BildirimState {
  liste: Bildirim[];
  okunmayanSayisi: number;
  yukleniyor: boolean;
}
