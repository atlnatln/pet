import { useState, useCallback } from 'react';

interface FormHatalari {
  [key: string]: string;
}

interface UseFormOptions<T> {
  baslangicDegerleri: T;
  dogrulama?: (degerler: T) => FormHatalari;
  onSubmit?: (degerler: T) => void | Promise<void>;
}

interface UseFormReturn<T> {
  degerler: T;
  hatalar: FormHatalari;
  dokunmus: { [K in keyof T]?: boolean };
  yukleniyor: boolean;
  degistir: (alan: keyof T, deger: any) => void;
  sifirla: () => void;
  gonder: (e?: React.FormEvent) => Promise<void>;
  alanHatasi: (alan: keyof T) => string | undefined;
  formGecerli: boolean;
}

export function useForm<T extends Record<string, any>>({
  baslangicDegerleri,
  dogrulama,
  onSubmit,
}: UseFormOptions<T>): UseFormReturn<T> {
  const [degerler, setDegerler] = useState<T>(baslangicDegerleri);
  const [hatalar, setHatalar] = useState<FormHatalari>({});
  const [dokunmus, setDokunmus] = useState<{ [K in keyof T]?: boolean }>({});
  const [yukleniyor, setYukleniyor] = useState(false);

  const dogrulamayiCalistir = useCallback((guncelDegerler: T): FormHatalari => {
    if (!dogrulama) return {};
    return dogrulama(guncelDegerler);
  }, [dogrulama]);

  const degistir = useCallback((alan: keyof T, deger: any) => {
    const yeniDegerler = { ...degerler, [alan]: deger };
    setDegerler(yeniDegerler);
    
    // Dokunmuş olarak işaretle
    setDokunmus(prev => ({ ...prev, [alan]: true }));
    
    // Doğrulamayı çalıştır
    const yeniHatalar = dogrulamayiCalistir(yeniDegerler);
    setHatalar(yeniHatalar);
  }, [degerler, dogrulamayiCalistir]);

  const sifirla = useCallback(() => {
    setDegerler(baslangicDegerleri);
    setHatalar({});
    setDokunmus({});
    setYukleniyor(false);
  }, [baslangicDegerleri]);

  const gonder = useCallback(async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    
    // Tüm alanları dokunmuş olarak işaretle
    const tumDokunmus = Object.keys(degerler).reduce((acc, key) => {
      acc[key as keyof T] = true;
      return acc;
    }, {} as { [K in keyof T]: boolean });
    setDokunmus(tumDokunmus);

    // Doğrulamayı çalıştır
    const yeniHatalar = dogrulamayiCalistir(degerler);
    setHatalar(yeniHatalar);

    // Hata varsa gönderme
    if (Object.keys(yeniHatalar).length > 0) {
      return;
    }

    if (onSubmit) {
      setYukleniyor(true);
      try {
        await onSubmit(degerler);
      } finally {
        setYukleniyor(false);
      }
    }
  }, [degerler, dogrulamayiCalistir, onSubmit]);

  const alanHatasi = useCallback((alan: keyof T): string | undefined => {
    return dokunmus[alan] ? hatalar[alan as string] : undefined;
  }, [hatalar, dokunmus]);

  const formGecerli = Object.keys(hatalar).length === 0;

  return {
    degerler,
    hatalar,
    dokunmus,
    yukleniyor,
    degistir,
    sifirla,
    gonder,
    alanHatasi,
    formGecerli,
  };
}
