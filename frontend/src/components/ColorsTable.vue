<template>
  <div class="table-container">
    <h2>Цвета</h2>
    <table v-if="colors.length > 0">
      <thead>
        <tr>
          <th>Название</th>
          <th>Код</th>
        </tr>
      </thead>
      <tbody>
        <!-- Vue автоматически создает строки для каждого цвета -->
        <tr v-for="color in colors" :key="color.id">
          <td>{{ color.name }}</td>
          <td>
            <!-- Если код есть, показываем его с цветным квадратиком -->
            <span v-if="color.code" class="color-display">
              <span 
                class="color-box" 
                :style="{ backgroundColor: color.code }"
              ></span>
              {{ color.code }}
            </span>
            <span v-else>—</span>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="loading">Загрузка...</p>
    <p v-else>Нет данных</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getColors } from '../services/api';
import type { Color } from '../types';

const colors = ref<Color[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    colors.value = await getColors();
  } catch (error) {
    console.error('Ошибка загрузки цветов:', error);
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

/* Стили для отображения цвета */
.color-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-box {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

p {
  color: #666;
}
</style>
