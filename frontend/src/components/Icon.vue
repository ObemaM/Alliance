<template>
  <component :is="iconComponent" :size="size" :class="className" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ShoppingCart, Search, Trash2, X } from 'lucide-vue-next'

interface Props {
  name: string
  size?: number
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 24,
  className: ''
})

const iconComponent = computed(() => {
  switch (props.name) {
    case 'ShoppingCart':
      return ShoppingCart
    case 'Search':
      return Search
    case 'Trash2':
      return Trash2
    case 'X':
      return X
  }
})
</script>
