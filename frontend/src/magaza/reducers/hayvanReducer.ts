import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Hayvan, PaginatedResponse } from '../../types';
import { hayvanService, HayvanFiltre } from '../../hizmetler/hayvanService';

interface HayvanState {
  liste: Hayvan[];
  yukleniyor: boolean;
  hata: string | null;
  toplamSayfa: number;
  mevcutSayfa: number;
  toplam: number;
  seciliHayvan: Hayvan | null;
  filtreler: HayvanFiltre;
}

const initialState: HayvanState = {
  liste: [],
  yukleniyor: false,
  hata: null,
  toplamSayfa: 0,
  mevcutSayfa: 1,
  toplam: 0,
  seciliHayvan: null,
  filtreler: { sayfa: 1, sayfa_boyutu: 12 },
};

// Async thunks
export const hayvanlarGetir = createAsyncThunk(
  'hayvanlar/hayvanlarGetir',
  async (filtreler: HayvanFiltre) => {
    const response = await hayvanService.hayvanlarListesi(filtreler);
    return response;
  }
);

export const hayvanDetayGetir = createAsyncThunk(
  'hayvanlar/hayvanDetayGetir',
  async (id: number) => {
    const response = await hayvanService.hayvanDetay(id);
    return response;
  }
);

const hayvanSlice = createSlice({
  name: 'hayvanlar',
  initialState,
  reducers: {
    filtreleriAyarla: (state, action: PayloadAction<HayvanFiltre>) => {
      state.filtreler = action.payload;
    },
    hatayiTemizle: (state) => {
      state.hata = null;
    },
    seciliHayvaniTemizle: (state) => {
      state.seciliHayvan = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Hayvan listesi
      .addCase(hayvanlarGetir.pending, (state) => {
        state.yukleniyor = true;
        state.hata = null;
      })
      .addCase(hayvanlarGetir.fulfilled, (state, action) => {
        state.yukleniyor = false;
        state.liste = action.payload.results;
        state.toplam = action.payload.count;
        state.toplamSayfa = Math.ceil(action.payload.count / (state.filtreler.sayfa_boyutu || 12));
      })
      .addCase(hayvanlarGetir.rejected, (state, action) => {
        state.yukleniyor = false;
        state.hata = action.error.message || 'Bir hata oluştu';
      })
      // Hayvan detay
      .addCase(hayvanDetayGetir.fulfilled, (state, action) => {
        state.seciliHayvan = action.payload;
      });
  },
});

export const { filtreleriAyarla, hatayiTemizle, seciliHayvaniTemizle } = hayvanSlice.actions;
export default hayvanSlice.reducer;
