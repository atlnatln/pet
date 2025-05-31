import api from './api';
import { Ilan, PaginatedResponse } from '../types';

export interface IlanFiltre {
  ilan_tipi?: 'SAHIPLENDIRME' | 'KAYIP' | 'BULUNDU' | 'BARINMA';
  konum?: string;
  fiyat_min?: number;
  fiyat_max?: number;
  durumu?: 'AKTIF' | 'PASIF' | 'TAMAMLANDI';
  sayfa?: number;
  sayfa_boyutu?: number;
}

export const ilanService = {
  async ilanListesi(filtreler: IlanFiltre = {}): Promise<PaginatedResponse<Ilan>> {
    const params = new URLSearchParams();
    Object.entries(filtreler).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, value.toString());
      }
    });

    const response = await api.get(`/ilanlar/?${params.toString()}`);
    return response.data;
  },

  async ilanDetay(id: number): Promise<Ilan> {
    const response = await api.get(`/ilanlar/${id}/`);
    return response.data;
  },

  async ilanOlustur(ilanData: FormData): Promise<Ilan> {
    const response = await api.post('/ilanlar/', ilanData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async ilanGuncelle(id: number, ilanData: FormData): Promise<Ilan> {
    const response = await api.patch(`/ilanlar/${id}/`, ilanData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async ilanSil(id: number): Promise<void> {
    await api.delete(`/ilanlar/${id}/`);
  },

  async benimIlanlarim(): Promise<Ilan[]> {
    const response = await api.get('/ilanlar/benim-ilanlarim/');
    return response.data.results;
  },
};
