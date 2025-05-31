import { useState, useEffect, useCallback } from 'react';
import { favoriService } from '../hizmetler/favoriService';
import { useBildirim } from '../baglamlar/BildirimBaglami';

interface UseFavorilerReturn {
  favoriler: number[];
  yukleniyor: boolean;
  favoriyeMi: (hayvanId: number) => boolean;
  favoriDegistir: (hayvanId: number) => Promise<void>;
  favorileriYukle: () => Promise<void>;
}

export function useFavoriler(): UseFavorilerReturn {
  const [favoriler, setFavoriler] = useState<number[]>([]);
  const [yukleniyor, setYukleniyor] = useState(false);
  const { hataBildirimi } = useBildirim();

  const favorileriYukle = useCallback(async () => {
    setYukleniyor(true);
    try {
      const response = await favoriService.favorilerim();
      const favoriIds = response.map(favori => favori.hayvan.id);
      setFavoriler(favoriIds);
    } catch (error) {
      console.error('Favoriler yüklenemedi:', error);
    } finally {
      setYukleniyor(false);
    }
  }, []);

  useEffect(() => {
    favorileriYukle();
  }, [favorileriYukle]);

  const favoriyeMi = useCallback((hayvanId: number): boolean => {
    return favoriler.includes(hayvanId);
  }, [favoriler]);

  const favoriDegistir = useCallback(async (hayvanId: number) => {
    try {
      const mevcutFavori = favoriyeMi(hayvanId);
      
      if (mevcutFavori) {
        await favoriService.favoridanKaldir(hayvanId);
        setFavoriler(prev => prev.filter(id => id !== hayvanId));
      } else {
        await favoriService.favoriyeEkle(hayvanId);
        setFavoriler(prev => [...prev, hayvanId]);
      }
    } catch (error) {
      hataBildirimi('Favori işlemi sırasında bir hata oluştu');
      console.error('Favori değiştirme hatası:', error);
    }
  }, [favoriyeMi, hataBildirimi]);

  return {
    favoriler,
    yukleniyor,
    favoriyeMi,
    favoriDegistir,
    favorileriYukle,
  };
}
