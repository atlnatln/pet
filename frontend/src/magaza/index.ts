import { configureStore } from '@reduxjs/toolkit';
import hayvanReducer from './reducers/hayvanReducer';
import ilanReducer from './reducers/ilanReducer';
import blogReducer from './reducers/blogReducer';

export const store = configureStore({
  reducer: {
    hayvanlar: hayvanReducer,
    ilanlar: ilanReducer,
    blog: blogReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// React-Redux hooks
export { useDispatch, useSelector } from 'react-redux';
