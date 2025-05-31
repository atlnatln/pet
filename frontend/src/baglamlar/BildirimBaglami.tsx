import React, { createContext, useContext, useState, ReactNode } from 'react';

interface Bildirim {
  id: string;
  mesaj: string;
  tip: 'basari' | 'hata' | 'uyari' | 'bilgi';
  gorunurSure?: number;
}

interface BildirimContextType {
  bildirimler: Bildirim[];
  bildirimEkle: (bildirim: Omit<Bildirim, 'id'>) => void;
  bildirimKaldir: (id: string) => void;
  basariBildirimi: (mesaj: string) => void;
  hataBildirimi: (mesaj: string) => void;
  uyariBildirimi: (mesaj: string) => void;
  bilgiBildirimi: (mesaj: string) => void;
}

const BildirimContext = createContext<BildirimContextType | undefined>(undefined);

interface BildirimProviderProps {
  children: ReactNode;
}

export const BildirimProvider: React.FC<BildirimProviderProps> = ({ children }) => {
  const [bildirimler, setBildirimler] = useState<Bildirim[]>([]);

  const bildirimEkle = (bildirim: Omit<Bildirim, 'id'>) => {
    const id = Date.now().toString();
    const yeniBildirim = { ...bildirim, id };
    
    setBildirimler(prev => [...prev, yeniBildirim]);

    // Otomatik kaldırma
    const sure = bildirim.gorunurSure || 5000;
    setTimeout(() => {
      bildirimKaldir(id);
    }, sure);
  };

  const bildirimKaldir = (id: string) => {
    setBildirimler(prev => prev.filter(bildirim => bildirim.id !== id));
  };

  const basariBildirimi = (mesaj: string) => {
    bildirimEkle({ mesaj, tip: 'basari' });
  };

  const hataBildirimi = (mesaj: string) => {
    bildirimEkle({ mesaj, tip: 'hata' });
  };

  const uyariBildirimi = (mesaj: string) => {
    bildirimEkle({ mesaj, tip: 'uyari' });
  };

  const bilgiBildirimi = (mesaj: string) => {
    bildirimEkle({ mesaj, tip: 'bilgi' });
  };

  return (
    <BildirimContext.Provider value={{
      bildirimler,
      bildirimEkle,
      bildirimKaldir,
      basariBildirimi,
      hataBildirimi,
      uyariBildirimi,
      bilgiBildirimi,
    }}>
      {children}
    </BildirimContext.Provider>
  );
};

export const useBildirim = (): BildirimContextType => {
  const context = useContext(BildirimContext);
  if (!context) {
    throw new Error('useBildirim, BildirimProvider içinde kullanılmalıdır');
  }
  return context;
};
