import React from 'react';
import { Link } from 'react-router-dom';
import './SiteFooter.css';

const SiteFooter: React.FC = () => {
  return (
    <footer className="site-footer">
      <div className="site-footer__inner">
        <div className="site-footer__cols">
          <section className="site-footer__col" aria-labelledby="site-footer-about">
            <h2 id="site-footer-about" className="site-footer__heading">
              О проекте
            </h2>
            <Link to="/" className="site-footer__brand">
              AlgoPlatform
            </Link>
            <p className="site-footer__text">
              Каталог алгоритмов для разработчиков: публикация решений, покупка кода и прозрачная
              модерация материалов перед появлением в поиске.
            </p>
          </section>

          <section className="site-footer__col" aria-labelledby="site-footer-catalog">
            <h2 id="site-footer-catalog" className="site-footer__heading">
              Каталог
            </h2>
            <p className="site-footer__highlight">
              Показываются только проверенные и одобренные алгоритмы
            </p>
            <p className="site-footer__text site-footer__text--muted">
              Каждая публикация проходит проверку модераторов: соответствие описанию, работоспособность
              и соблюдение правил площадки.
            </p>
          </section>

          <section className="site-footer__col" aria-labelledby="site-footer-contact">
            <h2 id="site-footer-contact" className="site-footer__heading">
              Связь
            </h2>
            <p className="site-footer__text">
              Вопросы по размещению, оплате и модерации можно обсудить через раздел профиля после
              входа в аккаунт.
            </p>
          </section>
        </div>

        <div className="site-footer__bar">
          <span>© {new Date().getFullYear()} AlgoPlatform</span>
          <span className="site-footer__bar-sep" aria-hidden>
            ·
          </span>
          <span>Платформа алгоритмов</span>
        </div>
      </div>
    </footer>
  );
};

export default SiteFooter;
