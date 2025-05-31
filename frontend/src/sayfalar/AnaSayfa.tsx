import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Hayvan, Blog } from '../types';
import { hayvanService } from '../hizmetler/hayvanService';
import { blogService } from '../hizmetler/blogService';
import HayvanKarti from '../bilesenler/kartlar/HayvanKarti';
import YuklemeDurumu from '../bilesenler/ortak/YuklemeDurumu';
import HataMesaji from '../bilesenler/ortak/HataMesaji';

const AnaSayfa: React.FC = () => {
  const [hayvanlar, setHayvanlar] = useState<Hayvan[]>([]);
  const [bloglar, setBloglar] = useState<Blog[]>([]);
  const [yukleniyor, setYukleniyor] = useState(true);
  const [hata, setHata] = useState<string | null>(null);

  useEffect(() => {
    const verileriYukle = async () => {
      try {
        setYukleniyor(true);
        const [hayvanlarResponse, bloglarResponse] = await Promise.all([
          hayvanService.rastgeleHayvanlar(6),
          blogService.populerBloglar(),
        ]);
        
        setHayvanlar(hayvanlarResponse);
        setBloglar(bloglarResponse.slice(0, 3));
      } catch (error) {
        setHata('Veriler yüklenirken bir hata oluştu');
      } finally {
        setYukleniyor(false);
      }
    };

    verileriYukle();
  }, []);

  if (yukleniyor) {
    return <YuklemeDurumu merkezde mesaj="Ana sayfa yükleniyor..." />;
  }

  if (hata) {
    return <HataMesaji mesaj={hata} tip="sayfa" />;
  }

  return (
    <div className="ana-sayfa">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero__icerik">
          <h1 className="hero__baslik">Evcil Dostunuzu Bulun</h1>
          <p className="hero__aciklama">
            Binlerce hayvan sahiplendirilmeyi bekliyor. Siz de yeni dostunuzu bulun!
          </p>
          <Link to="/hayvanlar" className="hero__cta">
            Hayvanları Keşfet
          </Link>
        </div>
      </section>

      {/* Öne Çıkan Hayvanlar */}
      <section className="ozellikli-hayvanlar">
        <div className="container">
          <h2 className="section-title">Öne Çıkan Hayvanlar</h2>
          <div className="hayvan-grid">
            {hayvanlar.map((hayvan) => (
              <HayvanKarti key={hayvan.id} hayvan={hayvan} />
            ))}
          </div>
          <div className="section-footer">
            <Link to="/hayvanlar" className="btn btn--secondary">
              Tümünü Gör
            </Link>
          </div>
        </div>
      </section>

      {/* Son Blog Yazıları */}
      <section className="son-bloglar">
        <div className="container">
          <h2 className="section-title">Son Blog Yazıları</h2>
          <div className="blog-grid">
            {bloglar.map((blog) => (
              <article key={blog.id} className="blog-kart">
                <Link to={`/blog/${blog.id}`}>
                  <h3>{blog.baslik}</h3>
                  <p>{blog.ozet}</p>
                </Link>
              </article>
            ))}
          </div>
          <div className="section-footer">
            <Link to="/blog" className="btn btn--secondary">
              Tüm Blog Yazıları
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AnaSayfa;
