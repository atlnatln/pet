import { useState, useCallback, useMemo } from 'react';
import { HayvanFiltre } from '../hizmetler/hayvanService';

interface UseHayvanFiltreReturn {
  filtreler: HayvanFiltre;
  filtreEkle: (anahtar: keyof HayvanFiltre, deger: any) => void;
  filtreKaldir: (anahtar: keyof HayvanFiltre) => void;
  filtreleriSifirla: () => void;
  aktifFiltreSayisi: number;
  filtreliMi: boolean;
  queryString: string;
}

const baslangicFiltreleri: HayvanFiltre = {
  sayfa: 1,
  sayfa_boyutu: 12,
};

export function useHayvanFiltre(): UseHayvanFiltreReturn {
  const [filtreler, setFiltreler] = useState<HayvanFiltre>(baslangicFiltreleri);

  const filtreEkle = useCallback((anahtar: keyof HayvanFiltre, deger: any) => {
    setFiltreler(prev => ({
      ...prev,
      [anahtar]: deger,
      sayfa: anahtar === 'sayfa' ? deger : 1, // Yeni filtre eklenince ilk sayfaya dön
    }));
  }, []);

  const filtreKaldir = useCallback((anahtar: keyof HayvanFiltre) => {
    setFiltreler(prev => {
      const yeniFiltreler = { ...prev };
      delete yeniFiltreler[anahtar];
      return {
        ...yeniFiltreler,
        sayfa: 1, // Filtre kaldırılınca ilk sayfaya dön
      };
    });
  }, []);

  const filtreleriSifirla = useCallback(() => {
    setFiltreler(baslangicFiltreleri);
  }, []);

  const aktifFiltreSayisi = useMemo(() => {
    const sayilmayanlar = ['sayfa', 'sayfa_boyutu'];
    return Object.keys(filtreler).filter(key => 
      !sayilmayanlar.includes(key) && filtreler[key as keyof HayvanFiltre] !== undefined
    ).length;
  }, [filtreler]);

  const filtreliMi = aktifFiltreSayisi > 0;

  const queryString = useMemo(() => {
    const params = new URLSearchParams();
    Object.entries(filtreler).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString());
      }
    });
    return params.toString();
  }, [filtreler]);

  return {
    filtreler,
    filtreEkle,
    filtreKaldir,
    filtreleriSifirla,
    aktifFiltreSayisi,
    filtreliMi,
    queryString,
  };
}
