import { createRouter, createWebHistory } from 'vue-router'
import Home from '../vistas/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/catalogo',
    name: 'Catalogo',
    component: () => import('../vistas/Catalogo.vue')
  },
  {
    path: '/producto/:id',
    name: 'ProductoDetalle',
    component: () => import('../vistas/ProductoDetalle.vue')
  },
  {
    path: '/registro',
    name: 'Registro',
    component: () => import('../vistas/Registro.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
