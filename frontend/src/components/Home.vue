<template>
  <div class="home__container">
    <div class="filters">
      <div class="filters__title">Фильтры</div>
      <div class="options">
        <div class="filter__option" :class="{ 'filter__option--active': activeFilters.includes('category') }"
          @click="toggleFilter('category')">
          Категория
          <div v-if="activeFilters.includes('category')">
            <Icon name="ChevronDown" :size="20" class="chevron" />
          </div>
          <div v-else>
            <Icon name="ChevronRight" :size="20" class="chevron" />
          </div>
        </div>

        <div v-if="activeFilters.includes('category')">
          <div class="category_filter">
            <label class="category_filter__label">Выберите категорию</label>
            <select v-model="selectedCategory">
              <option :value="null">Все категории</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
        </div>

        <div class="filter__option" :class="{ 'filter__option--active': activeFilters.includes('material') }"
          @click="toggleFilter('material')">
          Материал
          <div v-if="activeFilters.includes('material')">
            <Icon name="ChevronDown" :size="20" class="chevron" />
          </div>
          <div v-else>
            <Icon name="ChevronRight" :size="20" class="chevron" />
          </div>
        </div>

        <div v-if="activeFilters.includes('material')">
          <div class="category_filter">
            <label class="category_filter__label">Выберите материал</label>
            <select v-model="selectedMaterial">
              <option :value="null">Все материалы</option>
              <option v-for="material in materials" :key="material.id" :value="material.id">
                {{ material.name }}
              </option>
            </select>
          </div>
        </div>

        <div class="filter__option" :class="{ 'filter__option--active': activeFilters.includes('price') }"
          @click="toggleFilter('price')">
          Цена
          <div v-if="activeFilters.includes('price')">
            <Icon name="ChevronDown" :size="20" class="chevron" />
          </div>
          <div v-else>
            <Icon name="ChevronRight" :size="20" class="chevron" />
          </div>
        </div>

        <div v-if="activeFilters.includes('price')">
          <div class="category_filter">
            <label class="category_filter__label">Выберите цену</label>
            <div class="category_filter__price">
              <input type="number" v-model="minPrice" placeholder="От">
              <input type="number" v-model="maxPrice" placeholder="До">
            </div>
          </div>
        </div>

        <div class="filter__option" :class="{ 'filter__option--active': activeFilters.includes('country') }"
          @click="toggleFilter('country')">
          Страна
          <div v-if="activeFilters.includes('country')">
            <Icon name="ChevronDown" :size="20" class="chevron" />
          </div>
          <div v-else>
            <Icon name="ChevronRight" :size="20" class="chevron" />
          </div>
        </div>

        <div v-if="activeFilters.includes('country')">
          <div class="category_filter">
            <label class="category_filter__label">Выберите страну</label>
            <select v-model="selectedCountry">
              <option :value="null">Все страны</option>
              <option v-for="country in countries" :key="country.id" :value="country.id">
                {{ country.name }}
              </option>
            </select>
          </div>
        </div>

        <div class="filter__end" :class="{ 'filter__end--active': activeFilters.includes('color') }"
          @click="toggleFilter('color')">
          Цвет
          <div v-if="activeFilters.includes('color')">
            <Icon name="ChevronDown" :size="20" class="chevron" />
          </div>
          <div v-else>
            <Icon name="ChevronRight" :size="20" class="chevron" />
          </div>
        </div>

        <div v-if="activeFilters.includes('color')">
          <div class="category_filter">
            <label class="category_filter__label">Выберите цвет</label>
            <select v-model="selectedColor">
              <option :value="null">Все цвета</option>
              <option v-for="color in colors" :key="color.id" :value="color.id">
                {{ color.name }}
              </option>
            </select>
          </div>
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
        <div v-for="product in displayedProducts" :key="product.id" class="home__product"
          @click="openProductModal(product)">
          <!-- Показываем изображение если есть, иначе пропускаем -->
          <div class="product__image">
            <img v-if="product.images && product.images.length > 0" :src="`${API_BASE_URL}${product.images[0]?.url}`"
              alt="Product image" class="product__imageImg" />
          </div>

          <h3 class="product__name">{{ product.name }}</h3>
          <div class="product__bottom">
            <div class="product__priceBlock">
              <p class="product__price">{{ product.price }} ₽</p>
              <p class="product__priceUnit">за шт.</p>
            </div>
            <button class="product__cartBtn" type="button" @click.stop="handleAddToCart(product)">
              <Icon name="ShoppingCart" :size="20" className="product__cartIcon" />
            </button>
          </div>
        </div>
      </div>

      <ProductModal v-model="isModalOpen" :product="selectedProduct" />
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, inject, computed, watch, type Ref } from 'vue'
import { useCart } from '../composables/useCart'
import Icon from './Icon.vue'
import ProductModal from './products/ProductModal.vue'
import type { Product } from '../types/product'

interface Material {
  id: number
  name: string
}

interface Color {
  id: number
  name: string
  code: string | null
}

interface Country {
  id: number
  name: string
}

interface Category {
  id: number
  name: string
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const products = ref<Product[]>([])
const materials = ref<Material[]>([])
const loading = ref(true)
const error = ref('')
const activeFilters = ref<string[]>([])

const minPrice = ref('')
const selectedCategory = ref<number | null>(null)
const maxPrice = ref('')
const selectedMaterial = ref<number | null>(null)
const selectedColor = ref<number | null>(null)
const selectedCountry = ref<number | null>(null)

const categories = ref<Category[]>([])
const colors = ref<Color[]>([])
const countries = ref<Country[]>([])

const { addToCart } = useCart()

// Состояние для модального окна
const selectedProduct = ref<Product | undefined>(undefined)
const isModalOpen = ref(false)

// Функция для открытия модала
const openProductModal = (product: Product) => {
  selectedProduct.value = product
  isModalOpen.value = true
}

function handleAddToCart(product: Product) {
  if (typeof product.price !== 'number') {
    return
  }

  addToCart({
    id: product.id,
    name: product.name,
    price: product.price,
    images: product.images
      .filter((image): image is Product['images'][number] & { url: string } => typeof image.url === 'string')
      .map((image) => ({ url: image.url })),
  })
}

// Получаем результаты поиска из App.vue через inject
const searchResults = inject<Ref<Product[]>>('searchResults');

// Вычисляемые товары: если есть результаты поиска - показываем их, иначе все товары
const displayedProducts = computed(() => {
  if (searchResults?.value && searchResults.value.length > 0) {
    return searchResults.value;
  }
  return products.value;
});

// Функции для фильров (available обрабатывается на бэке)
async function getCategories() {
  const response = await fetch(`${API_BASE_URL}/categories/available`)

  if (response.ok) {
    const data = await response.json()
    categories.value = data
  }
}

async function getMaterials() {
  const response = await fetch(`${API_BASE_URL}/materials/available`)

  if (response.ok) {
    const data = await response.json()
    materials.value = data
  }
}

async function getColors() {
  const response = await fetch(`${API_BASE_URL}/colors/available`)

  if (response.ok) {
    const data = await response.json()
    colors.value = data
  }
}

async function getCountries() {
  const response = await fetch(`${API_BASE_URL}/countries/available`)

  if (response.ok) {
    const data = await response.json()
    countries.value = data
  }
}

async function loadProducts() {
  try {
    const params = new URLSearchParams();
    if (activeFilters.value.includes('category') && selectedCategory.value) {
      params.set('category', String(selectedCategory.value))
    }
    if (activeFilters.value.includes('price')) {
      const min = parseFloat(minPrice.value);
      const max = parseFloat(maxPrice.value);

      // NaN - Not a Number
      if (!Number.isNaN(min)) params.set('min_price', String(min))
      if (!Number.isNaN(max)) params.set('max_price', String(max))
    }

    if (activeFilters.value.includes('material') && selectedMaterial.value) {
      params.set('material', String(selectedMaterial.value))
    }

    if (activeFilters.value.includes('color') && selectedColor.value) {
      params.set('color', String(selectedColor.value))
    }

    if (activeFilters.value.includes('country') && selectedCountry.value) {
      params.set('country', String(selectedCountry.value))
    }

    const url = `${API_BASE_URL}/products/${params.toString() ? `?${params.toString()}` : ''}`
    const response = await fetch(url)

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

watch(
  [minPrice, maxPrice],
  () => {
    if (activeFilters.value.includes('price')) {
      loadProducts()
    }
  },
)

watch(
  selectedCategory,
  () => {
    if (activeFilters.value.includes('category')) {
      loadProducts()
    }
  },
)

watch(
  selectedMaterial,
  () => {
    if (activeFilters.value.includes('material')) {
      loadProducts()
    }
  },
)

watch(
  selectedColor,
  () => {
    if (activeFilters.value.includes('color')) {
      loadProducts()
    }
  },
)

watch(
  selectedCountry,
  () => {
    if (activeFilters.value.includes('country')) {
      loadProducts()
    }
  },
)

watch(
  activeFilters,
  () => {
    if (activeFilters.value.includes('price')) {
      loadProducts()
    }
  },
)

watch(
  activeFilters,
  () => {
    if (activeFilters.value.includes('category')) {
      loadProducts()
    }
  },
)


function toggleFilter(filter: string) {
  if (activeFilters.value.includes(filter)) {
    // Если фильтр уже есть - создаём новый массив без него
    activeFilters.value = activeFilters.value.filter(f => f !== filter)
  } else {
    // Если фильтра нет - создаём новый массив с ним
    activeFilters.value = [...activeFilters.value, filter]
  }
}

onMounted(() => {
  getCategories()
  getMaterials()
  getColors()
  getCountries()
  loadProducts()
})
</script>

<style scoped>
.home__container {
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
  cursor: pointer;
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
  transform: scale(0.95);
  background: #e5e7eb;
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
  top: calc(30px + 70px + 16px + 10px);
  /* topbar + header + padding + margin */
}

.filters__title {
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

.chevron {
  display: flex;
  flex-direction: row;
  color: #1e1e1e;
}

.filter__option {
  color: #1e1e1e;
  padding: 12px 12px;
  border-right: 1px solid #e5e7eb;
  border-left: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  background: white;
  cursor: pointer;
  transition: all 0.1s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter__option:hover {
  background: #EFEFEF;
}

.filter__option--active {
  background: #EFEFEF;
  position: relative;
}

.filter__end {
  color: #1e1e1e;
  padding: 12px 12px;
  border-right: 1px solid #e5e7eb;
  border-left: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  background: white;
  cursor: pointer;
  transition: all 0.1s ease;
  /* border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px; */
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter__end:hover {
  background: #EFEFEF;
}

.filter__end--active {
  background: #EFEFEF;
  position: relative;
}

.filter__option--active::before,
.filter__end--active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 25%;
  width: 3px;
  height: 50%;
  background: #1e1e1e;
  border-radius: 999px;
}

.category_filter {
  padding: 16px;
  border-right: 1px solid #e5e7eb;
  border-left: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  background: #fafafa;
}

.category_filter__label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.category_filter select,
.category_filter input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  color: #1e1e1e;
  background: white;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  outline: none;
}

.category_filter select:hover,
.category_filter input:hover {
  border-color: #9ca3af;
}

.category_filter select:focus,
.category_filter input:focus {
  border-color: #1e1e1e;
}

.category_filter__price {
  display: flex;
  gap: 10px;
}

.category_filter__price input {
  flex: 1;
}

/* Chrome, Edge, Safari */
.category_filter input[type="number"]::-webkit-outer-spin-button,
.category_filter input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  appearance: none;
  margin: 0;
}

/* Firefox */
.category_filter input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
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
