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
    component: () => import('../vistas/CatalogoProductos.vue')
  },
  {
    path: '/producto/:id',
    name: 'ProductoDetalle',
    component: () => import('../vistas/DetalleProducto.vue')
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
  },
  {
    path: '/quienes-somos',
    name: 'QuienesSomos',
    component: () => import('../vistas/QuienesSomos.vue')
  },
  {
    path: '/como-funciona',
    name: 'ComoFunciona',
    component: () => import('../vistas/ComoFunciona.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
