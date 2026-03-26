<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  content: string
  isLoading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
})

const displayedContent = computed(() =>
  props.isLoading ? 'Загрузка контента...' : props.content,
)
</script>

<template>
  <section class="site-page">
    <div class="site-page__container">
      <div class="site-page__card">
        <p class="site-page__eyebrow">Информация</p>
        <h1 class="site-page__title">{{ title }}</h1>
        <div class="site-page__content">{{ displayedContent }}</div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.site-page {
  width: 100%;
}

.site-page__container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 20px;
}

.site-page__card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
}

.site-page__eyebrow {
  margin: 0 0 12px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.site-page__title {
  margin: 0 0 24px;
  color: #1e1e1e;
  font-size: 34px;
  line-height: 1.15;
  font-weight: 700;
}

.site-page__content {
  margin-bottom: 32px;
  color: #374151;
  font-size: 16px;
  line-height: 1.8;
  white-space: pre-wrap;
}

@media (max-width: 740px) {
  .site-page__container {
    padding: 28px 20px;
  }

  .site-page__card {
    padding: 24px 20px;
    border-radius: 16px;
  }

  .site-page__title {
    font-size: 28px;
  }
}
</style>
