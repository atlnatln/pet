import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AnaSayfa from '../sayfalar/AnaSayfa';
import HayvanlarSayfasi from '../sayfalar/HayvanlarSayfasi';
import HayvanDetaySayfasi from '../sayfalar/HayvanDetaySayfasi';
import BlogSayfasi from '../sayfalar/BlogSayfasi';
import BlogDetaySayfasi from '../sayfalar/BlogDetaySayfasi';
import GirisSayfasi from '../sayfalar/GirisSayfasi';
import KayitSayfasi from '../sayfalar/KayitSayfasi';
import ProfilSayfasi from '../sayfalar/ProfilSayfasi';
import FavorilerSayfasi from '../sayfalar/FavorilerSayfasi';
import OzelRotalar from './OzelRotalar';

const Rotalar: React.FC = () => {
  return (
    <Routes>
      {/* Genel rotalar */}
      <Route path="/" element={<AnaSayfa />} />
      <Route path="/hayvanlar" element={<HayvanlarSayfasi />} />
      <Route path="/hayvanlar/:id" element={<HayvanDetaySayfasi />} />
      <Route path="/blog" element={<BlogSayfasi />} />
      <Route path="/blog/:id" element={<BlogDetaySayfasi />} />
      
      {/* Auth rotalar */}
      <Route path="/giris" element={<GirisSayfasi />} />
      <Route path="/kayit" element={<KayitSayfasi />} />
      
      {/* Korumalı rotalar */}
      <Route path="/profil" element={
        <OzelRotalar>
          <ProfilSayfasi />
        </OzelRotalar>
      } />
      <Route path="/favoriler" element={
        <OzelRotalar>
          <FavorilerSayfasi />
        </OzelRotalar>
      } />
    </Routes>
  );
};

export default Rotalar;
