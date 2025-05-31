import React from 'react';
import { useFavoriler } from '../../kancalar/useFavoriler';

interface FavoriButonuProps {
  hayvanId: number;
  className?: string;
  boyut?: 'kucuk' | 'orta' | 'buyuk';
}

const FavoriButonu: React.FC<FavoriButonuProps> = ({
  hayvanId,
  className = '',
  boyut = 'orta',
}) => {
  const { favoriyeMi, favoriDegistir } = useFavoriler();
  const isFavori = favoriyeMi(hayvanId);

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    favoriDegistir(hayvanId);
  };

  return (
    <button
      className={`favori-butonu favori-butonu--${boyut} ${isFavori ? 'favori-butonu--aktif' : ''} ${className}`}
      onClick={handleClick}
      aria-label={isFavori ? 'Favorilerden çıkar' : 'Favorilere ekle'}
      title={isFavori ? 'Favorilerden çıkar' : 'Favorilere ekle'}
    >
      <span className="favori-butonu__ikon">
        {isFavori ? '❤️' : '🤍'}
      </span>
    </button>
  );
};

export default FavoriButonu;
