import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { Ilan } from '../../types';
import { ilanService } from '../../hizmetler/ilanService';

interface IlanState {
  liste: Ilan[];
  yukleniyor: boolean;
  hata: string | null;
  seciliIlan: Ilan | null;
}

const initialState: IlanState = {
  liste: [],
  yukleniyor: false,
  hata: null,
  seciliIlan: null,
};

export const ilanlarGetir = createAsyncThunk(
  'ilanlar/ilanlarGetir',
  async (filtreler: any = {}) => {
    return await ilanService.ilanListesi(filtreler);
  }
);

export const ilanDetayGetir = createAsyncThunk(
  'ilanlar/ilanDetayGetir',
  async (id: number) => {
    return await ilanService.ilanDetay(id);
  }
);

const ilanSlice = createSlice({
  name: 'ilanlar',
  initialState,
  reducers: {
    hatayiTemizle: (state) => {
      state.hata = null;
    },
    seciliIlaniTemizle: (state) => {
      state.seciliIlan = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(ilanlarGetir.pending, (state) => {
        state.yukleniyor = true;
        state.hata = null;
      })
      .addCase(ilanlarGetir.fulfilled, (state, action) => {
        state.yukleniyor = false;
        state.liste = action.payload.results;
      })
      .addCase(ilanlarGetir.rejected, (state, action) => {
        state.yukleniyor = false;
        state.hata = action.error.message || 'Bir hata oluştu';
      })
      .addCase(ilanDetayGetir.fulfilled, (state, action) => {
        state.seciliIlan = action.payload;
      });
  },
});

export const { hatayiTemizle, seciliIlaniTemizle } = ilanSlice.actions;
export default ilanSlice.reducer;
