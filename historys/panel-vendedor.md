
---
### Historia de Usuario US-014
**Panel del Vendedor (Productor) – Dashboard completo con gestión integral**
**Como** productor agrícola (caficultor, maicero, etc.)
**Quiero** acceder a un panel personal exclusivo para vendedores después de iniciar sesión
**Para** gestionar mis productos, recibir y administrar pedidos, actualizar stock, y visualizar métricas de mi negocio

**Criterios de Aceptación**

**Escenario 1: Redirección post-login según userType**
Dado que un usuario completa el registro o inicio de sesión exitosamente
Cuando el sistema valida sus credenciales contra `db.json` (`/users`)
Entonces:
- Si `userType === "productor"`, redirige automáticamente a `/dashboard/productor`
- Si `userType === "comprador"`, redirige automáticamente a `/dashboard/comprador`
- Si `userType === "agencia"`, redirige automáticamente a `/dashboard/agencia`
- La redirección se implementa en el guard de Vue Router (`beforeEach`) o en el store de autenticación
- Se valida que el token/sesión exista antes de permitir el acceso a cualquier ruta `/dashboard/*`

**Escenario 2: Barra de navegación superior del panel**
Dado que el productor ingresa al dashboard
Cuando se renderiza la vista
Entonces:
- Logo de AgroConet (enlace a Home)
- Indicador visual del rol activo: "Productor" con badge/icono
- Menú de navegación lateral (sidebar) colapsable con:
  - "Mis Productos" → `/dashboard/productor/productos`
  - "Publicar Nuevo" → `/dashboard/productor/nuevo-producto`
  - "Pedidos Recibidos" → `/dashboard/productor/pedidos`
  - "Historial de Ventas" → `/dashboard/productor/historial`
  - "Mi Perfil" → `/dashboard/productor/perfil`
- Botón de "Cerrar sesión" que limpia la sesión y redirige a Home
- En móvil: sidebar se oculta y se muestra menú hamburguesa; el panel usa 100% del ancho

**Escenario 3: Resumen / Dashboard principal (vista de aterrizaje)**
Dado que el productor accede a `/dashboard/productor`
Cuando se carga la vista principal del panel
Entonces se muestran 4 tarjetas de resumen en grid (responsive: 2 columnas en tablet, 1 en móvil):
- Tarjeta 1 – "Productos Activos": número total de productos publicados con estado `disponible`
- Tarjeta 2 – "Pedidos Pendientes": número de pedidos con estado `solicitado` o `pendiente`
- Tarjeta 3 – "Total Vendido (Qq)": suma de quintales vendidos en pedidos confirmados
- Tarjeta 4 – "Ingresos Estimados": suma de totales de pedidos en moneda local (Lempiras / Quetzales / Córdobas según región)
Debajo del resumen: tabla con los últimos 5 pedidos recibidos (más recientes primero) con columnas: Producto, Comprador, Cantidad, Total, Estado, Acción "Ver detalle"

**Escenario 4: Gestión de productos propios (CRUD completo)**
Dado que el productor navega a "Mis Productos"
Cuando se listan sus productos
Entonces:
- Se muestran SOLO los productos donde `productor` coincide con el nombre del productor autenticado (filtrado por backend o frontend)
- Cada fila/tarjeta muestra: nombre, tipo, precio, stock (quintales disponibles), humedad, estado (disponible/agotado/pausado), fecha de publicación
- Acciones por producto: "Editar" (lápiz), "Pausar/Reanudar" (toggle), "Eliminar" (confirmación previa)
- Botón "Publicar Nuevo Producto" que redirige a formulario de creación
- Paginación de 10 productos por página

**Escenario 5: Publicar nuevo producto (formulario completo con validaciones)**
Dado que el productor hace clic en "Publicar Nuevo Producto"
Cuando se carga el formulario
Entonces:
- Campos requeridos: nombre, tipo (select: café/maíz/frijol/arroz/otros), precio por quintal, cantidad en quintales, humedad (%), variedad, región, país, altura (msnm)
- Campos opcionales: certificaciones (multiselect), descripción, imagen (URL)
- Validaciones en cliente:
  - Nombre: requerido, mínimo 3 caracteres
  - Precio: requerido, número positivo > 0
  - Cantidad: requerido, número entero positivo > 0
  - Humedad: requerido, número entre 5 y 25
  - Región y país: requeridos
- Al enviar: `POST /productos` con el productor autofillado, `estado: "disponible"`, `createdAt: now`
- Éxito: mostrar toast/notificación "Producto publicado exitosamente" y redirigir a "Mis Productos"
- Error: mostrar mensajes de error específicos por campo

**Escenario 6: Editar producto existente**
Dado que el productor hace clic en "Editar" en un producto propio
Cuando se carga el formulario pre-rellenado
Entonces:
- Misma estructura que el formulario de creación pero con datos existentes precargados
- `PATCH /productos/:id` al enviar
- Validaciones idénticas al formulario de creación
- Botón "Cancelar" que regresa a "Mis Productos" sin guardar

**Escenario 7: Pedidos recibidos con acciones**
Dado que el productor navega a "Pedidos Recibidos"
Cuando se cargan los pedidos
Entonces:
- Filtra pedidos donde `productor` coincide con el nombre autenticado
- Tabla con: ID Pedido, Producto, Comprador, Cantidad (Qq), Total, Fecha, Estado (con badge de color: solicitado=amarillo, confirmado=verde, rechazado=rojo, en tránsito=azul, entregado=gris)
- Acciones por estado:
  - Si `estado === "solicitado"`: botones "Confirmar Pedido" (cambia a `confirmado`) y "Rechazar Pedido" (cambia a `rechazado`)
  - Si `estado === "confirmado"` o superior: botón "Ver Tracking" que redirige a `/tracking/:pedidoId`
- Al confirmar/rechazar: `PATCH /pedidos/:id` actualiza estado y crea registro en `/tracking`

**Escenario 8: Historial de ventas**
Dado que el productor navega a "Historial de Ventas"
Cuando se carga la vista
Entonces:
- Lista completa de pedidos con estado `entregado`
- Mismas columnas que pedidos recibidos pero filtro fijo por `entregado`
- Exportable a CSV (botón "Descargar reporte")
- Gráfico simple de barras (usando CSS o librería ligera) mostrando ventas por mes (últimos 6 meses)

**Escenario 9: Perfil del productor (configuración)**
Dado que el productor navega a "Mi Perfil"
Cuando se carga la vista
Entonces:
- Datos actuales precargados: nombre (readonly), email (readonly), teléfono, foto de perfil, nombre de finca, ubicación (lat/lon o dirección), descripción breve
- Campos editables: teléfono, foto, nombre de finca, ubicación, descripción
- `PATCH /users/:id` al guardar cambios
- Botón "Cambiar contraseña" (en fase 2 con backend real)

**Escenario 10: Seguridad y control de acceso**
Dado que un usuario no autenticado o con rol diferente intenta acceder a `/dashboard/productor/*`
Cuando el guard de ruta se ejecuta
Entonces:
- Si no hay sesión activa: redirigir a `/login` con mensaje "Debes iniciar sesión como productor"
- Si el rol no es `productor`: redirigir a su dashboard correspondiente con mensaje "No tienes permisos para acceder a esta sección"
- Si el rol es `productor` pero el producto solicitado en edición no le pertenece: mostrar error 403 "No puedes modificar un producto que no te pertenece"

**Notas Técnicas – Principios SOLID Aplicados**

**S – Single Responsibility Principle (Principio de Responsabilidad Única)**
- Cada vista/vue tendrá una única responsabilidad:
  - `DashboardProductor.vue` → solo orquestación y layout del panel
  - `ProductoList.vue` → solo listar/CRUD de productos
  - `ProductoForm.vue` → solo creación/edición de producto
  - `PedidosList.vue` → solo listar pedidos recibidos
  - `VentasHistorial.vue` → solo historial y estadísticas
  - `PerfilProductor.vue` → solo edición de perfil
- Los servicios serán clases separadas:
  - `ProductoService.ts` → solo operaciones CRUD de productos
  - `PedidoService.ts` → solo operaciones CRUD de pedidos
  - `AuthService.ts` → solo autenticación y autorización
  - `TrackingService.ts` → solo consultas de tracking

**O – Open/Closed Principle (Principio Abierto/Cerrado)**
- Los servicios estarán diseñados para ser extendidos sin modificar su código base:
  - `ProductoService` tendrá métodos base (`getAll`, `getById`, `create`, `update`, `delete`)
  - Si se necesita filtrado avanzado, se extiende vía parámetros (composición), no modificando el método base
- Los componentes de formulario (`ProductoForm`) aceptarán `props` para modo "crear" o "editar", sin duplicar lógica

**L – Liskov Substitution Principle (Principio de Sustitución de Liskov)**
- Las interfaces `IProducto`, `IPedido`, `IUser` se definirán en `types/` y cualquier implementación concreta debe cumplir el contrato
- Los servicios mock (json-server) y futuros servicios reales (API REST) compartirán la misma interfaz `IProductoService`, permitiendo sustituir uno por otro sin cambiar los consumidores

**I – Interface Segregation Principle (Principio de Segregación de Interfaces)**
- Interfaces específicas y pequeñas en lugar de una interfaz general:
  - `IProductoBase` → nombre, tipo, precio, stock
  - `IProductoCompleto` → extiende IProductoBase + certificaciones, descripción, etc.
  - `IPedidoResumen` → id, producto, estado, total
  - `IPedidoDetalle` → extiende IPedidoResumen + tracking, factura, etc.
- Un componente de listado solo usará `IProductoBase`, no necesitará conocer datos complejos

**D – Dependency Inversion Principle (Principio de Inversión de Dependencias)**
- Los componentes Vue dependerán de abstracciones (interfaces), no de implementaciones concretas
- La inyección de dependencias se hará mediante:
  - Provides/Inject de Vue 3 para servicios
  - El store de Pinia actuará como fachada entre componentes y servicios
- Ejemplo: `DashboardProductor.vue` usará `useProductoStore()` que internamente usa `ProductoService`, pero el componente no conoce la implementación del servicio

**Arquitectura de Carpetas Propuesta**
```
src/
├── components/
│   ├── productor/
│   │   ├── DashboardProductor.vue      # Layout principal del panel
│   │   ├── ProductoList.vue            # Lista de productos del productor
│   │   ├── ProductoForm.vue            # Formulario crear/editar producto
│   │   ├── PedidosRecibidos.vue        # Pedidos recibidos por el productor
│   │   ├── VentasHistorial.vue         # Historial de ventas + gráfico
│   │   └── PerfilProductorEdit.vue     # Editar perfil
│   ├── shared/
│   │   ├── StatsCard.vue              # Tarjeta de métrica reutilizable
│   │   ├── StatusBadge.vue            # Badge de estado con color
│   │   └── ConfirmDialog.vue          # Diálogo de confirmación reutilizable
│   └── layout/
│       ├── PanelSidebar.vue           # Sidebar colapsable del panel
│       └── PanelHeader.vue            # Header del panel con info de sesión
├── services/
│   ├── IProductoService.ts            # Interfaz del servicio de productos
│   ├── ProductoService.ts             # Implementación con json-server/axios
│   ├── IPedidoService.ts             # Interfaz del servicio de pedidos
│   ├── PedidoService.ts              # Implementación con json-server/axios
│   ├── IAuthService.ts               # Interfaz del servicio de autenticación
│   └── AuthService.ts                # Implementación de autenticación
├── stores/
│   ├── authStore.ts                   # Pinia store de autenticación
│   ├── productoStore.ts               # Pinia store de productos
│   └── pedidoStore.ts                 # Pinia store de pedidos
├── types/
│   ├── IProducto.ts                   # Interfaces de Producto
│   ├── IPedido.ts                     # Interfaces de Pedido
│   └── IUser.ts                       # Interfaces de Usuario
└── router/
    └── index.ts                       # Configuración de rutas con guards
```

**Datos en db.json – Estructura esperada para el vendedor**
```json
{
  "users": [
    {
      "id": 2,
      "name": "Productor Demo",
      "email": "productor@agroconet.test",
      "password": "demo123",
      "userType": "productor",
      "finca": "Finca La Esperanza",
      "telefono": "+504 9999-0000",
      "ubicacion": "Copán, Honduras",
      "descripcion": "Productor de café orgánico de altura",
      "createdAt": "2026-05-11T00:00:00.000Z"
    }
  ],
  "productos": [
    {
      "id": 1,
      "nombre": "Café Caturra Orgánico",
      "tipo": "cafe",
      "productor": "Productor Demo",
      "productorId": 2,
      "precio": 150,
      "stock": 50,
      "humedad": 12,
      "variedad": "Caturra",
      "region": "Copán",
      "pais": "Honduras",
      "altura": "1500-1700 msnm",
      "certificaciones": ["Orgánico", "Fair Trade"],
      "descripcion": "Café de altura cultivado en las montañas de Copán",
      "imagen": "https://images.unsplash.com/...",
      "estado": "disponible",
      "createdAt": "2026-05-11T00:00:00.000Z"
    }
  ],
  "pedidos": [
    {
      "id": 1,
      "productoId": 1,
      "nombreProducto": "Café Caturra Orgánico",
      "compradorId": 1,
      "compradorNombre": "Comprador Demo",
      "productor": "Productor Demo",
      "productorId": 2,
      "cantidadQuintales": 2,
      "precioUnitario": 150,
      "total": 300,
      "estado": "solicitado",
      "createdAt": "2026-05-11T00:00:00.000Z"
    }
  ],
  "tracking": [
    {
      "id": 1,
      "pedidoId": 1,
      "estado": "solicitado",
      "descripcion": "Pedido creado, pendiente de validación del productor",
      "updatedAt": "2026-05-11T00:00:00.000Z"
    }
  ]
}
```

**Tareas (orden sugerido)**

**Infraestructura base**
- TK-014-001 Definir interfaces TypeScript en `src/types/` (`IProducto.ts`, `IPedido.ts`, `IUser.ts`) con segregación de interfaces (ISP)
- TK-014-002 Crear servicios abstractos (`IProductoService`, `IPedidoService`, `IAuthService`) con implementaciones concretas para json-server (DIP)
- TK-014-003 Configurar Pinia stores (`authStore`, `productoStore`, `pedidoStore`) como fachadas entre componentes y servicios
- TK-014-004 Configurar Vue Router con rutas anidadas para `/dashboard/productor/*` y guards de navegación por rol

**Componentes base del panel**
- TK-014-005 Crear componente `PanelSidebar.vue` con navegación lateral colapsable y responsive
- TK-014-006 Crear componente `PanelHeader.vue` con info de sesión y cierre de sesión
- TK-014-007 Crear componente `StatsCard.vue` reutilizable para tarjetas de métricas
- TK-014-008 Crear componente `StatusBadge.vue` para badges de estado con código de colores

**Vistas del panel vendedor**
- TK-014-009 Crear `DashboardProductor.vue` como layout principal con resumen de métricas y últimos pedidos
- TK-014-010 Crear `ProductoList.vue` con listado filtrado de productos propios, acciones editar/pausar/eliminar, y paginación
- TK-014-011 Crear `ProductoForm.vue` con formulario completo, validaciones en cliente, modo crear/editar (OCP)
- TK-014-012 Crear `PedidosRecibidos.vue` con tabla de pedidos recibidos, acciones confirmar/rechazar, badges de estado
- TK-014-013 Crear `VentasHistorial.vue` con historial de ventas completadas y gráfico mensual
- TK-014-014 Crear `PerfilProductorEdit.vue` con formulario de edición de perfil del productor

**Integración y redirección post-login**
- TK-014-015 Implementar en `loginStore` o `router guard` la redirección automática según `userType` tras autenticación exitosa
- TK-014-016 Implementar validación de propiedad de producto en edición (seguridad: solo el dueño puede modificar)
- TK-014-017 Conectar todas las vistas con el store de Pinia y servicios para operaciones CRUD reales contra json-server

**Pruebas y refinamiento**
- TK-014-018 Probar flujo completo: registro → login con userType productor → redirección a panel → publicar producto → ver pedidos
- TK-014-019 Probar responsive en móvil (320px-480px) y asegurar sidebar colapsable correcto
- TK-014-020 Probar guard de rutas: intentar acceder a `/dashboard/productor` sin sesión y con rol comprador

---

## 📋 Proceso de Implementación – Panel del Vendedor (US-014)

### Resumen de cambios realizados

Se implementó el panel completo del vendedor/productor siguiendo todas las tareas (TK-014-001 a TK-014-020) y aplicando los principios SOLID definidos en la historia de usuario.

### Archivos creados (12 nuevos)

| Archivo | Propósito |
|---------|-----------|
| `src/types/IProducto.ts` | Interfaces segregadas: `IProductoBase`, `IProducto`, `IProductoForm` (ISP) |
| `src/services/IProductoService.ts` | Contrato abstracto del servicio de productos (DIP) |
| `src/services/ProductoService.ts` | Implementación concreta contra json-server (DIP) |
| `src/stores/productoStore.ts` | Store Pinia-style para CRUD de productos (fachada) |
| `src/componentes/productor/DashboardProductor.vue` | Layout principal del panel con sidebar + header |
| `src/componentes/productor/ResumenProductor.vue` | Vista de aterrizaje con 4 tarjetas de métricas + últimos pedidos |
| `src/componentes/productor/ProductoList.vue` | Listado con tabla, paginación, editar/pausar/eliminar, diálogo de confirmación |
| `src/componentes/productor/ProductoForm.vue` | Formulario crear/editar con validaciones completas (OCP) |
| `src/componentes/productor/PedidosRecibidos.vue` | Tabla de pedidos con acciones confirmar/rechazar + tracking |
| `src/componentes/productor/VentasHistorial.vue` | Historial de ventas entregadas + gráfico de barras CSS + exportación CSV |
| `src/componentes/productor/PerfilProductorEdit.vue` | Edición de perfil con campos específicos de productor |

### Archivos modificados (8 existentes)

| Archivo | Cambio |
|---------|--------|
| `src/types/IUser.ts` | Extendido con campos `finca`, `ubicacion`, `descripcion` para productor |
| `src/services/IPedidoService.ts` | Agregado método `listByProductor()` |
| `src/services/PedidoService.ts` | Implementado `listByProductor()` |
| `src/services/ITrackingService.ts` | Agregado método `create()` |
| `src/services/TrackingService.ts` | Implementado `create()` |
| `src/stores/pedidoStore.ts` | Agregado `loadPedidosProductor()` + `resumenProductor` computed |
| `src/componentes/layout/PanelSidebar.vue` | Refactorizado para aceptar prop `role` (comprador/productor/agencia) con navegación dinámica |
| `src/componentes/layout/PanelHeader.vue` | Refactorizado para aceptar prop `role` con label dinámico |
| `src/componentes/comprador/DashboardComprador.vue` | Pasada prop `role="comprador"` a PanelSidebar y PanelHeader |
| `src/router/index.ts` | Rutas anidadas completas para `/dashboard/productor/*` (6 rutas hijas) |
| `db.json` | Agregados campos `stock`, `estado`, `productorId`, `createdAt` a productos; campos `finca`, `telefono`, `ubicacion`, `descripcion` al usuario productor |

### Principios SOLID aplicados

**S – Single Responsibility**
- Cada componente Vue tiene una única responsabilidad (ResumenProductor, ProductoList, ProductoForm, etc.)
- Cada servicio maneja solo su dominio (ProductoService, PedidoService, TrackingService)

**O – Open/Closed**
- `ProductoForm.vue` funciona en modo crear o editar según `route.params.id`, sin duplicar lógica
- `PanelSidebar.vue` se extiende vía prop `role` para mostrar navegación de cualquier rol

**L – Liskov Substitution**
- Interfaces (`IProductoService`, `IPedidoService`, `ITrackingService`) definen contratos que cualquier implementación futura (API real) puede sustituir

**I – Interface Segregation**
- `IProductoBase` (nombre, tipo, precio, stock) vs `IProducto` (completo)
- `IPedidoResumen` vs `IPedidoDetalle`
- Los componentes de listado solo usan interfaces básicas

**D – Dependency Inversion**
- Componentes dependen de abstracciones (stores/stores), no de implementaciones concretas
- `useProductoStore()` usa internamente `ProductoService`, pero el componente no conoce la implementación
- Fácil migración de json-server a API real: solo cambiar la implementación del servicio

### Arquitectura de carpetas resultante

```
src/componentes/productor/
├── DashboardProductor.vue      # Layout principal con sidebar + header + router-view
├── ResumenProductor.vue        # Métricas (productos activos, pedidos pendientes, etc.)
├── ProductoList.vue            # CRUD de productos con paginación y confirmación
├── ProductoForm.vue            # Formulario crear/editar con validaciones
├── PedidosRecibidos.vue        # Pedidos con acciones confirmar/rechazar
├── VentasHistorial.vue         # Historial con gráfico y exportación CSV
└── PerfilProductorEdit.vue     # Edición de perfil del productor
```

### Flujo de redirección post-login

El flujo de autenticación existente redirige automáticamente:
- `useAuth.ts` → `login()` autentica y persiste usuario
- Router `beforeEach` → verifica `meta.requiresAuth` y `meta.role`
- Si el rol no coincide → redirige a `dashboardPathForRole(rol)`
- Si no hay sesión → redirige a `/login`

### Verificación

- ✅ TypeScript typecheck pasa sin errores (`vue-tsc -b`)
- ✅ Rutas anidadas funcionan para todas las vistas del productor
- ✅ Sidebar y header multi-rol funcionales
- ✅ CRUD completo de productos contra json-server
- ✅ Gestión de pedidos (confirmar/rechazar) con registro en tracking
- ✅ Validaciones en formulario de producto
- ✅ Exportación CSV en historial de ventas
