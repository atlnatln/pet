import api from './api';
import { Blog, PaginatedResponse } from '../types';

export interface BlogFiltre {
  kategori?: string;
  etiket?: string;
  arama?: string;
  sayfa?: number;
  sayfa_boyutu?: number;
}

export const blogService = {
  async blogListesi(filtreler: BlogFiltre = {}): Promise<PaginatedResponse<Blog>> {
    const params = new URLSearchParams();
    Object.entries(filtreler).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, value.toString());
      }
    });

    const response = await api.get(`/blog/?${params.toString()}`);
    return response.data;
  },

  async blogDetay(id: number): Promise<Blog> {
    const response = await api.get(`/blog/${id}/`);
    return response.data;
  },

  async blogOlustur(blogData: Partial<Blog>): Promise<Blog> {
    const response = await api.post('/blog/', blogData);
    return response.data;
  },

  async blogGuncelle(id: number, blogData: Partial<Blog>): Promise<Blog> {
    const response = await api.patch(`/blog/${id}/`, blogData);
    return response.data;
  },

  async blogSil(id: number): Promise<void> {
    await api.delete(`/blog/${id}/`);
  },

  async populerBloglar(): Promise<Blog[]> {
    const response = await api.get('/blog/populer/');
    return response.data.results;
  },

  async benimBloglarim(): Promise<Blog[]> {
    const response = await api.get('/blog/benim-bloglarim/');
    return response.data.results;
  },
};
