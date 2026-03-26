import { onMounted, shallowRef } from 'vue'

type SiteContentItem = {
  id: number
  key: string
  value: string
  description: string | null
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export function useSiteContentPage(pageKey: string) {
  const content = shallowRef('Контент недоступен')
  const isLoading = shallowRef(true)

  async function loadPageContent() {
    try {
      const response = await fetch(`${API_BASE_URL}/site-content/`)

      if (!response.ok) {
        return
      }

      const data = (await response.json()) as SiteContentItem[]
      const contentMap = new Map<string, string>()

      for (const item of data) {
        contentMap.set(item.key, item.value)
      }

      content.value = contentMap.get(pageKey) ?? 'Контент недоступен'
    } catch {
      return
    } finally {
      isLoading.value = false
    }
  }

  onMounted(loadPageContent)

  return {
    content,
    isLoading,
  }
}
