import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { Blog } from '../../types';
import { blogService } from '../../hizmetler/blogService';

interface BlogState {
  liste: Blog[];
  yukleniyor: boolean;
  hata: string | null;
  seciliBlog: Blog | null;
}

const initialState: BlogState = {
  liste: [],
  yukleniyor: false,
  hata: null,
  seciliBlog: null,
};

export const bloglarGetir = createAsyncThunk(
  'blog/bloglarGetir',
  async (filtreler: any = {}) => {
    return await blogService.blogListesi(filtreler);
  }
);

export const blogDetayGetir = createAsyncThunk(
  'blog/blogDetayGetir',
  async (id: number) => {
    return await blogService.blogDetay(id);
  }
);

const blogSlice = createSlice({
  name: 'blog',
  initialState,
  reducers: {
    hatayiTemizle: (state) => {
      state.hata = null;
    },
    seciliBloguTemizle: (state) => {
      state.seciliBlog = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(bloglarGetir.pending, (state) => {
        state.yukleniyor = true;
        state.hata = null;
      })
      .addCase(bloglarGetir.fulfilled, (state, action) => {
        state.yukleniyor = false;
        state.liste = action.payload.results;
      })
      .addCase(bloglarGetir.rejected, (state, action) => {
        state.yukleniyor = false;
        state.hata = action.error.message || 'Bir hata oluştu';
      })
      .addCase(blogDetayGetir.fulfilled, (state, action) => {
        state.seciliBlog = action.payload;
      });
  },
});

export const { hatayiTemizle, seciliBloguTemizle } = blogSlice.actions;
export default blogSlice.reducer;
