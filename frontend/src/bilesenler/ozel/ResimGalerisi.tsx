import React, { useState } from 'react';

interface ResimGalerisiProps {
  resimler: string[];
  alt?: string;
  className?: string;
  gosterGosterge?: boolean;
}

const ResimGalerisi: React.FC<ResimGalerisiProps> = ({
  resimler,
  alt = 'Galeri resmi',
  className = '',
  gosterGosterge = true,
}) => {
  const [aktifIndex, setAktifIndex] = useState(0);

  if (!resimler || resimler.length === 0) {
    return (
      <div className={`resim-galerisi resim-galerisi--bos ${className}`}>
        <div className="resim-galerisi__placeholder">
          📷 Resim bulunamadı
        </div>
      </div>
    );
  }

  const sonraki = () => {
    setAktifIndex((prev) => (prev + 1) % resimler.length);
  };

  const onceki = () => {
    setAktifIndex((prev) => (prev - 1 + resimler.length) % resimler.length);
  };

  const resmeGit = (index: number) => {
    setAktifIndex(index);
  };

  return (
    <div className={`resim-galerisi ${className}`}>
      <div className="resim-galerisi__ana">
        <img
          src={resimler[aktifIndex]}
          alt={`${alt} ${aktifIndex + 1}`}
          className="resim-galerisi__resim"
        />
        
        {resimler.length > 1 && (
          <>
            <button
              className="resim-galerisi__nav resim-galerisi__nav--onceki"
              onClick={onceki}
              aria-label="Önceki resim"
            >
              ‹
            </button>
            <button
              className="resim-galerisi__nav resim-galerisi__nav--sonraki"
              onClick={sonraki}
              aria-label="Sonraki resim"
            >
              ›
            </button>
          </>
        )}
      </div>

      {gosterGosterge && resimler.length > 1 && (
        <div className="resim-galerisi__gostergeler">
          {resimler.map((_, index) => (
            <button
              key={index}
              className={`resim-galerisi__gosterge ${
                index === aktifIndex ? 'resim-galerisi__gosterge--aktif' : ''
              }`}
              onClick={() => resmeGit(index)}
              aria-label={`Resim ${index + 1}`}
            />
          ))}
        </div>
      )}

      {resimler.length > 1 && (
        <div className="resim-galerisi__sayac">
          {aktifIndex + 1} / {resimler.length}
        </div>
      )}
    </div>
  );
};

export default ResimGalerisi;
