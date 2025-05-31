import React from 'react';

interface YuklemeDurumuProps {
  tip?: 'spinner' | 'dots' | 'bars' | 'pulse';
  boyut?: 'kucuk' | 'orta' | 'buyuk';
  mesaj?: string;
  merkezde?: boolean;
  className?: string;
}

const YuklemeDurumu: React.FC<YuklemeDurumuProps> = ({
  tip = 'spinner',
  boyut = 'orta',
  mesaj,
  merkezde = false,
  className = '',
}) => {
  const renderYukleme = () => {
    switch (tip) {
      case 'dots':
        return (
          <div className="yukleme-dots">
            <div className="yukleme-dots__dot"></div>
            <div className="yukleme-dots__dot"></div>
            <div className="yukleme-dots__dot"></div>
          </div>
        );
      
      case 'bars':
        return (
          <div className="yukleme-bars">
            <div className="yukleme-bars__bar"></div>
            <div className="yukleme-bars__bar"></div>
            <div className="yukleme-bars__bar"></div>
            <div className="yukleme-bars__bar"></div>
          </div>
        );
      
      case 'pulse':
        return <div className="yukleme-pulse"></div>;
      
      default:
        return <div className="yukleme-spinner"></div>;
    }
  };

  return (
    <div className={`
      yukleme-durumu 
      yukleme-durumu--${boyut} 
      ${merkezde ? 'yukleme-durumu--merkezde' : ''} 
      ${className}
    `}>
      <div className="yukleme-durumu__icerik">
        {renderYukleme()}
        {mesaj && (
          <p className="yukleme-durumu__mesaj">{mesaj}</p>
        )}
      </div>
    </div>
  );
};

export default YuklemeDurumu;
