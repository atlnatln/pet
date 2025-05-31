import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

type Tema = 'acik' | 'koyu';

interface TemaContextType {
  tema: Tema;
  temaDegistir: () => void;
  temaAyarla: (tema: Tema) => void;
}

const TemaContext = createContext<TemaContextType | undefined>(undefined);

interface TemaBaglamiProps {
  children: ReactNode;
}

export const TemaBaglami: React.FC<TemaBaglamiProps> = ({ children }) => {
  const [tema, setTema] = useState<Tema>(() => {
    const kaydedilmisTema = localStorage.getItem('tema') as Tema;
    return kaydedilmisTema || 'acik';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-tema', tema);
    localStorage.setItem('tema', tema);
  }, [tema]);

  const temaDegistir = () => {
    setTema(prev => prev === 'acik' ? 'koyu' : 'acik');
  };

  const temaAyarla = (yeniTema: Tema) => {
    setTema(yeniTema);
  };

  return (
    <TemaContext.Provider value={{
      tema,
      temaDegistir,
      temaAyarla,
    }}>
      {children}
    </TemaContext.Provider>
  );
};

export const useTema = (): TemaContextType => {
  const context = useContext(TemaContext);
  if (!context) {
    throw new Error('useTema, TemaBaglami içinde kullanılmalıdır');
  }
  return context;
};
