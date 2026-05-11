
---
### Historia de Usuario US-015
**Panel del Comprador – Dashboard personal con gestión de pedidos y favoritos**
**Como** comprador (tostador, molino, supermercado, exportador, consumidor premium)
**Quiero** acceder a un panel personal exclusivo para compradores después de iniciar sesión
**Para** gestionar mis pedidos, dar seguimiento a compras, guardar productos favoritos, y administrar mi perfil

**Criterios de Aceptación**

**Escenario 1: Redirección post-login según userType**
Dado que un usuario completa el registro o inicio de sesión exitosamente
Cuando el sistema valida sus credenciales contra `db.json` (`/users`)
Entonces:
- Si `userType === "comprador"`, redirige automáticamente a `/dashboard/comprador`
- Si `userType === "productor"`, redirige automáticamente a `/dashboard/productor`
- Si `userType === "agencia"`, redirige automáticamente a `/dashboard/agencia`
- La redirección se implementa en el guard de Vue Router (`beforeEach`) o en el store de autenticación
- Se valida que el token/sesión exista antes de permitir el acceso a cualquier ruta `/dashboard/*`

**Escenario 2: Barra de navegación superior del panel**
Dado que el comprador ingresa al dashboard
Cuando se renderiza la vista
Entonces:
- Logo de AgroConet (enlace a Home)
- Indicador visual del rol activo: "Comprador" con badge/icono
- Menú de navegación lateral (sidebar) colapsable con:
  - "Resumen" → `/dashboard/comprador`
  - "Mis Pedidos" → `/dashboard/comprador/pedidos`
  - "Productos Favoritos" → `/dashboard/comprador/favoritos`
  - "Catálogo" → `/catalogo` (abre fuera del panel en nueva pestaña o navegación)
  - "Mi Perfil" → `/dashboard/comprador/perfil`
- Botón de "Cerrar sesión" que limpia la sesión y redirige a Home
- En móvil: sidebar se oculta y se muestra menú hamburguesa; el panel usa 100% del ancho

**Escenario 3: Resumen / Dashboard principal (vista de aterrizaje)**
Dado que el comprador accede a `/dashboard/comprador`
Cuando se carga la vista principal del panel
Entonces se muestran 4 tarjetas de resumen en grid (responsive: 2 columnas en tablet, 1 en móvil):
- Tarjeta 1 – "Pedidos Activos": número de pedidos con estado `solicitado`, `confirmado` o `en tránsito`
- Tarjeta 2 – "Pedidos Entregados": número de pedidos con estado `entregado` en los últimos 30 días
- Tarjeta 3 – "Total Invertido": suma de totales de todos los pedidos (moneda local)
- Tarjeta 4 – "Favoritos Guardados": número de productos marcados como favoritos
Debajo del resumen: tabla con los últimos 5 pedidos (más recientes primero) con columnas: Producto, Productor, Cantidad, Total, Estado (badge colorido), Acción "Ver detalle" y "Ver Tracking"

**Escenario 4: Listado de pedidos del comprador con filtros y búsqueda**
Dado que el comprador navega a "Mis Pedidos"
Cuando se carga la lista completa de pedidos
Entonces:
- Filtra pedidos donde `compradorId === usuarioAutenticado.id`
- Tabla con columnas: ID Pedido, Producto, Productor, Cantidad (Qq), Precio Unitario, Total, Fecha de solicitud, Estado (badge colorido)
- Filtros disponibles:
  - Por estado: Todos, Solicitado, Confirmado, En tránsito, Entregado, Rechazado
  - Por rango de fechas (selector de fecha inicio/fin)
  - Búsqueda por nombre de producto o productor (campo de texto)
- Acciones por fila:
  - "Ver Detalle" → modal o redirección a `/detalle-pedido/:id`
  - "Ver Tracking" → modal o redirección a `/tracking/:id`
  - "Contactar Productor" → enlace WhatsApp con número del productor
- Pedidos con estado `solicitado` muestran indicador visual "Pendiente de confirmación"
- Paginación de 10 pedidos por página
- Opción "Descargar reporte CSV" con los pedidos filtrados actualmente

**Escenario 5: Detalle de pedido desde el panel**
Dado que el comprador hace clic en "Ver Detalle" en un pedido
Cuando se abre la vista de detalle
Entonces:
- Información completa del pedido:
  - Encabezado: ID Pedido, Fecha de solicitud, Estado actual con badge
  - Datos del producto: nombre, tipo, variedad, certificaciones
  - Datos de la transacción: cantidad, precio unitario, subtotal, impuestos (si aplica), total final
  - Datos del productor: nombre, finca, ubicación, calificación, botón "Ver perfil del productor"
  - Timeline de tracking: historial completo de cambios de estado con fechas
- Botones de acción contextuales:
  - Si `estado === "solicitado"`: botón "Cancelar Pedido" (cambia estado a `cancelado`)
  - Si `estado === "confirmado"` o superior: botón "Solicitar Soporte" (abre formulario de contacto)

**Escenario 6: Tracking visual del pedido**
Dado que el comprador hace clic en "Ver Tracking"
Cuando se abre la vista de tracking
Entonces:
- Timeline vertical (o horizontal en desktop) con todos los estados del pedido:
  - `solicitado` → "Pedido creado" (check verde si completado)
  - `confirmado` → "Confirmado por el productor" (check verde si completado)
  - `en puerto` → "En puerto de origen" (check verde si completado)
  - `en tránsito` → "En tránsito" (check verde si completado)
  - `entregado` → "Entregado" (check verde si completado)
- Cada estado muestra: nombre, descripción, fecha y hora de actualización
- El estado actual se resalta con un indicador animado (punto pulsante)
- Los estados futuros (no alcanzados) se muestran en gris
- Si el estado es `rechazado` o `cancelado`, se muestra el timeline hasta ese punto y el resto en rojo/gris con mensaje explicativo
- Información adicional: datos de la agencia exportadora asignada (nombre, contacto) si aplica

**Escenario 7: Gestión de productos favoritos**
Dado que el comprador navega a "Productos Favoritos"
Cuando se carga la vista
Entonces:
- Grid de tarjetas (responsive: 3 columnas desktop, 2 tablet, 1 móvil) con productos marcados como favoritos
- Cada tarjeta muestra: imagen, nombre, precio por quintal, productor, región, certificaciones
- Botón "Quitar de favoritos" (corazón lleno que al hacer clic se vacía y desaparece la tarjeta con animación)
- Botón "Hacer pedido" → redirige a `/producto/:id` o abre modal de pedido rápido
- Si no hay favoritos: mensaje amigable "Aún no tienes productos favoritos. Explora el catálogo y guarda tus productos preferidos." con botón "Ir al catálogo"
- Los favoritos se almacenan en `db.json` bajo la colección `favoritos` con `{ id, compradorId, productoId, createdAt }`

**Escenario 8: Perfil del comprador (configuración)**
Dado que el comprador navega a "Mi Perfil"
Cuando se carga la vista
Entonces:
- Datos actuales precargados: nombre (readonly), email (readonly), teléfono, foto de perfil, empresa/organización (si aplica), dirección de envío preferida, país
- Campos editables: teléfono, foto, empresa, dirección de envío, país, preferencias de notificación (checkbox: email, WhatsApp)
- `PATCH /users/:id` al guardar cambios
- Sección "Direcciones de envío": posibilidad de agregar múltiples direcciones (array en el usuario)
- Botón "Cambiar contraseña" (en fase 2 con backend real)

**Escenario 9: Seguridad y control de acceso**
Dado que un usuario no autenticado o con rol diferente intenta acceder a `/dashboard/comprador/*`
Cuando el guard de ruta se ejecuta
Entonces:
- Si no hay sesión activa: redirigir a `/login` con mensaje "Debes iniciar sesión como comprador"
- Si el rol no es `comprador`: redirigir a su dashboard correspondiente con mensaje "No tienes permisos para acceder a esta sección"

**Escenario 10: Notificaciones y alertas contextuales**
Dado que el comprador está en cualquier sección del panel
Cuando ocurre un cambio de estado en uno de sus pedidos (simulado vía polling o refresco manual)
Entonces:
- Badge de notificación en el sidebar con número de pedidos actualizados
- Al hacer clic en el badge, se despliega lista de últimas 5 actualizaciones: "Tu pedido #123 de Café Caturra ha sido confirmado", "Tu pedido #456 de Maíz está en tránsito"
- Las notificaciones se almacenan temporalmente en el store de Pinia y se limpian al leerlas

**Notas Técnicas – Principios SOLID Aplicados**

**S – Single Responsibility Principle (Principio de Responsabilidad Única)**
- Cada componente tendrá una única responsabilidad bien definida:
  - `DashboardComprador.vue` → solo layout y orquestación del panel comprador
  - `PedidoList.vue` → solo listado, filtrado y búsqueda de pedidos
  - `PedidoDetalle.vue` → solo visualización de detalle de pedido
  - `TrackingTimeline.vue` → solo renderizado visual del timeline de tracking
  - `FavoritosList.vue` → solo gestión de productos favoritos
  - `PerfilCompradorEdit.vue` → solo edición de perfil del comprador
- Servicios separados por dominio:
  - `PedidoService.ts` → solo operaciones CRUD de pedidos
  - `FavoritoService.ts` → solo operaciones CRUD de favoritos
  - `TrackingService.ts` → solo consultas de tracking
  - `NotificacionStore.ts` → solo gestión de estado de notificaciones

**O – Open/Closed Principle (Principio Abierto/Cerrado)**
- El componente `PedidoList` aceptará props de configuración (columnas a mostrar, filtros habilitados, acciones disponibles) sin modificar su código interno
- `TrackingTimeline` aceptará un array de estados y renderizará cualquier secuencia, siendo extensible a nuevos estados sin cambios
- Los servicios se extienden vía composición (wrappers), no modificando la implementación base

**L – Liskov Substitution Principle (Principio de Sustitución de Liskov)**
- Interfaces compartidas (`IPedido`, `IProducto`, `IUser`) aseguran que cualquier implementación (json-server hoy, API real mañana) sea intercambiable
- `IFavoritoService` define el contrato y `FavoritoService` lo implementa; un futuro `FavoritoServiceAPI` podría sustituirlo sin cambiar los consumidores

**I – Interface Segregation Principle (Principio de Segregación de Interfaces)**
- Interfaces pequeñas y específicas:
  - `IPedidoResumen` → id, producto, estado, total, fecha
  - `IPedidoDetalle` → extiende IPedidoResumen + tracking, productor, factura
  - `IFavorito` → id, compradorId, productoId, producto (populated)
  - `ITrackingEvento` → estado, descripción, fecha
- `FavoritosList.vue` solo depende de `IFavorito`, no de `IPedidoDetalle`

**D – Dependency Inversion Principle (Principio de Inversión de Dependencias)**
- Los componentes dependen de abstracciones (interfaces/stores), no de implementaciones concretas
- Inyección de dependencias vía Pinia stores y Provide/Inject de Vue 3
- `PedidoService` implementa `IPedidoService`; el store `pedidoStore` usa la interfaz, los componentes usan el store
- Fácil migración de json-server a API real: solo cambiar la implementación del servicio, sin tocar componentes ni stores

**Arquitectura de Carpetas Propuesta**
```
src/
├── components/
│   ├── comprador/
│   │   ├── DashboardComprador.vue      # Layout principal del panel comprador
│   │   ├── PedidoList.vue             # Listado de pedidos con filtros
│   │   ├── PedidoDetalle.vue          # Detalle completo del pedido
│   │   ├── TrackingTimeline.vue       # Timeline visual de tracking
│   │   ├── FavoritosList.vue          # Grid de productos favoritos
│   │   └── PerfilCompradorEdit.vue    # Edición de perfil del comprador
│   ├── shared/
│   │   ├── StatsCard.vue              # Tarjeta de métrica reutilizable
│   │   ├── StatusBadge.vue            # Badge de estado con color
│   │   ├── SearchFilter.vue           # Barra de búsqueda y filtros
│   │   └── Pagination.vue             # Paginación reutilizable
│   └── layout/
│       ├── PanelSidebar.vue           # Sidebar colapsable del panel
│       └── PanelHeader.vue            # Header del panel con info de sesión
├── services/
│   ├── IPedidoService.ts             # Interfaz del servicio de pedidos
│   ├── PedidoService.ts              # Implementación con json-server/axios
│   ├── IFavoritoService.ts           # Interfaz del servicio de favoritos
│   ├── FavoritoService.ts            # Implementación con json-server/axios
│   ├── ITrackingService.ts           # Interfaz del servicio de tracking
│   ├── TrackingService.ts            # Implementación con json-server/axios
│   ├── IAuthService.ts               # Interfaz del servicio de autenticación
│   └── AuthService.ts                # Implementación de autenticación
├── stores/
│   ├── authStore.ts                   # Pinia store de autenticación
│   ├── pedidoStore.ts                 # Pinia store de pedidos
│   ├── favoritoStore.ts              # Pinia store de favoritos
│   └── notificacionStore.ts          # Pinia store de notificaciones
├── types/
│   ├── IPedido.ts                     # Interfaces de Pedido
│   ├── IFavorito.ts                   # Interfaces de Favorito
│   ├── ITracking.ts                   # Interfaces de Tracking
│   └── IUser.ts                       # Interfaces de Usuario
└── router/
    └── index.ts                       # Configuración de rutas con guards
```

**Datos en db.json – Estructura esperada para el comprador**
```json
{
  "users": [
    {
      "id": 1,
      "name": "Comprador Demo",
      "email": "comprador@agroconet.test",
      "password": "demo123",
      "userType": "comprador",
      "telefono": "+504 8888-0000",
      "empresa": "Tostadores del Valle",
      "direccionEnvio": "Tegucigalpa, Honduras",
      "pais": "Honduras",
      "preferenciasNotificacion": { "email": true, "whatsapp": false },
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
      "productor": "Finca La Esperanza",
      "productorId": 2,
      "cantidadQuintales": 2,
      "precioUnitario": 150,
      "total": 300,
      "estado": "solicitado",
      "createdAt": "2026-05-11T00:00:00.000Z"
    }
  ],
  "favoritos": [
    {
      "id": 1,
      "compradorId": 1,
      "productoId": 3,
      "createdAt": "2026-05-11T00:00:00.000Z"
    }
  ],
  "tracking": [
    {
      "id": 1,
      "pedidoId": 1,
      "estado": "solicitado",
      "descripcion": "Pedido creado por el comprador",
      "updatedAt": "2026-05-11T00:00:00.000Z"
    }
  ]
}
```

**Tareas (orden sugerido)**

**Infraestructura base**
- TK-015-001 Definir interfaces TypeScript en `src/types/` (`IPedido.ts`, `IFavorito.ts`, `ITracking.ts`, `IUser.ts`) con segregación de interfaces (ISP)
- TK-015-002 Crear servicios abstractos (`IPedidoService`, `IFavoritoService`, `ITrackingService`, `IAuthService`) con implementaciones para json-server (DIP)
- TK-015-003 Configurar Pinia stores (`pedidoStore`, `favoritoStore`, `notificacionStore`, `authStore`) como fachadas entre componentes y servicios
- TK-015-004 Configurar Vue Router con rutas anidadas para `/dashboard/comprador/*` y guards de navegación por rol

**Componentes base del panel**
- TK-015-005 Crear componente `PanelSidebar.vue` con navegación lateral colapsable, badge de notificaciones, y responsive
- TK-015-006 Crear componente `PanelHeader.vue` con info de sesión, notificaciones y cierre de sesión
- TK-015-007 Crear componente `StatsCard.vue` reutilizable para tarjetas de métricas
- TK-015-008 Crear componente `StatusBadge.vue` para badges de estado con código de colores
- TK-015-009 Crear componente `SearchFilter.vue` con campo de búsqueda y filtros por estado/fechas
- TK-015-010 Crear componente `Pagination.vue` reutilizable con página actual y total de páginas

**Vistas del panel comprador**
- TK-015-011 Crear `DashboardComprador.vue` como layout principal con resumen de métricas (pedidos activos, entregados, total invertido, favoritos) y últimos 5 pedidos
- TK-015-012 Crear `PedidoList.vue` con tabla completa de pedidos, filtros por estado/fechas, búsqueda por texto, paginación, y exportación CSV
- TK-015-013 Crear `PedidoDetalle.vue` con información completa del pedido, datos del productor, timeline de tracking, y acciones contextuales (cancelar, contactar)
- TK-015-014 Crear `TrackingTimeline.vue` con timeline visual vertical/horizontal, estados con iconos, check verde para completados, punto pulsante para actual, gris para futuros
- TK-015-015 Crear `FavoritosList.vue` con grid de productos favoritos, botón quitar, botón hacer pedido, y estado vacío con CTA al catálogo
- TK-015-016 Crear `PerfilCompradorEdit.vue` con formulario de edición de perfil, múltiples direcciones de envío, y preferencias de notificación

**Integración de redirección post-login**
- TK-015-017 Implementar en `authStore` o `router guard` la redirección automática según `userType` tras autenticación exitosa
- TK-015-018 Implementar polling periódico (cada 30 segundos) o badge manual de notificaciones con contador de pedidos actualizados
- TK-015-019 Conectar todas las vistas con los stores de Pinia y servicios para operaciones CRUD contra json-server

**Pruebas y refinamiento**
- TK-015-020 Probar flujo completo: registro → login con userType comprador → redirección a panel → ver resumen → navegar pedidos → ver tracking → gestionar favoritos
- TK-015-021 Probar responsive en móvil (320px-480px) asegurando sidebar colapsable y tablas con scroll horizontal
- TK-015-022 Probar guard de rutas: intentar acceder a `/dashboard/comprador` sin sesión y con rol productor
- TK-015-023 Probar exportación CSV con datos filtrados y verificar que el archivo descargado contiene los datos correctos

---

## Proceso realizado por Codex - 11 de mayo de 2026

### Evaluación inicial

Se revisó esta historia de usuario y se comparó con el estado actual del proyecto. El proyecto ya tenía autenticación mock básica, `useApi`, catálogo, favoritos desde detalle de producto y datos iniciales en `db.json`, pero no existía el dashboard del comprador, rutas protegidas, servicios, stores, componentes de panel, detalle de pedido, tracking visual, filtros, exportación CSV ni edición de perfil.

Como `pinia` no está instalado en el proyecto, se implementaron stores ligeros con `ref/computed` en `src/stores/`. La estructura respeta la función de fachada entre componentes y servicios, y queda preparada para migrarse a Pinia sin reescribir las vistas.

### Tareas implementadas

- TK-015-001: se crearon interfaces TypeScript en `src/types/`:
  - `IUser.ts`
  - `IPedido.ts`
  - `IFavorito.ts`
  - `ITracking.ts`
- TK-015-002: se crearon servicios e interfaces en `src/services/`:
  - `IAuthService.ts` / `AuthService.ts`
  - `IPedidoService.ts` / `PedidoService.ts`
  - `IFavoritoService.ts` / `FavoritoService.ts`
  - `ITrackingService.ts` / `TrackingService.ts`
- TK-015-003: se crearon stores/fachadas en `src/stores/`:
  - `authStore.ts`
  - `pedidoStore.ts`
  - `favoritoStore.ts`
  - `trackingStore.ts`
  - `notificacionStore.ts`
- TK-015-004: se añadieron rutas anidadas bajo `/dashboard/comprador/*` y guards por rol en `src/router/index.ts`.
- TK-015-005: se creó `src/componentes/layout/PanelSidebar.vue` con navegación, cierre de sesión, responsive y badge de notificaciones.
- TK-015-006: se creó `src/componentes/layout/PanelHeader.vue` con sesión y notificaciones.
- TK-015-007: se creó `src/componentes/shared/StatsCard.vue`.
- TK-015-008: se creó `src/componentes/shared/StatusBadge.vue`.
- TK-015-009: se creó `src/componentes/shared/SearchFilter.vue`.
- TK-015-010: se creó `src/componentes/shared/Pagination.vue`.
- TK-015-011: se creó `src/componentes/comprador/DashboardComprador.vue` como layout y `ResumenComprador.vue` como vista resumen.
- TK-015-012: se creó `src/componentes/comprador/PedidoList.vue` con filtros, búsqueda, paginación y exportación CSV.
- TK-015-013: se creó `src/componentes/comprador/PedidoDetalle.vue` con detalle, productor, transacción, tracking y acción de cancelar.
- TK-015-014: se creó `src/componentes/comprador/TrackingTimeline.vue`.
- TK-015-015: se creó `src/componentes/comprador/FavoritosList.vue`.
- TK-015-016: se creó `src/componentes/comprador/PerfilCompradorEdit.vue` con `PATCH /users/:id`.
- TK-015-017: se actualizó `useAuth.ts`, `Login.vue` y `Registro.vue` para redirigir por `userType`.
- TK-015-018: se implementó badge de notificaciones basado en pedidos con estados actualizados.
- TK-015-019: las vistas se conectaron a stores y servicios contra `json-server`.
- TK-015-020 a TK-015-023: se validó compilación con `typecheck` y `build`. Las pruebas manuales visuales/responsive quedan pendientes para navegador real.

### Rutas añadidas

- `/dashboard/comprador`
- `/dashboard/comprador/pedidos`
- `/dashboard/comprador/pedidos/:id`
- `/dashboard/comprador/tracking/:id`
- `/dashboard/comprador/favoritos`
- `/dashboard/comprador/perfil`
- `/dashboard/productor` y `/dashboard/agencia` como placeholders protegidos para respetar la redirección por rol.

### Datos mock actualizados

Se amplió `db.json` para incluir:

- Perfil de comprador con teléfono, empresa, país, direcciones y preferencias.
- Pedidos con `nombreProducto`, `compradorNombre`, datos del productor, agencia, tipo, variedad, certificaciones e impuestos.
- Favoritos con `{ id, compradorId, productoId, createdAt }`.
- Tracking con varios eventos por pedido.

También se ajustó `useMarketplaceActions.ts` para crear pedidos con `nombreProducto` y favoritos con `compradorId`.

### Principios SOLID aplicados

- Responsabilidad única: los componentes de UI no contienen llamadas HTTP directas; los servicios consultan API, los stores coordinan estado y los componentes renderizan.
- Abierto/cerrado: `TrackingTimeline.vue` renderiza estados desde una lista configurable y puede ampliarse sin tocar consumidores.
- Sustitución de dependencias: los componentes consumen stores y servicios, no detalles de `axios` o `json-server`.
- Segregación de interfaces: se separaron tipos de usuario, pedido, favorito y tracking en archivos pequeños.
- Inversión de dependencias: los componentes dependen de fachadas (`stores`) y estas de contratos de servicio, facilitando migrar a API real.

### Verificaciones ejecutadas

- `npm run typecheck`: correcto.
- `npm run build`: correcto.

### Pendientes reales

- Instalar y migrar los stores ligeros a Pinia si el proyecto decide usar Pinia formalmente.
- Validar visualmente responsive en navegador real, especialmente tablas en 320px-480px.
- Añadir tests automatizados para servicios, stores y guards.
- Conectar notificaciones a polling real o backend de eventos; ahora se derivan de pedidos cargados.
- Completar dashboards de productor y agencia, que actualmente son placeholders protegidos.
