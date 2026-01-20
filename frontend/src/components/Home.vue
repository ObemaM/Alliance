<template>
  <div class="home__container">
    <div class="filters">
      <div class="filters__title">Фильтры</div>
      <div class="options">
        <div
          class="filter__option"
          :class="{ 'filter__option--active': activeFilters.includes('category') }"
          @click="toggleFilter('category')"
        >
          Категория
        </div>
        <div
          class="filter__option"
          :class="{ 'filter__option--active': activeFilters.includes('price') }"
          @click="toggleFilter('price')"
        >
          Цена
        </div>
        <div
          class="filter__option"
          :class="{ 'filter__option--active': activeFilters.includes('material') }"
          @click="toggleFilter('material')"
        >
          Материал
        </div>
        <div
          class="filter__option"
          :class="{ 'filter__option--active': activeFilters.includes('purpose') }"
          @click="toggleFilter('purpose')"
        >
          Назначение
        </div>
        <div
          class="filter__end"
          :class="{ 'filter__end--active': activeFilters.includes('color') }"
          @click="toggleFilter('color')"
        >
          Цвет
        </div>

      </div>
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
          <div class="product__bottom">
            <div class="product__priceBlock">
              <p class="product__price">{{ product.price }} ₽</p>
              <p class="product__priceUnit">за шт.</p>
            </div>
            <button class="product__cartBtn" type="button" @click="addToCart(product)">
              <Icon name="ShoppingCart" :size="20" className="product__cartIcon" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCart } from '../composables/useCart'
import Icon from './Icon.vue'

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
  purpose: string | null
  created_at: string |  null 
  updated_at: string | null
  images: ProductImage[]
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const products = ref<Product[]>([])
const loading = ref(true)
const error = ref('')
const activeFilters = ref<string[]>([])

const { addToCart } = useCart()

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

function toggleFilter(filter: string){
  if (activeFilters.value.includes(filter)){
    // Если фильтр уже есть - создаём новый массив без него
    activeFilters.value = activeFilters.value.filter(f => f !== filter)
  } else {
    // Если фильтра нет - создаём новый массив с ним
    activeFilters.value = [...activeFilters.value, filter]
  }
}


onMounted(loadProducts)
</script>

<style scoped>

.home__container{
  margin: 0 auto;
  max-width: 1100px;
  display: flex;
  gap: 40px;
  padding-top: 20px;
  padding-left: 20px;
  padding-bottom: 20px;
}

.home {
  padding-right: 20px;
  padding-top: 20px;
  padding-bottom: 20px;
  padding-left: 20px;
  max-width: 1100px;
  margin: 0 auto;
  flex: 1;
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
  height: 320px;
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
  font-size: 15px;
  font-weight: 500;
  margin: 0 0 8px 0;
  color: #1e1e1e;
  padding: 12px 14px 0 14px;
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product__price {
  height: 30px;
  font-size: 20px;
  font-weight: 700;
  color: #1e1e1e;
  margin: 0;
}

.product__bottom {
  margin-top: auto;
  padding: 0 14px 14px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.product__priceBlock {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.product__priceUnit {
  margin: 0;
  font-size: 12px;
  color: #6b7280;
  line-height: 1;
}

.product__cartBtn {
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 10px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.product__cartBtn:hover {
  background: #e5e7eb;
}

.product__cartBtn:active {
  transform: scale(0.98);
}

.product__cartIcon {
  color: #1e1e1e;
}

.product__description {
  font-size: 12px;
  color: #666;
  margin: 0;
  line-height: 1.5;
}

.product__image {
  position: relative;
  background: #ffffff;
  overflow: hidden;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e5e7eb;
}

.product__imageImg {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
  padding: 10px;
  position: relative;
}

.home__product:hover .product__imageImg {
  transform: scale(1.05);
}

.filters {
  background-color: #f3f4f6;
  width: 250px;
  background: white;
  border-radius: 8px;
  height: fit-content;
  position: sticky;
  top: calc(30px + 70px + 16px + 10px); /* topbar + header + padding + margin */
}

.filters__title{
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  color: #ffffff;
  padding: 16px;
  background-color: #1e1e1e;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 12px;
  font-size: 18px;
  font-weight: 600;
}

.filter__option{
  color: #1e1e1e;
  padding: 12px 12px;
  border-right: 1px solid #e5e7eb;
  border-left: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter__option:hover{
  background: #f3f4f6;
}

.filter__option--active{
  background: #e5e7eb;
  font-weight: 600;
}

.filter__end{
  color: #1e1e1e;
  padding: 12px 12px;
  border-right: 1px solid #e5e7eb;
  border-left: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.filter__end:hover{
  background: #f3f4f6;
}

.filter__end--active{
  background: #e5e7eb;
  font-weight: 600;
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
