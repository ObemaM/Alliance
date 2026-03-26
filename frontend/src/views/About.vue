<script setup lang="ts">
import SiteContentPage from '../components/info-pages/SiteContentPage.vue'
import { useSiteContentPage } from '../composables/useSiteContentPage'

const { content, isLoading } = useSiteContentPage(`Страница "О компании"`)
</script>

<template>
  <div class="about-view">
    <SiteContentPage
      title="О компании"
      :content="content"
      :is-loading="isLoading"
    />
  </div>
</template>

<style scoped>
.about-view {
  width: 100%;
}
</style>
