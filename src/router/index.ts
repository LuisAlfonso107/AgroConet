import { createRouter, createWebHistory } from 'vue-router'
import Home from '../vistas/Home.vue'
import { useAuth, type UserRole } from '../composables/useAuth'

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
    component: () => import('../vistas/Registro.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../vistas/Login.vue')
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
  },
  {
    path: '/contacto',
    name: 'Contacto',
    component: () => import('../vistas/Contacto.vue')
  },
  {
    path: '/dashboard/comprador',
    component: () => import('../componentes/comprador/DashboardComprador.vue'),
    meta: { requiresAuth: true, role: 'comprador' },
    children: [
      {
        path: '',
        name: 'DashboardCompradorResumen',
        component: () => import('../componentes/comprador/ResumenComprador.vue')
      },
      {
        path: 'pedidos',
        name: 'DashboardCompradorPedidos',
        component: () => import('../componentes/comprador/PedidoList.vue')
      },
      {
        path: 'pedidos/:id',
        name: 'DashboardCompradorPedidoDetalle',
        component: () => import('../componentes/comprador/PedidoDetalle.vue')
      },
      {
        path: 'tracking/:id',
        name: 'DashboardCompradorTracking',
        component: () => import('../componentes/comprador/TrackingPedido.vue')
      },
      {
        path: 'favoritos',
        name: 'DashboardCompradorFavoritos',
        component: () => import('../componentes/comprador/FavoritosList.vue')
      },
      {
        path: 'perfil',
        name: 'DashboardCompradorPerfil',
        component: () => import('../componentes/comprador/PerfilCompradorEdit.vue')
      }
    ]
  },
  {
    path: '/dashboard/productor',
    component: () => import('../componentes/productor/DashboardProductor.vue'),
    meta: { requiresAuth: true, role: 'productor' },
    children: [
      {
        path: '',
        name: 'DashboardProductorResumen',
        component: () => import('../componentes/productor/ResumenProductor.vue')
      },
      {
        path: 'productos',
        name: 'DashboardProductorProductos',
        component: () => import('../componentes/productor/ProductoList.vue')
      },
      {
        path: 'nuevo-producto',
        name: 'DashboardProductorNuevoProducto',
        component: () => import('../componentes/productor/ProductoForm.vue')
      },
      {
        path: 'editar-producto/:id',
        name: 'DashboardProductorEditarProducto',
        component: () => import('../componentes/productor/ProductoForm.vue')
      },
      {
        path: 'pedidos',
        name: 'DashboardProductorPedidos',
        component: () => import('../componentes/productor/PedidosRecibidos.vue')
      },
      {
        path: 'tracking/:id',
        name: 'DashboardProductorTracking',
        component: () => import('../componentes/comprador/TrackingPedido.vue')
      },
      {
        path: 'historial',
        name: 'DashboardProductorHistorial',
        component: () => import('../componentes/productor/VentasHistorial.vue')
      },
      {
        path: 'perfil',
        name: 'DashboardProductorPerfil',
        component: () => import('../componentes/productor/PerfilProductorEdit.vue')
      }
    ]
  },
  {
    path: '/dashboard/agencia',
    name: 'DashboardAgencia',
    component: () => import('../vistas/DashboardPendiente.vue'),
    meta: { requiresAuth: true, role: 'agencia' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const { currentUser, dashboardPathForRole } = useAuth()
  const requiredRole = to.meta.role as UserRole | undefined

  if (!to.meta.requiresAuth) return true

  if (!currentUser.value) {
    return {
      path: '/login',
      query: { mensaje: `Debes iniciar sesión como ${requiredRole || 'usuario'}` }
    }
  }

  if (requiredRole && currentUser.value.userType !== requiredRole) {
    return {
      path: dashboardPathForRole(currentUser.value.userType),
      query: { mensaje: 'No tienes permisos para acceder a esta sección' }
    }
  }

  return true
})

export default router
