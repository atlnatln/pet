import React from 'react';
import { useForm } from '../../kancalar/useForm';
import { useAuth } from '../../baglamlar/AuthContext';
import { useBildirim } from '../../baglamlar/BildirimBaglami';
import Dugme from '../ortak/Dugme';

interface GirisFormData {
  email: string;
  sifre: string;
}

const GirisFormu: React.FC = () => {
  const { girisYap } = useAuth();
  const { hataBildirimi } = useBildirim();

  const { degerler, degistir, gonder, alanHatasi, yukleniyor } = useForm<GirisFormData>({
    baslangicDegerleri: {
      email: '',
      sifre: '',
    },
    dogrulama: (values) => {
      const errors: { [key: string]: string } = {};
      
      if (!values.email) {
        errors.email = 'E-posta gerekli';
      } else if (!/\S+@\S+\.\S+/.test(values.email)) {
        errors.email = 'Geçerli bir e-posta adresi girin';
      }
      
      if (!values.sifre) {
        errors.sifre = 'Şifre gerekli';
      }
      
      return errors;
    },
    onSubmit: async (values) => {
      try {
        await girisYap(values.email, values.sifre);
      } catch (error) {
        hataBildirimi('Giriş yapılamadı. E-posta ve şifrenizi kontrol edin.');
      }
    },
  });

  return (
    <form onSubmit={gonder} className="giris-formu">
      {/* Form implementation will be completed later */}
      <div className="form-group">
        <label htmlFor="email">E-posta</label>
        <input
          id="email"
          type="email"
          value={degerler.email}
          onChange={(e) => degistir('email', e.target.value)}
        />
        {alanHatasi('email') && <span className="error">{alanHatasi('email')}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="sifre">Şifre</label>
        <input
          id="sifre"
          type="password"
          value={degerler.sifre}
          onChange={(e) => degistir('sifre', e.target.value)}
        />
        {alanHatasi('sifre') && <span className="error">{alanHatasi('sifre')}</span>}
      </div>

      <Dugme type="submit" yukleniyor={yukleniyor}>
        Giriş Yap
      </Dugme>
    </form>
  );
};

export default GirisFormu;
