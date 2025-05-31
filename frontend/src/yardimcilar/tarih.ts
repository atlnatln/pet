export const tarihYardimcilari = {
  // Tarih formatı
  format: (tarih: string | Date, format: 'kisa' | 'uzun' | 'saat' = 'kisa'): string => {
    const tarihNesnesi = typeof tarih === 'string' ? new Date(tarih) : tarih;
    
    if (isNaN(tarihNesnesi.getTime())) {
      return 'Geçersiz tarih';
    }

    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: format === 'uzun' ? 'long' : '2-digit',
      day: '2-digit',
    };

    if (format === 'saat') {
      options.hour = '2-digit';
      options.minute = '2-digit';
    }

    return new Intl.DateTimeFormat('tr-TR', options).format(tarihNesnesi);
  },

  // Göreceli zaman (örn: "2 saat önce")
  goreceli: (tarih: string | Date): string => {
    const tarihNesnesi = typeof tarih === 'string' ? new Date(tarih) : tarih;
    const simdi = new Date();
    const fark = simdi.getTime() - tarihNesnesi.getTime();
    
    const saniye = Math.floor(fark / 1000);
    const dakika = Math.floor(saniye / 60);
    const saat = Math.floor(dakika / 60);
    const gun = Math.floor(saat / 24);
    const hafta = Math.floor(gun / 7);
    const ay = Math.floor(gun / 30);
    const yil = Math.floor(gun / 365);

    if (yil > 0) return `${yil} yıl önce`;
    if (ay > 0) return `${ay} ay önce`;
    if (hafta > 0) return `${hafta} hafta önce`;
    if (gun > 0) return `${gun} gün önce`;
    if (saat > 0) return `${saat} saat önce`;
    if (dakika > 0) return `${dakika} dakika önce`;
    return 'Az önce';
  },

  // Yaş hesaplama
  yasHesapla: (dogumTarihi: string | Date): number => {
    const dogum = typeof dogumTarihi === 'string' ? new Date(dogumTarihi) : dogumTarihi;
    const bugün = new Date();
    
    let yas = bugün.getFullYear() - dogum.getFullYear();
    const ayFarki = bugün.getMonth() - dogum.getMonth();
    
    if (ayFarki < 0 || (ayFarki === 0 && bugün.getDate() < dogum.getDate())) {
      yas--;
    }
    
    return yas;
  },

  // Tarih aralığı kontrolü
  araliktaMi: (tarih: string | Date, baslangic: string | Date, bitis: string | Date): boolean => {
    const kontrol = typeof tarih === 'string' ? new Date(tarih) : tarih;
    const bas = typeof baslangic === 'string' ? new Date(baslangic) : baslangic;
    const bit = typeof bitis === 'string' ? new Date(bitis) : bitis;
    
    return kontrol >= bas && kontrol <= bit;
  },

  // Bugün mü?
  bugunMu: (tarih: string | Date): boolean => {
    const kontrol = typeof tarih === 'string' ? new Date(tarih) : tarih;
    const bugün = new Date();
    
    return kontrol.toDateString() === bugün.toDateString();
  },

  // Bu hafta mı?
  buHaftaMi: (tarih: string | Date): boolean => {
    const kontrol = typeof tarih === 'string' ? new Date(tarih) : tarih;
    const bugün = new Date();
    const haftaBaslangici = new Date(bugün.setDate(bugün.getDate() - bugün.getDay()));
    const haftaSonu = new Date(haftaBaslangici.getTime() + 6 * 24 * 60 * 60 * 1000);
    
    return tarihYardimcilari.araliktaMi(kontrol, haftaBaslangici, haftaSonu);
  },

  // Tarih string'ini ISO formatına çevirme
  isoFormat: (tarih: Date): string => {
    return tarih.toISOString().split('T')[0];
  },

  // Türkçe gün adı
  gunAdi: (tarih: string | Date): string => {
    const tarihNesnesi = typeof tarih === 'string' ? new Date(tarih) : tarih;
    const gunler = ['Pazar', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'];
    return gunler[tarihNesnesi.getDay()];
  },

  // Türkçe ay adı
  ayAdi: (tarih: string | Date): string => {
    const tarihNesnesi = typeof tarih === 'string' ? new Date(tarih) : tarih;
    const aylar = [
      'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
      'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
    ];
    return aylar[tarihNesnesi.getMonth()];
  },
};
