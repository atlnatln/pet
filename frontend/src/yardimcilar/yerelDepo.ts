export const yerelDepo = {
  // Veri kaydetme
  kaydet: <T>(anahtar: string, deger: T): void => {
    try {
      const json = JSON.stringify(deger);
      localStorage.setItem(anahtar, json);
    } catch (error) {
      console.error('LocalStorage kaydetme hatası:', error);
    }
  },

  // Veri okuma
  oku: <T>(anahtar: string, varsayilan?: T): T | null => {
    try {
      const item = localStorage.getItem(anahtar);
      if (item === null) {
        return varsayilan || null;
      }
      return JSON.parse(item) as T;
    } catch (error) {
      console.error('LocalStorage okuma hatası:', error);
      return varsayilan || null;
    }
  },

  // Veri silme
  sil: (anahtar: string): void => {
    try {
      localStorage.removeItem(anahtar);
    } catch (error) {
      console.error('LocalStorage silme hatası:', error);
    }
  },

  // Tüm verileri temizleme
  temizle: (): void => {
    try {
      localStorage.clear();
    } catch (error) {
      console.error('LocalStorage temizleme hatası:', error);
    }
  },

  // Anahtar varlık kontrolü
  varMi: (anahtar: string): boolean => {
    return localStorage.getItem(anahtar) !== null;
  },

  // Tüm anahtarları listeleme
  anahtarlar: (): string[] => {
    const anahtarlar: string[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const anahtar = localStorage.key(i);
      if (anahtar) {
        anahtarlar.push(anahtar);
      }
    }
    return anahtarlar;
  },

  // LocalStorage boyutu hesaplama (KB)
  boyut: (): number => {
    let toplam = 0;
    for (const anahtar in localStorage) {
      if (localStorage.hasOwnProperty(anahtar)) {
        toplam += localStorage[anahtar].length + anahtar.length;
      }
    }
    return Math.round(toplam / 1024 * 100) / 100; // KB cinsinden
  },

  // Token işlemleri
  token: {
    kaydet: (token: string): void => {
      yerelDepo.kaydet('auth_token', token);
    },
    
    oku: (): string | null => {
      return yerelDepo.oku<string>('auth_token');
    },
    
    sil: (): void => {
      yerelDepo.sil('auth_token');
    },
    
    varMi: (): boolean => {
      return yerelDepo.varMi('auth_token');
    },
  },

  // Kullanıcı tercihleri
  tercihler: {
    tema: {
      kaydet: (tema: 'acik' | 'koyu'): void => {
        yerelDepo.kaydet('tema', tema);
      },
      
      oku: (): 'acik' | 'koyu' => {
        return yerelDepo.oku<'acik' | 'koyu'>('tema', 'acik');
      },
    },
    
    dil: {
      kaydet: (dil: string): void => {
        yerelDepo.kaydet('dil', dil);
      },
      
      oku: (): string => {
        return yerelDepo.oku<string>('dil', 'tr');
      },
    },
    
    sayfaBoyutu: {
      kaydet: (boyut: number): void => {
        yerelDepo.kaydet('sayfa_boyutu', boyut);
      },
      
      oku: (): number => {
        return yerelDepo.oku<number>('sayfa_boyutu', 12);
      },
    },
  },
};
