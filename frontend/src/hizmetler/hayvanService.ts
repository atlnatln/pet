import api from './api';
import { Hayvan, PaginatedResponse, ApiResponse } from '../types';

export interface HayvanFiltre {
  tur?: string;
  cins?: string;
  yas_min?: number;
  yas_max?: number;
  cinsiyet?: 'E' | 'D';
  konum?: string;
  sahiplendirme_durumu?: 'MEVCUT' | 'SAHIPLENDI' | 'BEKLEMEDE';
  sayfa?: number;
  sayfa_boyutu?: number;
}

export const hayvanService = {
  async hayvanlarListesi(filtreler: HayvanFiltre = {}): Promise<PaginatedResponse<Hayvan>> {
    const params = new URLSearchParams();
    Object.entries(filtreler).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, value.toString());
      }
    });

    const response = await api.get(`/hayvanlar/?${params.toString()}`);
    return response.data;
  },

  async hayvanDetay(id: number): Promise<Hayvan> {
    const response = await api.get(`/hayvanlar/${id}/`);
    return response.data;
  },

  async hayvanOlustur(hayvanData: FormData): Promise<Hayvan> {
    const response = await api.post('/hayvanlar/', hayvanData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async hayvanGuncelle(id: number, hayvanData: FormData): Promise<Hayvan> {
    const response = await api.patch(`/hayvanlar/${id}/`, hayvanData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async hayvanSil(id: number): Promise<void> {
    await api.delete(`/hayvanlar/${id}/`);
  },

  async benimHayvanlarim(): Promise<Hayvan[]> {
    const response = await api.get('/hayvanlar/benim-hayvanlarim/');
    return response.data.results;
  },

  async popülerHayvanlar(): Promise<Hayvan[]> {
    const response = await api.get('/hayvanlar/populer/');
    return response.data.results;
  },

  async rastgeleHayvanlar(adet: number = 6): Promise<Hayvan[]> {
    const response = await api.get(`/hayvanlar/rastgele/?adet=${adet}`);
    return response.data.results;
  },
};
