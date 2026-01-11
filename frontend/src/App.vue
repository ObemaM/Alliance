<template>
  <div class="page">
    <div class="topbar">
      <div class="topbar__container">
        <div class="topbar__item">{{ phone }}</div>
        <div class="topbar__address">{{ address }}</div>
      </div>
    </div>

    <div class = "header">
      <div class="header__container">
        <img v-if="logo" :src="logo" alt="Логотип" class="header__logo" />
        <div v-else class="header__logo"> - </div>
        <h1>ALLIANCE.</h1>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';

type SiteContentItem = {
  id: number;
  key: string;
  value: string;
  description: string | null;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Реактивные переменные, нужны для обновления данных при загрузке
const phone = ref('Номер телефона недоступен');
const address = ref('Адрес недоступен');
const logo = ref(' ')

async function loadSiteContent() {
  try{
    const response = await fetch(`${API_BASE_URL}/site-content/`);

    // Если сервер ответил ошибкой, то не пытаться обработать данные, а просто выйти
    if (response.ok == false) return;

    const data = (await response.json()) as SiteContentItem[];
    const map = new Map<string, string>();

    for (const item of data) {
      map.set(item.key, item.value);
    }

    phone.value = map.get('Телефон') ?? 'Номер телефона недоступен';
    address.value = map.get('Адрес') ?? 'Адрес недоступен'; // 𖠿
    logo.value = `${API_BASE_URL}${map.get('Логотип') ?? ' '}`;
  } 
  catch {
    return;
  }
}

onMounted(loadSiteContent);
</script>

<style>
  :root {
    --topbar-height: 32px;
    --header-height: 72px;
  }
  
  .page {
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial;
    background-color: #f5f6f7;
    padding-top: 0;
    min-height: 100vh;
  }

  .topbar{
    font-size: 13px;
    position: sticky;
    top: 0;
    min-height: var(--topbar-height);

    width: 100%; 
    color: black;
    background-color: #eaae52;
    z-index: 20;
  }

  .topbar__container {
    font-family: 'Futura', monospace;
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
  }
  
  .topbar__address {
    text-align: right;
  }

  .header{
    top: var(--topbar-height);
    position: sticky;
    height: var(--header-height);
 
    width: 100%; 
    color: #eff6ff;
    background-color: white;

    display: flex;
    align-items: center;
    z-index: 10;
  }
 
  .header__container {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 16px;
    width: 100%;
    gap: 2px;
  }
 
  .header__logo{
    /* Чтобы лого спокойно вписывалось в нужные размеры */
    display: block; 
    margin-top: 2px;
    width: 50px;
    height: 50px;
    object-fit: contain;
  }

  h1 {
    text-align: left;
    font-size: 22px;
    font-style: italic;
    font-weight: 500;
    color: black;
    letter-spacing: -0.02em;
    -webkit-text-stroke: 0.3px black;
    margin: 0;
  }
  
  @media (max-width: 740px) {
    :root{
      --topbar-height: 30px;
      --header-height: 55px;
    }
    
    .topbar {
      font-size: 13px;
      min-height: var(--topbar-height);
    }

    .topbar__container {
      /* Перенос на новую строку для мобильных */
      flex-wrap: wrap;

      gap: 0;
      justify-content: center;
    }

    .topbar__address {
      display: none;
      text-align: center;
      flex-basis: 100%;
      margin-top: -12px;
    }

    .header{
      top: var(--topbar-height);
      height: var(--header-height);
    }
  }

</style>