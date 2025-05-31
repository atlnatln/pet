import React from 'react';

interface DugmeProps {
  children: React.ReactNode;
  onClick?: () => void;
  tip?: 'birincil' | 'ikincil' | 'tehlike' | 'basari';
  boyut?: 'kucuk' | 'orta' | 'buyuk';
  devre_disi?: boolean;
  yukleniyor?: boolean;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

const Dugme: React.FC<DugmeProps> = ({
  children,
  onClick,
  tip = 'birincil',
  boyut = 'orta',
  devre_disi = false,
  yukleniyor = false,
  className = '',
  type = 'button'
}) => {
  const dugmeClassName = `dugme dugme--${tip} dugme--${boyut} ${className}`;

  return (
    <button
      type={type}
      className={dugmeClassName}
      onClick={onClick}
      disabled={devre_disi || yukleniyor}
    >
      {yukleniyor ? 'Yükleniyor...' : children}
    </button>
  );
};

export default Dugme;
