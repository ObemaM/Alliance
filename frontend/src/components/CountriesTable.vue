<template>
  <div class="table-container">
    <h2>Страны</h2>
    <table v-if="countries.length > 0">
      <thead>
        <tr>
          <th>Название</th>
        </tr>
      </thead>
      <tbody>
        <!-- Вот здесь Vue автоматически создает строки для каждой страны -->
        <tr v-for="country in countries" :key="country.id">
          <td>{{ country.name }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="loading">Загрузка...</p>
    <p v-else>Нет данных</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getCountries } from '../services/api';
import type { Country } from '../types';

// Реактивные переменные
const countries = ref<Country[]>([]);
const loading = ref(true);

// Загрузка данных при монтировании компонента
onMounted(async () => {
  try {
    countries.value = await getCountries();
  } catch (error) {
    console.error('Ошибка загрузки стран:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.table-container {
  margin-bottom: 30px;
}

h2 {
  color: #333;
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #4caf50;
  color: white;
  font-weight: bold;
}

tr:hover {
  background-color: #f5f5f5;
}

p {
  color: #666;
}
</style>
