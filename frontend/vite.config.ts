import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // Слушать на всех адресах (0.0.0.0)
    port: 5173, // Фиксированный порт
    strictPort: false, // Если 5173 занят, попробовать следующий
    proxy: {
      '/api': {
        target: process.env.VITE_DEV_API_PROXY_TARGET || 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/uploads': {
        target: process.env.VITE_DEV_API_PROXY_TARGET || 'http://localhost:8000',
        changeOrigin: true,
      },
      '/admin': {
        target: process.env.VITE_DEV_API_PROXY_TARGET || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
