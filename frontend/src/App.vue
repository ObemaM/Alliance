<template>
  <div class="page">
    <!-- Aria-label для доступности -->
    <aside class="topbar" aria-label="Контактная информация">
      <div class="topbar__container">
        <div class="topbar__item">☎ {{ phone }}</div>
        <address class="topbar__address">⚐ {{ address }}</address>
      </div>
    </aside>

    <header>
      <div class="header__container">
        <div class="header__left">
          <router-link to="/" class="header__name" aria-label="Перейти на главную">
            <img :src="logo" alt="Лого" class="header__logo" />
            <h1>ALLIANCE</h1>
          </router-link>
          <router-link
            v-if="showCatalogReturnButton"
            to="/"
            class="header__back-link"
            aria-label="Вернуться в каталог"
          >
            <Icon name="ArrowLeft" :size="16" className="header__back-icon" />
            <span>Товары</span>
          </router-link>
        </div>
        <SearchInput v-model="searchTerm" placeholder="Поиск товаров..." class="header__search"/>

        <button class="header__cart" @click="handleCartClick" aria-label="Открыть корзину">
          <Icon name="ShoppingCart" :size="25" />
          <span v-if="cartCount > 0" class="header__cart-count"> {{ cartCount }} </span>
        </button>
      </div>
    </header>

    <main class="content">
      <!-- Показывает роуты в зависимости от страницы -->
      <router-view />
    </main>

    <footer class="bottom">
      <div class="bottom__info">
        <div class="bottom__brand" aria-label="О компании">
          <div class="bottom__headers">
            <h2>ALLIANCE</h2>
          </div>
          <p class="alliance__text">Крепеж и строительные материалы. Доставка по Санкт-Петербургу и Ленинградской области.</p>
        </div>
        <div class="bottom__contacts" aria-label="Контакты">
          <div class="bottom__headers">
            <h3>Контакты</h3>
          </div>
          <p class="alliance__text">Телефон: {{phone }}
            <br>
            Город: {{address }}</p>
        </div>
        <div class="bottom__information" aria-label="Навигация по футеру">
          <div class="bottom__headers">
            <h4>Информация</h4>
          </div>
          <div class="bottom__links">
            <a href="https://www.ozon.ru/seller/alliance-3804007/?miniapp=seller_3804007">OZON</a>
            <router-link to="/delivery">Доставка и оплата</router-link>
          </div>
        </div>
        <div class="bottom__additional" aria-label="Дополнительная информация">
          <div class="bottom__headers">
            <h4>Дополнительно</h4>
          </div>
          <div class="bottom__links">
            <router-link to="/about">О компании</router-link>
          </div>
        </div>
      </div>
      <div class="bottom__copyright">
        <small> 2026 ALLIANCE</small>
      </div>
    </footer>
    <CartDrawer 
      :is-open="isCartOpen"
      :items="cart"
      @close="isCartOpen = false"
      @update-quantity="handleUpdateQuantity"
      @remove-item="handleRemoveItem"
      @checkout="handleCheckout"
      @clear-cart="handleClearCart" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import Icon from './components/Icon.vue';
import SearchInput from './components/SearchInput.vue';
import { useCart } from './composables/useCart'
import CartDrawer from './components/CartDrawer.vue';
import { useSearch } from './composables/useSearch';
import { provide } from 'vue';
import { useRoute } from 'vue-router';
 

type SiteContentItem = {
  id: number;
  key: string;
  value: string;
  description: string | null;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// Реактивные переменные, нужны для обновления данных при загрузке
const phone = ref('');
const address = ref('');
const logo = ref('');
const searchTerm = ref ('')
const { searchResults } = useSearch(searchTerm)
const isCartOpen = ref(false);
const route = useRoute();
const infoPagePaths = new Set(['/about', '/delivery']);
const showCatalogReturnButton = computed(() => infoPagePaths.has(route.path));

provide('searchResults', searchResults)

const { cart, cartCount, loadCart, updateQuantity, removeFromCart, clearCart } = useCart();

const handleCartClick = () => {
  isCartOpen.value = !isCartOpen.value;
};

function handleUpdateQuantity(productId: number, quantity: number) {
  updateQuantity(productId, quantity);
}

function handleRemoveItem(productId: number) {
  removeFromCart(productId);
}

function handleCheckout() {
  console.log('Оформление заказа');
  clearCart();
  isCartOpen.value = false;
}

function handleClearCart() {
  clearCart();
}

async function loadSiteContent() {
  try{
    const response = await fetch(`${API_BASE_URL}/site-content/`);

    // Если сервер ответил ошибкой, то не пытаться обработать данные, а просто выйти
    if (!response.ok) return;

    const data = (await response.json()) as SiteContentItem[];
    const map = new Map<string, string>();

    for (const item of data) {
      map.set(item.key, item.value);
    }

    phone.value = map.get('Телефон') ?? 'Номер телефона недоступен';
    address.value = map.get('Адрес') ?? 'Адрес недоступен';
    logo.value = `${API_BASE_URL}${map.get('Логотип') ?? ' '}`;
  } 
  catch {
    return;
  }
}

onMounted(() => {
  loadSiteContent();
  loadCart();
});

</script>

<style>
  :root {
    --topbar-height: 30px;
    --header-height: 70px;
    font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
    line-height: 1.5;
    font-weight: 400;
    color-scheme: light dark;
  }

  body {
    margin: 0;
    min-width: 320px;
    min-height: 100vh;
  }
  
  .page {
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial;
    background-color: #f5f6f7;
    padding-top: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .topbar{
    font-size: 15px;
    position: sticky;
    top: 0;
    min-height: var(--topbar-height);

    width: 100%; 
    color: white;
    background-color: #1e1e1e;
    z-index: 20;
  }

  .topbar__container {
    font-family: Calibri, sans-serif;
    display: flex;
    justify-content: space-between;
    
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 16px;
    align-items: center;
  }

  .topbar__item, .topbar__address {
    line-height: var(--topbar-height);
  }

  .topbar__item {
    text-align: left;
    text-decoration: none;
    color: inherit;
  }
  
  .topbar__address {
    text-align: right;
    font-style: normal;
  }

  header{
    top: var(--topbar-height);
    position: sticky;
    height: var(--header-height);
 
    width: 100%; 
    color: #eff6ff;
    background-color: white;

    display: flex;
    align-items: center;
    z-index: 10;

    border-bottom: 1px solid #e0e0e0;
  }
 
  .header__name {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    text-decoration: none;
  }

  .header__left {
    display: flex;
    align-items: center;
    gap: 18px;
    min-width: 0;
  }
 
  .header__logo{
    /* Чтобы лого спокойно вписывалось в нужные размеры */
    display: flex; 
    margin-top: 2px;
    width: 50px;
    height: 50px;
    object-fit: contain;
  }

  .header__cart{
    position: relative;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    background: none;
    border: none;
    padding: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: black;
  }

  .header__cart:hover {
    background-color: #f5f6f7;
    color: #1e1e1e;
    border-radius: 15px;
  }

  .header__container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 16px;
    width: 100%;
    gap: 2px;
  }
  
  h1 {
    text-align: left;
    font-size: 22px;
    font-weight: 500;
    color: black;
    letter-spacing: -0.02em;
    -webkit-text-stroke: 0.3px black;
    margin: 0;
    line-height: 1.1;
  }
  
  .header__search {
    background-color: #f5f6f7;
    border-radius: 1px
  }

  .header__back-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    min-height: 36px;
    padding: 0 12px;
    border-radius: 10px;
    background-color: #1e1e1e;
    color: #ffffff;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    transition: background-color 0.2s ease, transform 0.2s ease;
  }

  .header__back-link:hover {
    background-color: #111111;
    transform: translateY(-1px);
  }

  .header__back-icon {
    color: #ffffff;
    flex-shrink: 0;
  }
  
  .bottom{
    margin-top: auto;
    width: 100%;
    min-height: 280px;
    background-color: #1e1e1e;
    padding: 48px 0 24px;
  }
  
  .bottom__container{
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .bottom__brand {
    width: fit-content;
    min-width: 200px;
  }

  .bottom__contacts {
    width: fit-content;
    min-width: 200px;
  }

  .bottom__additional {
    width: fit-content;
    min-width: 200px;
  }

  .bottom__information {
    width: fit-content;
    min-width: 150px;
  }
  
  .bottom__copyright {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid #374151;
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1100px;
    margin-left: auto;
    margin-right: auto;
  }

  .bottom__copyright small {
    color: #9ca3af;
    font-size: 12px;
  }

  .bottom__info {
    display: flex;
    justify-content: space-between;
    gap: 40px;
    max-width: 1100px;
    margin: 0 auto;
  }
  
  .alliance__text {
    margin-top: 4px;
    font-size: 14px;
    line-height: 1.6;
    color: #9ca3af;
  }

  .bottom__headers {
    margin-bottom: 8px;
  }
  
  .bottom__headers h2,
  .bottom__headers h3,
  .bottom__headers h4 {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
    color: #f9fafb;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .bottom__links {
    display: flex;
    flex-direction: column;
    gap: 1.6px;
  }

  .bottom__links a {
    color: #9ca3af;
    font-size: 14px;
    text-decoration: none;
    transition: color 0.15s ease;
    line-height: 1.5;
  }

  .bottom__links a:hover {
    color: #ffffff;
  }

  .bottom__icon{
    padding-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    width: 100px;
    height: 100px;
  }

  .header__cart-count {
    position: absolute;
    top: 2px;
    right: 2px;
    background: #bd0707;
    color: white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  @media (max-width: 740px) {
    :root{
      --topbar-height: 30px;
      --header-height: 110px;
    }
    
    .topbar {
      font-size: 15px;
      min-height: var(--topbar-height);
    }

    .topbar__container {
      /* Перенос на новую строку для мобильных */
      flex-wrap: wrap;

      gap: 0;
      justify-content: center;
    }

    .topbar__address {
      /* Убрано из отображения */
      display: none;
    }

    .header{
      top: var(--topbar-height);
      height: var(--header-height);
    }

    .header__container {
      flex-wrap: wrap;
    }

    .header__left {
      width: 100%;
      justify-content: space-between;
    }
    
    .header__search{
      margin-bottom: 10px;
      min-width: 150px; 
      margin-left: auto;
      margin-right: auto;
      flex-basis: 100%;
      order: 3;
      width: 100%;
    }

    .header__cart{
      order: 2;
      flex-basis: auto;
    }
  }
</style>
