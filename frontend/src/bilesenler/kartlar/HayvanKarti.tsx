import React from 'react';
import { Link } from 'react-router-dom';
import { Hayvan } from '../../types';
import FavoriButonu from '../ozel/FavoriButonu';
import YasBilgisi from '../ozel/YasBilgisi';

interface HayvanKartiProps {
  hayvan: Hayvan;
  className?: string;
}

const HayvanKarti: React.FC<HayvanKartiProps> = ({ hayvan, className = '' }) => {
  return (
    <div className={`hayvan-karti ${className}`}>
      <div className="hayvan-karti__resim">
        <Link to={`/hayvanlar/${hayvan.id}`}>
          <img
            src={hayvan.resimler[0] || '/default-pet.jpg'}
            alt={hayvan.ad}
            className="hayvan-karti__img"
          />
        </Link>
        <FavoriButonu hayvanId={hayvan.id} className="hayvan-karti__favori" />
      </div>

      <div className="hayvan-karti__icerik">
        <h3 className="hayvan-karti__baslik">
          <Link to={`/hayvanlar/${hayvan.id}`}>{hayvan.ad}</Link>
        </h3>
        
        <div className="hayvan-karti__bilgiler">
          <span className="hayvan-karti__cins">{hayvan.cins}</span>
          <YasBilgisi yas={hayvan.yas} />
          <span className="hayvan-karti__konum">{hayvan.konum}</span>
        </div>

        <p className="hayvan-karti__aciklama">
          {hayvan.aciklama.substring(0, 100)}...
        </p>
      </div>
    </div>
  );
};

export default HayvanKarti;
