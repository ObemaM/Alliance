<template>
  <div class="page">
    <div class="topbar">
      <div class="topbar__inner">
        <div class="topbar__left">
          <a class="topbar__item" href="tel:+79991234567">☎ +7 (999) 123-45-67</a>
          <div class="topbar__item">г. Санкт-Петербург, Красногвардейский район</div>
        </div>
      </div>
    </div>

    <header class="header">
      <div class="header__inner">
        <div class="brand">ALLIANCE<span class="brand__dot">.</span></div>
        <form class="search" role="search">
          <input class="search__input" type="search" placeholder="Поиск товаров..." />
          <button class="search__btn" type="submit">Найти</button>
        </form>
        <div class="header__actions">
          <a class="icon-btn" href="#cart" aria-label="Корзина">🛒</a>
        </div>
      </div>
    </header>

    <main class="main">
      <section class="hero">
        <div class="container">
          <h1 class="hero__title">Строительный магазин и материалы</h1>
          <p class="hero__subtitle">Крепёж, инструмент и расходники. Подбор и доставка.</p>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <h2 class="section__title">Каталог</h2>
          <p class="section__text">Дальше здесь можно вывести товары карточками.</p>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="container footer__inner">
        <div class="footer__copy"> {{ year }} Alliance</div>
        <div class="footer__note">Крепёж • Инструмент • Стройматериалы</div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const year = new Date().getFullYear();
</script>

<style>
body {
  margin: 0;
  background: #f4f4f9;
}

:root {
  --topbar-height: 36px;
  --header-height: 72px;
  --max-width: 1100px;
}

.page {
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  color: #111827;
  padding-top: calc(var(--topbar-height) + var(--header-height));
}

.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 16px;
}

.topbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--topbar-height);
  background: #1e3a8a;
  color: #f5f7ff;
  z-index: 20;
}

.topbar__inner {
  height: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.topbar__left {
  display: flex;
  gap: 18px;
  align-items: center;
  font-size: 13px;
  flex-wrap: wrap;
}

.topbar__item {
  color: inherit;
  text-decoration: none;
  opacity: 0.95;
}

.header {
  position: fixed;
  top: var(--topbar-height);
  left: 0;
  width: 100%;
  height: var(--header-height);
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(17, 24, 39, 0.08);
  z-index: 10;
}

.header__inner {
  height: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand {
  font-weight: 900;
  color: #1d4ed8;
  letter-spacing: -0.02em;
}

.brand__dot {
  color: #f97316;
}

.search {
  flex: 1;
  display: flex;
  gap: 10px;
  max-width: 620px;
}

.search__input {
  flex: 1;
  height: 40px;
  border: 2px solid rgba(17, 24, 39, 0.12);
  border-radius: 10px;
  padding: 0 12px;
  background: white;
}

.search__btn {
  height: 40px;
  padding: 0 14px;
  border: 0;
  border-radius: 10px;
  background: #111827;
  color: white;
  font-weight: 700;
  cursor: pointer;
}

.header__actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  text-decoration: none;
  color: #111827;
  background: rgba(17, 24, 39, 0.06);
}

.main {
  min-height: calc(100vh - (var(--topbar-height) + var(--header-height)));
}

.hero {
  padding: 36px 0;
}

.hero__title {
  margin: 0;
  font-size: 36px;
}

.hero__subtitle {
  margin: 10px 0 0;
  color: rgba(17, 24, 39, 0.7);
}

.section {
  padding: 32px 0;
}

.section__title {
  margin: 0 0 12px;
  font-size: 22px;
}

.section__text {
  margin: 0;
  color: rgba(17, 24, 39, 0.7);
}

.footer {
  padding: 18px 0;
  background: white;
  border-top: 1px solid rgba(17, 24, 39, 0.08);
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

@media (max-width: 700px) {
  :root {
    --header-height: 92px;
  }

  .search {
    max-width: none;
  }
}
</style>