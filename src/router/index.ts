import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/catalogo',
    name: 'Catalogo',
    component: () => import('../views/Catalogo.vue')
  },
  {
    path: '/producto/:id',
    name: 'ProductoDetalle',
    component: () => import('../views/ProductoDetalle.vue')
  },
  {
    path: '/registro',
    name: 'Registro',
    component: () => import('../views/Registro.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
