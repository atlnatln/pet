import api from './api';
import { Kullanici, ApiResponse } from '../types';

export interface KullaniciKayitData {
  kullanici_adi: string;
  email: string;
  sifre: string;
  ad: string;
  soyad: string;
  telefon?: string;
  adres?: string;
}

export interface KullaniciGuncelleData {
  ad?: string;
  soyad?: string;
  telefon?: string;
  adres?: string;
  profil_resmi?: File;
}

export interface SifreDegistirData {
  eski_sifre: string;
  yeni_sifre: string;
  yeni_sifre_tekrar: string;
}

export const kullaniciService = {
  async profil(): Promise<Kullanici> {
    const response = await api.get('/kullanicilar/profil/');
    return response.data;
  },

  async profilGuncelle(data: KullaniciGuncelleData): Promise<Kullanici> {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        formData.append(key, value);
      }
    });

    const response = await api.patch('/kullanicilar/profil/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async sifreDegistir(data: SifreDegistirData): Promise<ApiResponse<void>> {
    const response = await api.post('/kullanicilar/sifre-degistir/', data);
    return response.data;
  },

  async hesapSil(): Promise<void> {
    await api.delete('/kullanicilar/profil/');
  },

  async emailDogrula(token: string): Promise<ApiResponse<void>> {
    const response = await api.post('/kullanicilar/email-dogrula/', { token });
    return response.data;
  },

  async emailDogrulamaTekrarGonder(): Promise<ApiResponse<void>> {
    const response = await api.post('/kullanicilar/email-dogrulama-tekrar/');
    return response.data;
  },

  async sifreSifirlamaTalebi(email: string): Promise<ApiResponse<void>> {
    const response = await api.post('/kullanicilar/sifre-sifirlama-talebi/', { email });
    return response.data;
  },

  async sifreSifirlama(token: string, yeni_sifre: string): Promise<ApiResponse<void>> {
    const response = await api.post('/kullanicilar/sifre-sifirlama/', {
      token,
      yeni_sifre,
    });
    return response.data;
  },

  async kullaniciDetay(id: number): Promise<Kullanici> {
    const response = await api.get(`/kullanicilar/${id}/`);
    return response.data;
  },
};
