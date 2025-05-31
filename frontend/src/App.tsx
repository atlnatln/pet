import React from 'react';
import { Routes, Route } from 'react-router-dom';
import NavBar from './bilesenler/header/NavBar';
import Footer from './bilesenler/footer/Footer';
import Rotalar from './yonlendirme/Rotalar';
import BildirimToast from './bilesenler/ortak/BildirimToast';

const App: React.FC = () => {
  return (
    <div className="app">
      <NavBar />
      <main className="main-content">
        <Rotalar />
      </main>
      <Footer />
      <BildirimToast />
    </div>
  );
};

export default App;
