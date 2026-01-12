<template>
  <div class="home">
    <h1 class="home__title">Товары</h1>
    
    <div v-if="loading" class="home__loading">
      Загрузка товаров...
    </div>
    
    <div v-else-if="error" class="home__error">
      {{ error }}
    </div>
    
    <div v-else class="home__products">
      <div v-for="product in products" :key="product.id" class="home__product">
        <h3 class="product__name">{{ product.name }}</h3>
        <p class="product__price">{{ product.price }} ₽</p>
        <p v-if="product.description" class="product__description">{{ product.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Product {
  id: number
  name: string
  price: number
  description: string | null
}

const products = ref<Product[]>([])
const loading = ref(true)
const error = ref('')

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function loadProducts() {
  try {
    const response = await fetch(`${API_BASE_URL}/products`)
    
    if (!response.ok) {
      throw new Error('Ошибка загрузки товаров')
    }
    
    const data = await response.json()
    products.value = data
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Неизвестная ошибка'
  } finally {
    loading.value = false
  }
}

onMounted(loadProducts)
</script>

<style scoped>
.home {
  padding: 20px;
  max-width: 1100px;
  margin: 0 auto;
}

.home__title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #1e1e1e;
}

.home__loading,
.home__error {
  text-align: center;
  padding: 40px;
  color: #666;
}

.home__error {
  color: #dc2626;
}

.home__products {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.home__product {
  padding: 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: box-shadow 0.2s ease;
}

.home__product:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.product__name {
  font-size: 18px;
  font-weight: 500;
  margin: 0 0 8px 0;
  color: #1e1e1e;
}

.product__price {
  font-size: 20px;
  font-weight: 600;
  color: #eaae52;
  margin: 0 0 8px 0;
}

.product__description {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.5;
}
</style>
