import { useState, useCallback, useMemo } from 'react';

interface UsePaginationOptions {
  baslangicSayfasi?: number;
  sayfaBoyutu?: number;
  toplamEleman?: number;
}

interface UsePaginationReturn {
  mevcutSayfa: number;
  sayfaBoyutu: number;
  toplamSayfa: number;
  sonrakiSayfa: () => void;
  oncekiSayfa: () => void;
  sayfayaGit: (sayfa: number) => void;
  sayfaBoyutunuDegistir: (boyut: number) => void;
  toplamElemaniAyarla: (toplam: number) => void;
  ilkSayfa: boolean;
  sonSayfa: boolean;
  offset: number;
}

export function usePagination({
  baslangicSayfasi = 1,
  sayfaBoyutu: baslangicSayfaBoyutu = 10,
  toplamEleman: baslangicToplamEleman = 0,
}: UsePaginationOptions = {}): UsePaginationReturn {
  const [mevcutSayfa, setMevcutSayfa] = useState(baslangicSayfasi);
  const [sayfaBoyutu, setSayfaBoyutu] = useState(baslangicSayfaBoyutu);
  const [toplamEleman, setToplamEleman] = useState(baslangicToplamEleman);

  const toplamSayfa = useMemo(() => {
    return Math.ceil(toplamEleman / sayfaBoyutu);
  }, [toplamEleman, sayfaBoyutu]);

  const offset = useMemo(() => {
    return (mevcutSayfa - 1) * sayfaBoyutu;
  }, [mevcutSayfa, sayfaBoyutu]);

  const ilkSayfa = mevcutSayfa === 1;
  const sonSayfa = mevcutSayfa === toplamSayfa || toplamSayfa === 0;

  const sonrakiSayfa = useCallback(() => {
    if (!sonSayfa) {
      setMevcutSayfa(prev => prev + 1);
    }
  }, [sonSayfa]);

  const oncekiSayfa = useCallback(() => {
    if (!ilkSayfa) {
      setMevcutSayfa(prev => prev - 1);
    }
  }, [ilkSayfa]);

  const sayfayaGit = useCallback((sayfa: number) => {
    if (sayfa >= 1 && sayfa <= toplamSayfa) {
      setMevcutSayfa(sayfa);
    }
  }, [toplamSayfa]);

  const sayfaBoyutunuDegistir = useCallback((boyut: number) => {
    setSayfaBoyutu(boyut);
    setMevcutSayfa(1); // Sayfa boyutu değiştiğinde ilk sayfaya dön
  }, []);

  const toplamElemaniAyarla = useCallback((toplam: number) => {
    setToplamEleman(toplam);
    
    // Eğer mevcut sayfa toplam sayfa sayısından büyükse, son sayfaya git
    const yeniToplamSayfa = Math.ceil(toplam / sayfaBoyutu);
    if (mevcutSayfa > yeniToplamSayfa && yeniToplamSayfa > 0) {
      setMevcutSayfa(yeniToplamSayfa);
    }
  }, [mevcutSayfa, sayfaBoyutu]);

  return {
    mevcutSayfa,
    sayfaBoyutu,
    toplamSayfa,
    sonrakiSayfa,
    oncekiSayfa,
    sayfayaGit,
    sayfaBoyutunuDegistir,
    toplamElemaniAyarla,
    ilkSayfa,
    sonSayfa,
    offset,
  };
}
