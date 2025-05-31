import React from 'react';

interface Ozellik {
  anahtar: string;
  deger: string | boolean;
  tip?: 'metin' | 'boolean' | 'durum';
}

interface OzellikEtiketleriProps {
  ozellikler: Ozellik[];
  maksimumGoster?: number;
  className?: string;
}

const OzellikEtiketleri: React.FC<OzellikEtiketleriProps> = ({
  ozellikler,
  maksimumGoster,
  className = '',
}) => {
  const gosterilecekOzellikler = maksimumGoster 
    ? ozellikler.slice(0, maksimumGoster)
    : ozellikler;

  const gizlenenSayi = maksimumGoster && ozellikler.length > maksimumGoster
    ? ozellikler.length - maksimumGoster
    : 0;

  const renderEtiket = (ozellik: Ozellik) => {
    const { anahtar, deger, tip = 'metin' } = ozellik;

    if (tip === 'boolean') {
      return deger ? (
        <span className="etiket etiket--basari">{anahtar}</span>
      ) : null;
    }

    if (tip === 'durum') {
      const durumClass = typeof deger === 'string' ? deger.toLowerCase() : '';
      return (
        <span className={`etiket etiket--durum etiket--${durumClass}`}>
          {deger}
        </span>
      );
    }

    return (
      <span className="etiket etiket--varsayilan">
        {anahtar}: {deger}
      </span>
    );
  };

  return (
    <div className={`ozellik-etiketleri ${className}`}>
      {gosterilecekOzellikler.map((ozellik, index) => (
        <React.Fragment key={`${ozellik.anahtar}-${index}`}>
          {renderEtiket(ozellik)}
        </React.Fragment>
      ))}
      
      {gizlenenSayi > 0 && (
        <span className="etiket etiket--gizlenen">
          +{gizlenenSayi} daha
        </span>
      )}
    </div>
  );
};

export default OzellikEtiketleri;
