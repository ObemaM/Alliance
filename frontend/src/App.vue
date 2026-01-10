<script setup lang="ts">
  // Импортируем наш новый компонент DataManager
  const year = new Date().getFullYear();
</script>

<template>
  <div class="page">
    <div class="topbar">
      <div class="topbar__inner">
        <div class="topbar__group">
          <a class="topbar__item" href="tel:+79991234567" aria-label="Телефон для связи">
            <span class="topbar__icon">☎</span>
            <span>+7 (999) 123-45-67</span>
          </a>
          <div class="topbar__item topbar__item--address" aria-label="Адрес офиса">
            <span>г. Санкт-Петербург, Красногвардейский район</span>
          </div>
        </div>
      </div>
    </div>
    <header class="header">
      <div class="header__inner">
        <div class="brand">Alliance</div>
        <form class="header__search" role="search">
          <input
            class="header__input"
            type="search"
            placeholder="Поиск товаров (например, саморезы, цемент)..."
            aria-label="Поиск товаров"
          />
          <button class="header__search-btn" type="submit">Найти</button>
        </form>
        <div class="header__actions">
          <a class="header__action" href="#favorites" aria-label="Избранное">★</a>
          <a class="header__action" href="#cart" aria-label="Корзина">🛒</a>
          <a class="cta" href="#contacts">Рассчитать смету</a>
        </div>
      </div>
    </header>

    <main>
      <section class="hero">
        <div class="container hero__inner">
          <div class="hero__content">
            <h1 class="hero__title">Строительство и ремонт под ключ</h1>
            <p class="hero__subtitle">
              Частные дома, коммерческие объекты, отделка и инженерные работы.
              Берём ответственность за сроки, качество и прозрачную смету.
            </p>
            <div class="hero__actions">
              <a class="button button--primary" href="#contacts">Получить консультацию</a>
              <a class="button button--ghost" href="#projects">Посмотреть работы</a>
            </div>
          </div>
          <div class="hero__card" aria-label="Преимущества">
            <div class="kpi">
              <div class="kpi__value">10+ лет</div>
              <div class="kpi__label">на рынке</div>
            </div>
            <div class="kpi">
              <div class="kpi__value">Договор</div>
              <div class="kpi__label">и гарантия</div>
            </div>
            <div class="kpi">
              <div class="kpi__value">Смета</div>
              <div class="kpi__label">без скрытых работ</div>
            </div>
          </div>
        </div>
      </section>

      <section id="services" class="section">
        <div class="container">
          <h2 class="section__title">Услуги</h2>
          <div class="grid">
            <article class="card">
              <h3 class="card__title">Строительство домов</h3>
              <p class="card__text">Фундамент, коробка, кровля, фасад — полный цикл.</p>
            </article>
            <article class="card">
              <h3 class="card__title">Ремонт и отделка</h3>
              <p class="card__text">Квартира, офис, магазин — аккуратно и по технологии.</p>
            </article>
            <article class="card">
              <h3 class="card__title">Инженерные системы</h3>
              <p class="card__text">Электрика, сантехника, отопление, вентиляция.</p>
            </article>
          </div>
        </div>
      </section>

      <section id="projects" class="section section--alt">
        <div class="container">
          <h2 class="section__title">Примеры работ</h2>
          <div class="grid">
            <article class="card">
              <h3 class="card__title">Коттедж 180 м²</h3>
              <p class="card__text">Фундамент + коробка + кровля. Срок: 4 месяца.</p>
            </article>
            <article class="card">
              <h3 class="card__title">Офис 320 м²</h3>
              <p class="card__text">Демонтаж, отделка, инженерия. Срок: 6 недель.</p>
            </article>
            <article class="card">
              <h3 class="card__title">Фасад и утепление</h3>
              <p class="card__text">Теплый контур, декоративная штукатурка.</p>
            </article>
          </div>
        </div>
      </section>

      <section id="about" class="section">
        <div class="container">
          <h2 class="section__title">О компании</h2>
          <p class="text">
            Работаем по договору, фиксируем этапы и стоимость, ведём фото-отчёт.
            Подбираем материалы под бюджет и задачу, соблюдаем СНиП и техкарты.
          </p>
        </div>
      </section>

      <section id="contacts" class="section section--alt">
        <div class="container">
          <h2 class="section__title">Контакты</h2>
          <div class="contacts">
            <div class="contacts__block">
              <div class="contacts__label">Телефон</div>
              <a class="contacts__value" href="tel:+70000000000">+7 (000) 000-00-00</a>
            </div>
            <div class="contacts__block">
              <div class="contacts__label">Email</div>
              <a class="contacts__value" href="mailto:info@example.com">info@example.com</a>
            </div>
            <div class="contacts__block">
              <div class="contacts__label">Город</div>
              <div class="contacts__value">Ваш город</div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="container footer__inner">
        <div class="footer__copy">© {{ year }} Alliance</div>
        <div class="footer__note">Строительство • Ремонт • Инженерные работы</div>
      </div>
    </footer>
  </div>
</template>

<style>
/* Глобальные стили для всего приложения */
body {
  margin: 0;
  padding: 0;
  background-color: #f4f4f9;
}

:root {
  --topbar-height: 36px;
  --header-height: 80px;
}

.page {
  color: #111827;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  padding-top: calc(var(--topbar-height) + var(--header-height));
}

.topbar {
  background: #1e3a8a;
  color: #f5f7ff;
  font-size: 14px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 20;
}

.topbar__inner {
  min-height: 36px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 16px;
}

.topbar__item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: inherit;
  text-decoration: none;
}

.topbar__item--address {
  margin-left: 20px;
  text-align: right;
}

.topbar__item:hover {
  opacity: 0.85;
}

.topbar__icon {
  font-size: 16px;
  line-height: 1;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 16px;
}

.header {
  position: fixed;
  top: var(--topbar-height);
  left: 0;
  width: 100%;
  z-index: 10;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(17, 24, 39, 0.08);
}

.header__inner {
  height: var(--header-height);
  display: flex;
  align-items: center;
  gap: 16px;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 16px;
  width: 100%;
}

.brand {
  font-weight: 800;
  letter-spacing: 0.4px;
}

.nav {
  display: flex;
  gap: 14px;
  margin-left: 12px;
  flex: 1;
  flex-wrap: wrap;
}

.nav__link {
  color: #111827;
  text-decoration: none;
  font-weight: 600;
  opacity: 0.85;
}

.nav__link:hover {
  opacity: 1;
}

.cta {
  text-decoration: none;
  color: #ffffff;
  background: #111827;
  padding: 10px 14px;
  border-radius: 10px;
  font-weight: 700;
}

.hero {
  padding: 56px 0;
}

.hero__inner {
  display: grid;
  grid-template-columns: 1.4fr 0.8fr;
  gap: 18px;
  align-items: start;
}

.hero__title {
  margin: 0;
  font-size: 42px;
  line-height: 1.1;
}

.hero__subtitle {
  margin: 14px 0 0;
  color: rgba(17, 24, 39, 0.8);
  font-size: 16px;
  line-height: 1.6;
}

.hero__actions {
  margin-top: 18px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 16px;
  border-radius: 12px;
  font-weight: 700;
  text-decoration: none;
  border: 1px solid transparent;
}

.button--primary {
  background: #2563eb;
  color: #fff;
}

.button--ghost {
  background: transparent;
  color: #111827;
  border-color: rgba(17, 24, 39, 0.18);
}

.hero__card {
  background: #ffffff;
  border: 1px solid rgba(17, 24, 39, 0.08);
  border-radius: 16px;
  padding: 16px;
  display: grid;
  gap: 14px;
  box-shadow: 0 10px 30px rgba(17, 24, 39, 0.08);
}

.kpi__value {
  font-weight: 800;
  font-size: 18px;
}

.kpi__label {
  color: rgba(17, 24, 39, 0.7);
  margin-top: 2px;
}

.section {
  padding: 40px 0;
}

.section--alt {
  background: rgba(17, 24, 39, 0.04);
}

.section__title {
  margin: 0 0 16px;
  font-size: 24px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.card {
  background: #ffffff;
  border: 1px solid rgba(17, 24, 39, 0.08);
  border-radius: 14px;
  padding: 16px;
}

.card__title {
  margin: 0;
  font-size: 16px;
}

.card__text {
  margin: 8px 0 0;
  color: rgba(17, 24, 39, 0.75);
  line-height: 1.6;
}

.text {
  margin: 0;
  color: rgba(17, 24, 39, 0.75);
  line-height: 1.7;
  max-width: 800px;
}

.contacts {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.contacts__block {
  background: #ffffff;
  border: 1px solid rgba(17, 24, 39, 0.08);
  border-radius: 14px;
  padding: 16px;
}

.contacts__label {
  color: rgba(17, 24, 39, 0.65);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.contacts__value {
  display: inline-block;
  margin-top: 6px;
  color: #111827;
  font-weight: 700;
  text-decoration: none;
}

.footer {
  padding: 22px 0;
  border-top: 1px solid rgba(17, 24, 39, 0.08);
  background: #ffffff;
}

.footer__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.footer__copy {
  font-weight: 700;
}

.footer__note {
  color: rgba(17, 24, 39, 0.6);
}

@media (max-width: 900px) {
  .hero__inner {
    grid-template-columns: 1fr;
  }

  .grid {
    grid-template-columns: 1fr;
  }

  .contacts {
    grid-template-columns: 1fr;
  }
}
</style>
