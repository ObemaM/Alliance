<template>
  <div id="app">
    <h1>Управление данными</h1>
    <CountriesTable />
    <ColorsTable />
  </div>
</template>

<script setup lang="ts">
import CountriesTable from './components/CountriesTable.vue';
import ColorsTable from './components/ColorsTable.vue';
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  margin: 20px;
  background-color: #f4f4f9;
  min-height: 100vh;
  padding: 20px;
}

h1 {
  color: #333;
  margin-bottom: 30px;
}

body {
  margin: 0;
  padding: 0;
}
</style>
