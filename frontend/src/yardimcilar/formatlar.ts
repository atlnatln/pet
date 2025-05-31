export const formatlar = {
  // Para formatı
  para: (miktar: number): string => {
    return new Intl.NumberFormat('tr-TR', {
      style: 'currency',
      currency: 'TRY',
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    }).format(miktar);
  },

  // Sayı formatı
  sayi: (sayi: number): string => {
    return new Intl.NumberFormat('tr-TR').format(sayi);
  },

  // Telefon formatı
  telefon: (telefon: string): string => {
    const temizTelefon = telefon.replace(/\D/g, '');
    if (temizTelefon.length === 11) {
      return `${temizTelefon.slice(0, 4)} ${temizTelefon.slice(4, 7)} ${temizTelefon.slice(7, 9)} ${temizTelefon.slice(9)}`;
    }
    if (temizTelefon.length === 10) {
      return `${temizTelefon.slice(0, 3)} ${temizTelefon.slice(3, 6)} ${temizTelefon.slice(6, 8)} ${temizTelefon.slice(8)}`;
    }
    return telefon;
  },

  // Metni kısaltma
  metinKisalt: (metin: string, uzunluk: number = 100): string => {
    if (metin.length <= uzunluk) return metin;
    return metin.slice(0, uzunluk).trim() + '...';
  },

  // İlk harfi büyük yapma
  ilkHarfBuyuk: (metin: string): string => {
    if (!metin) return '';
    return metin.charAt(0).toUpperCase() + metin.slice(1).toLowerCase();
  },

  // Tüm kelimelerin ilk harfini büyük yapma
  baslikFormat: (metin: string): string => {
    if (!metin) return '';
    return metin
      .split(' ')
      .map(kelime => formatlar.ilkHarfBuyuk(kelime))
      .join(' ');
  },

  // URL slug formatı
  slug: (metin: string): string => {
    const turkceKarakterler: { [key: string]: string } = {
      'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
      'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
    };

    return metin
      .toLowerCase()
      .replace(/[çğıöşü]/g, (karakter) => turkceKarakterler[karakter] || karakter)
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim();
  },

  // Dosya boyutu formatı
  dosyaBoyutu: (byte: number): string => {
    if (byte === 0) return '0 B';
    
    const birimler = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(byte) / Math.log(1024));
    
    return Math.round(byte / Math.pow(1024, i) * 100) / 100 + ' ' + birimler[i];
  },

  // Yaş formatı
  yas: (yas: number): string => {
    if (yas < 1) {
      const ay = Math.round(yas * 12);
      return `${ay} aylık`;
    }
    return `${yas} yaşında`;
  },

  // Cinsiyet formatı
  cinsiyet: (cinsiyet: 'E' | 'D'): string => {
    return cinsiyet === 'E' ? 'Erkek' : 'Dişi';
  },
};
