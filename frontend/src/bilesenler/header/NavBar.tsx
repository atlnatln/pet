import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../baglamlar/AuthContext';
import AramaKutusu from './AramaKutusu';
import KullaniciMenu from './KullaniciMenu';

const NavBar: React.FC = () => {
  const [mobileMenuAcik, setMobileMenuAcik] = useState(false);
  const { state } = useAuth();
  const location = useLocation();

  const menuItems = [
    { to: '/', label: 'Ana Sayfa' },
    { to: '/hayvanlar', label: 'Hayvanlar' },
    { to: '/blog', label: 'Blog' },
    { to: '/hakkimizda', label: 'Hakkımızda' },
  ];

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar">
      <div className="navbar__container">
        <div className="navbar__brand">
          <Link to="/" className="navbar__logo">
            🐾 Pet Platform
          </Link>
        </div>

        {/* Desktop Menu */}
        <div className="navbar__menu">
          <ul className="navbar__nav">
            {menuItems.map((item) => (
              <li key={item.to} className="navbar__item">
                <Link
                  to={item.to}
                  className={`navbar__link ${
                    isActive(item.to) ? 'navbar__link--active' : ''
                  }`}
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* Search */}
        <div className="navbar__search">
          <AramaKutusu />
        </div>

        {/* User Menu */}
        <div className="navbar__user">
          {state.girisYapildi ? (
            <KullaniciMenu />
          ) : (
            <div className="navbar__auth">
              <Link to="/giris" className="navbar__link">
                Giriş
              </Link>
              <Link to="/kayit" className="navbar__link navbar__link--primary">
                Kayıt Ol
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button
          className="navbar__toggle"
          onClick={() => setMobileMenuAcik(!mobileMenuAcik)}
          aria-label="Menüyü aç/kapat"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuAcik && (
        <div className="navbar__mobile">
          <ul className="navbar__mobile-nav">
            {menuItems.map((item) => (
              <li key={item.to} className="navbar__mobile-item">
                <Link
                  to={item.to}
                  className={`navbar__mobile-link ${
                    isActive(item.to) ? 'navbar__mobile-link--active' : ''
                  }`}
                  onClick={() => setMobileMenuAcik(false)}
                >
                  {item.label}
                </Link>
              </li>
            ))}
            
            {!state.girisYapildi && (
              <>
                <li className="navbar__mobile-item">
                  <Link
                    to="/giris"
                    className="navbar__mobile-link"
                    onClick={() => setMobileMenuAcik(false)}
                  >
                    Giriş
                  </Link>
                </li>
                <li className="navbar__mobile-item">
                  <Link
                    to="/kayit"
                    className="navbar__mobile-link navbar__mobile-link--primary"
                    onClick={() => setMobileMenuAcik(false)}
                  >
                    Kayıt Ol
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>
      )}
    </nav>
  );
};

export default NavBar;
