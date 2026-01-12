<template>
  <label class="search">
    <Icon name="Search" :size="20" class="search__icon" />
    <input
      type="text"
      :placeholder="placeholder"
      :value="modelValue"
      @input="onInput"
      class="search__field"
    />
  </label>
</template>

<script setup lang="ts">
import Icon from './Icon.vue'

interface Props {
  modelValue: string
  placeholder?: string
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Поиск товаров...'
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

function onInput(event: Event) {
  const target = event.target as HTMLInputElement | null
  emit('update:modelValue', target?.value ?? '')
}
</script>

<style scoped>
.search {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 360px;
  background-color: white;
}

.search__icon {
  position: absolute;
  left: 14px;
  color: #9ca3af;
  pointer-events: none;
}

.search__field {
  width: 100%;
  padding: 10px 14px 10px 44px;
  border: 2px solid #e5e7eb;
  border-radius: 999px;
  font-size: 14px;
  background-color: #f9fafb;
  transition: border-color 0.2s ease, background-color 0.2s ease;
  font-size: 15px;
  font-family: Calibri, sans-serif;
  color: #1e1e1e;
}

.search__field:focus {
  outline: none;
  border-color: #eaae52;
  background-color: #fff;
}

.search__field::placeholder {
  color: #9ca3af;
}
</style>