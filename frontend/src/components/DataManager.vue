<script setup lang="ts">
// <script setup lang="ts"> - это специальный синтаксис Vue 3.
// "setup" означает, что код внутри выполняется при создании компонента.
// "lang='ts'" говорит, что мы используем TypeScript.

// Импортируем функции из Vue
// ref - используется для создания реактивных переменных (которые меняются на странице)
// onMounted - хук, который запускается, когда компонент "смонтирован" (появился на странице)
import { ref, onMounted } from 'vue';

// Импортируем наши функции для запросов к API
import { getCountries, getColors, getCategories, createCountry } from '../services/api';

// Импортируем типы данных (интерфейсы), чтобы TypeScript понимал структуру наших объектов
import type { Country, Color, Category } from '../types';

// ==========================================
// СОСТОЯНИЕ (STATE)
// ==========================================

// 1. СТРАНЫ
// ref<Country[]>([]) означает:
// - Создай реактивную переменную
// - Тип данных: массив объектов Country (Country[])
// - Начальное значение: пустой массив ([])
const countries = ref<Country[]>([]);
const countriesLoading = ref<boolean>(false); // Тип boolean (true/false)
const countriesError = ref<string | null>(null); // Тип string или null (если ошибки нет)

// 2. ЦВЕТА
const colors = ref<Color[]>([]);
const colorsLoading = ref<boolean>(false);
const colorsError = ref<string | null>(null);

// 3. КАТЕГОРИИ
const categories = ref<Category[]>([]);
const categoriesLoading = ref<boolean>(false);
const categoriesError = ref<string | null>(null);

// ==========================================
// МЕТОДЫ (FUNCTIONS)
// ==========================================

// Асинхронная функция для загрузки стран
const fetchCountries = async () => {
  countriesLoading.value = true; // В ref-переменных обращаемся к значению через .value
  countriesError.value = null;

  try {
    // Ждем ответ от API
    const data = await getCountries();
    countries.value = data; // Сохраняем полученные данные
  } catch (err) {
    console.error('Ошибка загрузки стран:', err);
    countriesError.value = 'Не удалось загрузить страны.';
  } finally {
    countriesLoading.value = false; // Выключаем индикатор загрузки
  }
};

const newCountryName = ref('');

const addCountry = async () => {
  if (!newCountryName.value) return;

  try {
    const newCountry = await createCountry(newCountryName.value);
    countries.value.push(newCountry);
    newCountryName.value = '';
  } catch (err) {
    console.error('Ошибка добавления страны:', err);
    alert('Не удалось добавить страну');
  }
};

// Асинхронная функция для загрузки цветов
const fetchColors = async () => {
  colorsLoading.value = true;
  colorsError.value = null;

  try {
    const data = await getColors();
    colors.value = data;
  } catch (err) {
    console.error('Ошибка загрузки цветов:', err);
    colorsError.value = 'Не удалось загрузить цвета.';
  } finally {
    colorsLoading.value = false;
  }
};

// Асинхронная функция для загрузки категорий
const fetchCategories = async () => {
  categoriesLoading.value = true;
  categoriesError.value = null;

  try {
    const data = await getCategories();
    categories.value = data;
  } catch (err) {
    console.error('Ошибка загрузки категорий:', err);
    categoriesError.value = 'Не удалось загрузить категории.';
  } finally {
    categoriesLoading.value = false;
  }
};

// ==========================================
// ЖИЗНЕННЫЙ ЦИКЛ (LIFECYCLE)
// ==========================================

// onMounted запускается автоматически, когда компонент готов
onMounted(async () => {
  // Запускаем все загрузки параллельно
  await Promise.all([
    fetchCountries(),
    fetchColors(),
    fetchCategories()
  ]);
});
</script>

<template>
  <div class="data-manager">
    <h1>Данные</h1>

    <!-- ТАБЛИЦА СТРАН -->
    <section>
      <h2>Страны</h2>
      <!-- v-if - условный рендеринг: показываем, если true -->
      <p v-if="countriesLoading" class="loading">Загрузка стран...</p>
      <p v-else-if="countriesError" class="error">{{ countriesError }}</p>
      
      <!-- v-else-if - показываем таблицу, если есть данные -->
      <table v-else-if="countries.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
          </tr>
        </thead>
        <tbody>
          <!-- v-for - цикл: создаем строку для каждой страны -->
          <!-- :key - обязательный уникальный ключ для оптимизации Vue -->
          <tr v-for="country in countries" :key="country.id">
            <td>{{ country.id }}</td>
            <td>{{ country.name }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>Нет данных о странах</p>

      <!-- ФОРМА ДОБАВЛЕНИЯ СТРАНЫ -->
      <div class="add-form">
        <input 
          v-model="newCountryName" 
          placeholder="Название новой страны" 
          @keyup.enter="addCountry"
        />
        <button @click="addCountry" :disabled="!newCountryName">Добавить</button>
      </div>
    </section>

    <!-- ТАБЛИЦА ЦВЕТОВ -->
    <section>
      <h2>Цвета</h2>
      <p v-if="colorsLoading" class="loading">Загрузка цветов...</p>
      <p v-else-if="colorsError" class="error">{{ colorsError }}</p>
      <table v-else-if="colors.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Код</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="color in colors" :key="color.id">
            <td>{{ color.id }}</td>
            <td>{{ color.name }}</td>
            <td>
              <!-- template - невидимая обертка для группировки -->
              <template v-if="color.code">
                <!-- :style - динамические стили -->
                <span 
                  class="color-box" 
                  :style="{ backgroundColor: color.code }"
                ></span>
                {{ color.code }}
              </template>
              <span v-else>—</span>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>Нет данных о цветах</p>
    </section>

    <!-- ТАБЛИЦА КАТЕГОРИЙ -->
    <section>
      <h2>Категории</h2>
      <p v-if="categoriesLoading" class="loading">Загрузка категорий...</p>
      <p v-else-if="categoriesError" class="error">{{ categoriesError }}</p>
      <table v-else-if="categories.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.id">
            <td>{{ category.id }}</td>
            <td>{{ category.name }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>Нет данных о категориях</p>
    </section>
  </div>
</template>

<!-- scoped означает, что стили действуют ТОЛЬКО на этот компонент -->
<style scoped>
.data-manager {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #333;
  text-align: center;
}

h2 {
  color: #333;
  margin-top: 30px;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
  color: black;
}

th {
  background-color: #4CAF50;
  color: black;
}

tr:hover {
  background-color: #f5f5f5;
}

.loading {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 20px;
}

.error {
  color: #d32f2f;
  background-color: #ffebee;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.color-box {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 1px solid #ccc;
  margin-right: 8px;
  vertical-align: middle;
  border-radius: 4px;
}

.add-form {
  width: 50%;
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.add-form input {
  background-color: white;
  color: black;
  flex: 1;
  padding: 8px;
  border: 1px solid black;
  border-radius: 4px;
}

.add-form input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px #4CAF50;
}

.add-form button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: black;
  border: 1px solid black;
  border-radius: 4px;
  cursor: pointer;
}

.add-form button:disabled {
  background-color: #4CAF50;
  cursor: not-allowed;
}
</style>
