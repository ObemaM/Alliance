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
        <div class="header__name">
          <img :src="logo" alt="Лого" class="header__logo" />
          <h1>ALLIANCE</h1>
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
      <div class="bottom__container">
        <div class="bottom__brand">
          <div class="bottom__headers">
            <h2>ALLIANCE</h2> 
          </div>
          <p class="alliance__text">Ваш надежный партнер в строительстве и ремонте.</p>
        </div>
        <div class="bottom__contacts">
          <div class="bottom__headers">
            <h3>Контакты</h3>
          </div>
          <p class="alliance__text">Телефон: {{phone }}
            <br>
            Город: {{address }}</p>
        </div>
        <div class="bottom_information" aria-label="Навигация по футеру">
          <div class="bottom__headers">
            <h4>Информация</h4>
          </div>
          <div class="bottom__links">
            <a href="https://www.ozon.ru/seller/alliance-3804007/?miniapp=seller_3804007">OZON</a>
            <br>
            <a href="">Доставка и оплата</a>
          </div>
        </div>
        <img :src="`${API_BASE_URL}/uploads/images/icon.svg`" alt="" class="bottom__icon" />
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
import { onMounted, ref } from 'vue';
import Icon from './components/Icon.vue';
import SearchInput from './components/SearchInput.vue';
import { useCart } from './composables/useCart'
import CartDrawer from './components/CartDrawer.vue';
import { useSearch } from './composables/useSearch';
import { provide } from 'vue';
 

type SiteContentItem = {
  id: number;
  key: string;
  value: string;
  description: string | null;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Реактивные переменные, нужны для обновления данных при загрузке
const phone = ref('');
const address = ref('');
const logo = ref('');
const searchTerm = ref ('')
const { searchResults } = useSearch(searchTerm)
const isCartOpen = ref(false);

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
  
  .bottom{
    margin-top: auto;
    width: 100%;
    min-height: 250px;
    bottom: auto;
    background-color: #1e1e1e;
  }
  
  .bottom__container{
    /* отступ сверху */
    padding-top: 20px;
    
    padding-left: 20px;
    padding-right: 20px;
    
    /* классический способ центрирования блочного элемента */
    margin: 0 auto;
    
    display: flex;
    align-items: center;
    max-width: 1100px;
  }
  
  .bottom__brand {
    min-height: 160px;
    margin-right: 50px;
  }

  .bottom__contacts {
    min-height: 160px;
    margin-right: 50px;
  }
  
  .bottom_information {
    min-height: 160px;
  }
  
  .bottom__copyright small {
    padding-top: 20px;
    border-top: 1px solid #374151;
    display: flex;
    margin: 0 auto;
    color: #9ca3af;
    justify-content: center;
    max-width: 1100px;
    font-size: 12px;
  }

  .bottom__info {
    display: flex;
    justify-content: space-between;
    margin: 0 auto;
    max-width: 1100px;
    gap: 20px;
  }
  
  .alliance__text {
    margin-top: 15px;
    max-width: 385px;
    font-size: 15px;
    color: #9ca3af;
  }

  .bottom__headers {
    min-height: 40px;
    display: flex;
    align-items: center;
  }
  
  .bottom__headers h3 {
    margin: 0;
  }
  
  .bottom__headers h4 {
    margin: 0;
  }
  
  .bottom__headers h2 {
    margin: 0;
  }

  .bottom__links {
    margin-top: 15px;
  }

  .bottom__links a {
    color: #9ca3af;
  }

  .bottom__links a:hover {
    text-decoration: underline;
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