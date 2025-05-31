import React from 'react';
import { Link } from 'react-router-dom';
import { Ilan } from '../../types';
import { tarihYardimcilari } from '../../yardimcilar/tarih';

interface IlanKartiProps {
  ilan: Ilan;
  className?: string;
}

const IlanKarti: React.FC<IlanKartiProps> = ({ ilan, className = '' }) => {
  return (
    <div className={`ilan-karti ${className}`}>
      <div className="ilan-karti__header">
        <h3 className="ilan-karti__baslik">
          <Link to={`/ilanlar/${ilan.id}`}>{ilan.baslik}</Link>
        </h3>
        <span className={`ilan-karti__durum ilan-karti__durum--${ilan.durumu.toLowerCase()}`}>
          {ilan.durumu}
        </span>
      </div>

      <div className="ilan-karti__icerik">
        <p className="ilan-karti__aciklama">
          {ilan.aciklama.substring(0, 150)}...
        </p>
        
        <div className="ilan-karti__bilgiler">
          <span className="ilan-karti__konum">{ilan.konum}</span>
          <span className="ilan-karti__tarih">
            {tarihYardimcilari.goreceli(ilan.olusturma_tarihi)}
          </span>
          {ilan.fiyat && (
            <span className="ilan-karti__fiyat">₺{ilan.fiyat}</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default IlanKarti;
