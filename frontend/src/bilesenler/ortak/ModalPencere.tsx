import React, { useEffect, useRef, ReactNode } from 'react';
import Dugme from './Dugme';

interface ModalPencereProps {
  acik: boolean;
  onKapat: () => void;
  baslik?: string;
  children: ReactNode;
  boyut?: 'kucuk' | 'orta' | 'buyuk' | 'tam';
  kapatilabilir?: boolean;
  onOnay?: () => void;
  onIptal?: () => void;
  onayMetni?: string;
  iptalMetni?: string;
  yukleniyor?: boolean;
  className?: string;
}

const ModalPencere: React.FC<ModalPencereProps> = ({
  acik,
  onKapat,
  baslik,
  children,
  boyut = 'orta',
  kapatilabilir = true,
  onOnay,
  onIptal,
  onayMetni = 'Onayla',
  iptalMetni = 'İptal',
  yukleniyor = false,
  className = '',
}) => {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && kapatilabilir) {
        onKapat();
      }
    };

    if (acik) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [acik, kapatilabilir, onKapat]);

  useEffect(() => {
    if (acik && modalRef.current) {
      modalRef.current.focus();
    }
  }, [acik]);

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget && kapatilabilir) {
      onKapat();
    }
  };

  if (!acik) return null;

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div
        ref={modalRef}
        className={`modal modal--${boyut} ${className}`}
        tabIndex={-1}
        role="dialog"
        aria-modal="true"
        aria-labelledby={baslik ? "modal-baslik" : undefined}
      >
        {baslik && (
          <div className="modal__header">
            <h2 id="modal-baslik" className="modal__baslik">
              {baslik}
            </h2>
            {kapatilabilir && (
              <button
                className="modal__kapat"
                onClick={onKapat}
                aria-label="Modalı kapat"
              >
                ×
              </button>
            )}
          </div>
        )}

        <div className="modal__icerik">
          {children}
        </div>

        {(onOnay || onIptal) && (
          <div className="modal__footer">
            {onIptal && (
              <Dugme
                tip="ikincil"
                onClick={onIptal}
                devre_disi={yukleniyor}
              >
                {iptalMetni}
              </Dugme>
            )}
            {onOnay && (
              <Dugme
                tip="birincil"
                onClick={onOnay}
                yukleniyor={yukleniyor}
                devre_disi={yukleniyor}
              >
                {onayMetni}
              </Dugme>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ModalPencere;
