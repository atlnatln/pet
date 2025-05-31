import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import { Kullanici } from '../types';
import api from '../hizmetler/api';

interface AuthState {
  kullanici: Kullanici | null;
  token: string | null;
  yukleniyor: boolean;
  girisYapildi: boolean;
}

interface AuthAction {
  type: 'LOGIN_START' | 'LOGIN_SUCCESS' | 'LOGIN_FAILURE' | 'LOGOUT' | 'SET_USER';
  payload?: any;
}

interface AuthContextType {
  state: AuthState;
  girisYap: (email: string, sifre: string) => Promise<void>;
  kayitOl: (kullaniciData: any) => Promise<void>;
  cikisYap: () => void;
  kullaniciyiGuncelle: (kullanici: Kullanici) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, yukleniyor: true };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        yukleniyor: false,
        girisYapildi: true,
        kullanici: action.payload.kullanici,
        token: action.payload.token,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        yukleniyor: false,
        girisYapildi: false,
        kullanici: null,
        token: null,
      };
    case 'LOGOUT':
      return {
        ...state,
        kullanici: null,
        token: null,
        girisYapildi: false,
      };
    case 'SET_USER':
      return {
        ...state,
        kullanici: action.payload,
      };
    default:
      return state;
  }
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, {
    kullanici: null,
    token: localStorage.getItem('token'),
    yukleniyor: false,
    girisYapildi: !!localStorage.getItem('token'),
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Token varsa kullanıcı bilgilerini al
      getCurrentUser();
    }
  }, []);

  const getCurrentUser = async () => {
    try {
      const response = await api.get('/kullanicilar/profil/');
      dispatch({ type: 'SET_USER', payload: response.data });
    } catch (error) {
      localStorage.removeItem('token');
      dispatch({ type: 'LOGOUT' });
    }
  };

  const girisYap = async (email: string, sifre: string) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const response = await api.post('/auth/giris/', { email, sifre });
      const { kullanici, token } = response.data;
      
      localStorage.setItem('token', token);
      dispatch({ type: 'LOGIN_SUCCESS', payload: { kullanici, token } });
    } catch (error) {
      dispatch({ type: 'LOGIN_FAILURE' });
      throw error;
    }
  };

  const kayitOl = async (kullaniciData: any) => {
    try {
      const response = await api.post('/auth/kayit/', kullaniciData);
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  const cikisYap = () => {
    localStorage.removeItem('token');
    dispatch({ type: 'LOGOUT' });
  };

  const kullaniciyiGuncelle = (kullanici: Kullanici) => {
    dispatch({ type: 'SET_USER', payload: kullanici });
  };

  return (
    <AuthContext.Provider value={{
      state,
      girisYap,
      kayitOl,
      cikisYap,
      kullaniciyiGuncelle,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth, AuthProvider içinde kullanılmalıdır');
  }
  return context;
};
