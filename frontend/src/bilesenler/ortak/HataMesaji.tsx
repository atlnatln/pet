import React from 'react';

interface HataMesajiProps {
  mesaj?: string;
  tip?: 'genel' | 'alan' | 'sayfa';
  gosterilsin?: boolean;
  onTekrarDene?: () => void;
  className?: string;
}

const HataMesaji: React.FC<HataMesajiProps> = ({
  mesaj = 'Bir hata oluştu. Lütfen tekrar deneyin.',
  tip = 'genel',
  gosterilsin = true,
  onTekrarDene,
  className = '',
}) => {
  if (!gosterilsin) return null;

  return (
    <div className={`hata-mesaji hata-mesaji--${tip} ${className}`}>
      <div className="hata-mesaji__icerik">
        <span className="hata-mesaji__ikon">⚠️</span>
        <div className="hata-mesaji__detay">
          <p className="hata-mesaji__metin">{mesaj}</p>
          {onTekrarDene && (
            <button
              className="hata-mesaji__tekrar-dene"
              onClick={onTekrarDene}
            >
              Tekrar Dene
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default HataMesaji;
