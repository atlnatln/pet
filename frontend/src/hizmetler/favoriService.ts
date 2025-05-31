import api from './api';
import { Hayvan, PaginatedResponse } from '../types';

interface Favori {
  id: number;
  hayvan: Hayvan;
  olusturma_tarihi: string;
}

export const favoriService = {
  async favorilerim(): Promise<Favori[]> {
    const response = await api.get('/favoriler/');
    return response.data.results;
  },

  async favoriyeEkle(hayvanId: number): Promise<Favori> {
    const response = await api.post('/favoriler/', { hayvan: hayvanId });
    return response.data;
  },

  async favoridanKaldir(hayvanId: number): Promise<void> {
    await api.delete(`/favoriler/hayvan/${hayvanId}/`);
  },

  async favoriMi(hayvanId: number): Promise<boolean> {
    try {
      const response = await api.get(`/favoriler/kontrol/${hayvanId}/`);
      return response.data.favori;
    } catch (error) {
      return false;
    }
  },
};
