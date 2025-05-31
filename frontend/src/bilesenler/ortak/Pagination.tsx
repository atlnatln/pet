import React from 'react';

interface PaginationProps {
  mevcutSayfa: number;
  toplamSayfa: number;
  onSayfaDegistir: (sayfa: number) => void;
  gosterilecekSayfaSayisi?: number;
  className?: string;
}

const Pagination: React.FC<PaginationProps> = ({
  mevcutSayfa,
  toplamSayfa,
  onSayfaDegistir,
  gosterilecekSayfaSayisi = 5,
  className = '',
}) => {
  if (toplamSayfa <= 1) return null;

  const sayfalar: number[] = [];
  const yarim = Math.floor(gosterilecekSayfaSayisi / 2);
  
  let baslangic = Math.max(1, mevcutSayfa - yarim);
  let bitis = Math.min(toplamSayfa, baslangic + gosterilecekSayfaSayisi - 1);
  
  // Sağa hizalama
  if (bitis - baslangic + 1 < gosterilecekSayfaSayisi) {
    baslangic = Math.max(1, bitis - gosterilecekSayfaSayisi + 1);
  }

  for (let i = baslangic; i <= bitis; i++) {
    sayfalar.push(i);
  }

  return (
    <nav className={`pagination ${className}`} aria-label="Sayfa navigasyonu">
      <ul className="pagination__liste">
        {/* İlk sayfa */}
        <li className="pagination__item">
          <button
            className="pagination__link"
            onClick={() => onSayfaDegistir(1)}
            disabled={mevcutSayfa === 1}
            aria-label="İlk sayfa"
          >
            «
          </button>
        </li>

        {/* Önceki sayfa */}
        <li className="pagination__item">
          <button
            className="pagination__link"
            onClick={() => onSayfaDegistir(mevcutSayfa - 1)}
            disabled={mevcutSayfa === 1}
            aria-label="Önceki sayfa"
          >
            ‹
          </button>
        </li>

        {/* Başlangıçta boşluk varsa */}
        {baslangic > 1 && (
          <li className="pagination__item pagination__item--dots">
            <span className="pagination__dots">...</span>
          </li>
        )}

        {/* Sayfa numaraları */}
        {sayfalar.map(sayfa => (
          <li key={sayfa} className="pagination__item">
            <button
              className={`pagination__link ${
                sayfa === mevcutSayfa ? 'pagination__link--aktif' : ''
              }`}
              onClick={() => onSayfaDegistir(sayfa)}
              aria-label={`Sayfa ${sayfa}`}
              aria-current={sayfa === mevcutSayfa ? 'page' : undefined}
            >
              {sayfa}
            </button>
          </li>
        ))}

        {/* Sonunda boşluk varsa */}
        {bitis < toplamSayfa && (
          <li className="pagination__item pagination__item--dots">
            <span className="pagination__dots">...</span>
          </li>
        )}

        {/* Sonraki sayfa */}
        <li className="pagination__item">
          <button
            className="pagination__link"
            onClick={() => onSayfaDegistir(mevcutSayfa + 1)}
            disabled={mevcutSayfa === toplamSayfa}
            aria-label="Sonraki sayfa"
          >
            ›
          </button>
        </li>

        {/* Son sayfa */}
        <li className="pagination__item">
          <button
            className="pagination__link"
            onClick={() => onSayfaDegistir(toplamSayfa)}
            disabled={mevcutSayfa === toplamSayfa}
            aria-label="Son sayfa"
          >
            »
          </button>
        </li>
      </ul>
    </nav>
  );
};

export default Pagination;
