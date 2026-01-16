<template>
  <div class="filters">
  </div>
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

        <!-- Показываем изображение если есть, иначе пропускаем -->
        <div class="product__image">
          <img 
            v-if="product.images && product.images.length > 0" 
            :src="`${API_BASE_URL}${product.images[0]?.url}`" 
            alt="Product image" 
            class="product__imageImg"
          />
        </div>

        <h3 class="product__name">{{ product.name }}</h3>
        <p class="product__price">{{ product.price }} ₽</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface ProductImage {
  id: number;
  product_id: number;
  url: string;
}

interface Product {
  id: number
  name: string
  price: number
  description: string | null
  category_id: number | null
  pack_quantity: number | null
  quantity: number | null
  weight: string | null
  color_id: number | null
  material_id: number | null
  country_id: number | null
  created_at: string |  null 
  updated_at: string | null
  images: ProductImage[]
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const products = ref<Product[]>([])
const loading = ref(true)
const error = ref('')

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
  padding-right: 20px;
  padding-top: 20px;
  padding-bottom: 20px;
  padding-left: 300px;
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
  display: grid;
  grid-template-columns: repeat(3, 230px);
  gap: 20px;
}

.home__product {
  width: 230px;
  height: 280px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.06);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.home__product:hover {
  box-shadow: 0 10px 24px rgba(16, 24, 40, 0.12);
}

.product__name {
  font-size: 18px;
  font-weight: 500;
  margin: 0 0 8px 0;
  color: #1e1e1e;
  padding: 12px 14px 0 14px;
}

.product__price {
  font-size: 20px;
  font-weight: 600;
  color: #eaae52;
  margin: 0;
  padding: 0 14px 14px 14px;
}

.product__description {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.5;
}

.product__image {
  position: relative;
  height: 180px;
  background: #f3f4f6;
  overflow: hidden;
}

.product__imageImg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.home__product:hover .product__imageImg {
  transform: scale(1.05);
}

@media (max-width: 1000px) {
  .home__products {
    grid-template-columns: repeat(2, 230px);
  }
}

@media (max-width: 740px) {
  .home {
    padding-left: 20px;
  }

  .home__products {
    grid-template-columns: repeat(1, 230px);
    justify-content: center;
  }
}
</style>
