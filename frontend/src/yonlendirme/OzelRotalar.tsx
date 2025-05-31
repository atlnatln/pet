import React, { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../baglamlar/AuthContext';
import YuklemeDurumu from '../bilesenler/ortak/YuklemeDurumu';

interface OzelRotalarProps {
  children: ReactNode;
}

const OzelRotalar: React.FC<OzelRotalarProps> = ({ children }) => {
  const { state } = useAuth();

  if (state.yukleniyor) {
    return <YuklemeDurumu merkezde mesaj="Yetkilendirme kontrol ediliyor..." />;
  }

  if (!state.girisYapildi) {
    return <Navigate to="/giris" replace />;
  }

  return <>{children}</>;
};

export default OzelRotalar;
