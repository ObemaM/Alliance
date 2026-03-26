<template>
  <component :is="iconComponent" :size="size" :class="className" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ShoppingCart, Search, Trash2, X, ChevronDown, ChevronRight, ArrowLeft } from 'lucide-vue-next'

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
    case 'ChevronDown':
      return ChevronDown
    case 'ChevronRight':
      return ChevronRight
    case 'X':
      return X
    case 'ArrowLeft':
      return ArrowLeft
  }
})
</script>
