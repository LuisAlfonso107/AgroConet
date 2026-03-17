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
    component: () => import('../componentes/Catalogo.vue')
  },
  {
    path: '/producto/:id',
    name: 'ProductoDetalle',
    component: () => import('../componentes/ProductoDetalle.vue')
  },
  {
    path: '/registro',
    name: 'Registro',
    component: () => import('../componentes/Registro.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../componentes/Login.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
