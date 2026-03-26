<script setup lang="ts">
import SiteContentPage from '../components/info-pages/SiteContentPage.vue'
import { useSiteContentPage } from '../composables/useSiteContentPage'

const { content, isLoading } = useSiteContentPage(`Страница "Доставка и оплата"`)
</script>

<template>
  <div class="delivery-view">
    <SiteContentPage
      title="Доставка и оплата"
      :content="content"
      :is-loading="isLoading"
    />
  </div>
</template>

<style scoped>
.delivery-view {
  width: 100%;
}
</style>
