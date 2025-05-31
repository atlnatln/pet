import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface AramaKutusuProps {
  className?: string;
  placeholder?: string;
}

const AramaKutusu: React.FC<AramaKutusuProps> = ({
  className = '',
  placeholder = 'Hayvan ara...',
}) => {
  const [aramaMetni, setAramaMetni] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (aramaMetni.trim()) {
      navigate(`/hayvanlar?arama=${encodeURIComponent(aramaMetni.trim())}`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={`arama-kutusu ${className}`}>
      <input
        type="text"
        value={aramaMetni}
        onChange={(e) => setAramaMetni(e.target.value)}
        placeholder={placeholder}
        className="arama-kutusu__input"
      />
      <button type="submit" className="arama-kutusu__button">
        🔍
      </button>
    </form>
  );
};

export default AramaKutusu;
