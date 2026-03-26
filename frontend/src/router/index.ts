import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/About.vue')
  },
  {
    path: '/delivery',
    name: 'delivery',
    component: () => import('../views/Delivery.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
