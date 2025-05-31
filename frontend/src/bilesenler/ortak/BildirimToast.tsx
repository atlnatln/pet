import React from 'react';
import { useBildirim } from '../../baglamlar/BildirimBaglami';

const BildirimToast: React.FC = () => {
  const { bildirimler, bildirimKaldir } = useBildirim();

  if (bildirimler.length === 0) return null;

  return (
    <div className="bildirim-toast-container">
      {bildirimler.map(bildirim => (
        <div
          key={bildirim.id}
          className={`bildirim-toast bildirim-toast--${bildirim.tip}`}
          onClick={() => bildirimKaldir(bildirim.id)}
        >
          <div className="bildirim-toast__icerik">
            <span className="bildirim-toast__mesaj">{bildirim.mesaj}</span>
            <button
              className="bildirim-toast__kapat"
              onClick={(e) => {
                e.stopPropagation();
                bildirimKaldir(bildirim.id);
              }}
              aria-label="Bildirimi kapat"
            >
              ×
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default BildirimToast;
