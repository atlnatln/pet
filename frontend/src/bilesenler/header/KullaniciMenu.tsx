import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../baglamlar/AuthContext';

const KullaniciMenu: React.FC = () => {
  const [menuAcik, setMenuAcik] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const { state, cikisYap } = useAuth();

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuAcik(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleCikis = () => {
    cikisYap();
    setMenuAcik(false);
  };

  return (
    <div className="kullanici-menu" ref={menuRef}>
      <button
        className="kullanici-menu__trigger"
        onClick={() => setMenuAcik(!menuAcik)}
      >
        <img
          src={state.kullanici?.profil_resmi || '/default-avatar.png'}
          alt={state.kullanici?.ad}
          className="kullanici-menu__avatar"
        />
        <span className="kullanici-menu__name">
          {state.kullanici?.ad} {state.kullanici?.soyad}
        </span>
      </button>

      {menuAcik && (
        <div className="kullanici-menu__dropdown">
          {/* Menu items will be implemented later */}
          <Link to="/profil" onClick={() => setMenuAcik(false)}>
            Profilim
          </Link>
          <Link to="/favoriler" onClick={() => setMenuAcik(false)}>
            Favorilerim
          </Link>
          <button onClick={handleCikis}>Çıkış</button>
        </div>
      )}
    </div>
  );
};

export default KullaniciMenu;
