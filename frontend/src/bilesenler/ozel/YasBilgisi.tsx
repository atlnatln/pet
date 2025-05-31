import React from 'react';
import { formatlar } from '../../yardimcilar/formatlar';

interface YasBilgisiProps {
  yas: number;
  dogumTarihi?: string;
  format?: 'kisa' | 'detayli';
  className?: string;
}

const YasBilgisi: React.FC<YasBilgisiProps> = ({
  yas,
  dogumTarihi,
  format = 'kisa',
  className = '',
}) => {
  const yasMetni = formatlar.yas(yas);

  if (format === 'kisa') {
    return (
      <span className={`yas-bilgisi yas-bilgisi--kisa ${className}`}>
        {yasMetni}
      </span>
    );
  }

  return (
    <div className={`yas-bilgisi yas-bilgisi--detayli ${className}`}>
      <span className="yas-bilgisi__yas">{yasMetni}</span>
      {dogumTarihi && (
        <span className="yas-bilgisi__tarih">
          Doğum: {new Date(dogumTarihi).toLocaleDateString('tr-TR')}
        </span>
      )}
    </div>
  );
};

export default YasBilgisi;
