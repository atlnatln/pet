export const emailDogrula = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const telefonDogrula = (telefon: string): boolean => {
  const telefonRegex = /^[0-9]{10,11}$/;
  return telefonRegex.test(telefon.replace(/\s+/g, ''));
};

export const sifreDogrula = (sifre: string): boolean => {
  return sifre.length >= 8;
};

export const zorunluAlanDogrula = (deger: string): boolean => {
  return deger.trim().length > 0;
};

export const yasDogrula = (yas: number): boolean => {
  return yas > 0 && yas <= 30;
};
