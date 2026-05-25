# ESPECIFICACIÓN TÉCNICA DEL BACKEND - AgroConet

## Stack Recomendado
python +flask

PostgreSQL
JWT para autenticación
bcrypt para hashing de contraseñas
pytest para pruebas

---

## 1. ENTIDADES DE BASE DE DATOS (8 tablas)

### 1.1 User
Representa los 3 roles del sistema.

| Campo | Tipo | Restricciones |
|---|---|---|
| id | UUID/PK | auto-generado |
| name | VARCHAR(150) | NOT NULL |
| email | VARCHAR(255) | NOT NULL, UNIQUE, lowercase |
| password | VARCHAR(255) | NOT NULL (bcrypt hash) |
| userType | ENUM('comprador','productor','agencia') | NOT NULL |
| telefono | VARCHAR(20) | nullable |
| fotoPerfil | TEXT | nullable (URL) |
| empresa | VARCHAR(200) | nullable |
| direccionEnvio | TEXT | nullable |
| direccionesEnvio | JSONB/TEXT[] | nullable |
| pais | VARCHAR(100) | nullable |
| preferenciasNotificacion | JSONB `{email:boolean, whatsapp:boolean}` | default {"email":true,"whatsapp":false} |
| finca | VARCHAR(200) | nullable (solo productor) |
| ubicacion | VARCHAR(200) | nullable (solo productor) |
| descripcion | TEXT | nullable (solo productor) |
| refreshToken | TEXT | nullable (para JWT refresh) |
| createdAt | TIMESTAMP | NOT NULL, default now() |
| updatedAt | TIMESTAMP | NOT NULL, auto-update |

### 1.2 Producto
Catálogo de productos agrícolas publicados por productores.

| Campo | Tipo | Restricciones |
|---|---|---|
| id | UUID/PK | auto-generado |
| nombre | VARCHAR(200) | NOT NULL |
| tipo | ENUM('cafe','maiz','frijol','arroz','otros') | NOT NULL |
| precio | DECIMAL(10,2) | NOT NULL, >= 0 |
| stock | INTEGER | NOT NULL, >= 0 |
| estado | ENUM('disponible','agotado','pausado') | NOT NULL, default 'disponible' |
| productor | VARCHAR(200) | NOT NULL (nombre del productor) |
| productorId | UUID/FK → User.id | NOT NULL |
| humedad | DECIMAL(5,2) | nullable |
| variedad | VARCHAR(100) | nullable |
| region | VARCHAR(100) | nullable |
| pais | VARCHAR(100) | nullable |
| altura | VARCHAR(50) | nullable |
| certificaciones | JSONB/TEXT[] | nullable (ej: ["Orgánico","Fair Trade"]) |
| descripcion | TEXT | nullable |
| imagen | TEXT | nullable (URL) |
| lat | DECIMAL(10,7) | nullable (para clima) |
| lon | DECIMAL(10,7) | nullable (para clima) |
| createdAt | TIMESTAMP | NOT NULL, default now() |
| updatedAt | TIMESTAMP | NOT NULL, auto-update |

### 1.3 Pedido
Órdenes de compra creadas por compradores.

| Campo | Tipo | Restricciones |
|---|---|---|
| id | UUID/PK | auto-generado |
| productoId | UUID/FK → Producto.id | NOT NULL |
| nombreProducto | VARCHAR(200) | NOT NULL (copia del producto al momento del pedido) |
| compradorId | UUID/FK → User.id | NOT NULL |
| compradorNombre | VARCHAR(150) | NOT NULL |
| productor | VARCHAR(200) | NOT NULL |
| productorId | UUID/FK → User.id | nullable |
| productorTelefono | VARCHAR(20) | nullable |
| productorUbicacion | VARCHAR(200) | nullable |
| productorCalificacion | DECIMAL(3,2) | nullable |
| agenciaNombre | VARCHAR(200) | nullable (nombre de la agencia asignada) |
| agenciaContacto | VARCHAR(200) | nullable |
| agenciaId | UUID/FK → User.id | nullable |
| cantidadQuintales | INTEGER | NOT NULL, > 0 |
| precioUnitario | DECIMAL(10,2) | NOT NULL |
| total | DECIMAL(12,2) | NOT NULL (cantidad * precioUnitario) |
| impuestos | DECIMAL(10,2) | default 0 |
| tipo | VARCHAR(50) | nullable (copia del tipo de producto) |
| variedad | VARCHAR(100) | nullable |
| certificaciones | JSONB/TEXT[] | nullable |
| estado | ENUM('solicitado','confirmado','en puerto','en tránsito','entregado','rechazado','cancelado') | NOT NULL, default 'solicitado' |
| notas | TEXT | nullable |
| createdAt | TIMESTAMP | NOT NULL, default now() |
| updatedAt | TIMESTAMP | NOT NULL, auto-update |

### 1.4 TrackingEvento
Historial de cambios de estado de cada pedido.

| Campo | Tipo | Restricciones |
|---|---|---|
| id | UUID/PK | auto-generado |
| pedidoId | UUID/FK → Pedido.id | NOT NULL |
| estado | ENUM(estados de Pedido) | NOT NULL |
| descripcion | TEXT | NOT NULL |
| actualizadoPor | UUID/FK → User.id | nullable (quién hizo el cambio) |
| createdAt | TIMESTAMP | NOT NULL, default now() |

### 1.5 Favorito
Productos guardados por compradores.

| Campo | Tipo | Restricciones |
|---|---|---|
| id | UUID/PK | auto-generado |
| compradorId | UUID/FK → User.id | NOT NULL |
| productoId | UUID/FK → Producto.id | NOT NULL |
| createdAt | TIMESTAMP | NOT NULL, default now() |

**Unique constraint:** (compradorId, productoId)

### 1.6 Contacto
Mensajes de contacto entre comprador y productor.

| Campo | Tipo | Restricciones |
|---|---|---|
| id | UUID/PK | auto-generado |
| productoId | UUID/FK → Producto.id | nullable |
| usuarioId | UUID/FK → User.id | NOT NULL |
| productorNombre | VARCHAR(200) | NOT NULL |
| mensaje | TEXT | NOT NULL |
| estado | ENUM('pendiente','leido','respondido','cerrado') | NOT NULL, default 'pendiente' |
| createdAt | TIMESTAMP | NOT NULL, default now() |
| updatedAt | TIMESTAMP | NOT NULL, auto-update |

### 1.7 MensajeContacto
Formulario de contacto general (visitantes).

| Campo | Tipo | Restricciones |
|---|---|---|
| id | UUID/PK | auto-generado |
| nombre | VARCHAR(150) | NOT NULL |
| email | VARCHAR(255) | NOT NULL |
| telefono | VARCHAR(20) | nullable |
| asunto | VARCHAR(200) | NOT NULL |
| mensaje | TEXT | NOT NULL |
| estado | ENUM('nuevo','leido','respondido') | NOT NULL, default 'nuevo' |
| createdAt | TIMESTAMP | NOT NULL, default now() |

### 1.8 Notificacion (opcional para futuro)
Notificaciones push/in-app para usuarios.

| Campo | Tipo | Restricciones |
|---|---|---|
| id | UUID/PK | auto-generado |
| usuarioId | UUID/FK → User.id | NOT NULL |
| titulo | VARCHAR(200) | NOT NULL |
| mensaje | TEXT | NOT NULL |
| tipo | ENUM('pedido','tracking','mensaje','sistema') | NOT NULL |
| referenciaId | VARCHAR(50) | nullable (ID del pedido relacionado) |
| leida | BOOLEAN | default false |
| createdAt | TIMESTAMP | NOT NULL, default now() |

---

## 2. DIAGRAMA DE RELACIONES

```
User (1) ────< Producto (N)      # User es productor de N productos
User (1) ────< Pedido (N)        # User es comprador de N pedidos (compradorId)
User (1) ────< Pedido (N)        # User es productor de N pedidos (productorId)
User (1) ────< Pedido (N)        # User es agencia asignada (agenciaId)
User (1) ────< Favorito (N)      # User es comprador de N favoritos
User (1) ────< Contacto (N)      # User envía N contactos
User (1) ────< Notificacion (N)  # User recibe N notificaciones
User (1) ────< TrackingEvento (N) # User actualiza N eventos

Producto (1) ──< Pedido (N)      # Producto aparece en N pedidos
Producto (1) ──< Favorito (N)    # Producto es favorito de N compradores

Pedido (1) ────< TrackingEvento (N)  # Pedido tiene N eventos de tracking
```

---

## 3. API ENDPOINTS COMPLETOS

### 3.1 Autenticación

#### POST /api/auth/register
Registrar nuevo usuario.
```json
// Request
{
  "name": "Juan Pérez",
  "email": "juan@email.com",
  "password": "MiPass123!",
  "userType": "productor"
}
// Response 201
{
  "user": {
    "id": "uuid",
    "name": "Juan Pérez",
    "email": "juan@email.com",
    "userType": "productor"
  },
  "accessToken": "jwt...",
  "refreshToken": "jwt..."
}
```

#### POST /api/auth/login
Iniciar sesión.
```json
// Request
{
  "email": "juan@email.com",
  "password": "MiPass123!"
}
// Response 200
{
  "user": {
    "id": "uuid",
    "name": "Juan Pérez",
    "email": "juan@email.com",
    "userType": "productor"
  },
  "accessToken": "jwt...",
  "refreshToken": "jwt..."
}
```

#### POST /api/auth/refresh
Renovar access token.
```json
// Request
{ "refreshToken": "jwt..." }
// Response 200
{
  "accessToken": "jwt...",
  "refreshToken": "jwt..."
}
```

#### POST /api/auth/logout
Invalidar refresh token.
```json
// Request
{ "refreshToken": "jwt..." }
// Response 204
```

### 3.2 Usuarios (requiere auth)

#### GET /api/users/me
Perfil del usuario autenticado. Response 200: `IUser`

#### PATCH /api/users/me
Actualizar perfil propio.
```json
// Request (parcial)
{
  "name": "Nuevo Nombre",
  "telefono": "+504 9999-0000",
  "finca": "Finca La Esperanza",
  "ubicacion": "Copán, Honduras",
  "direccionesEnvio": ["Tegucigalpa", "San Pedro Sula"]
}
// Response 200: IUser actualizado
```

#### PATCH /api/users/me/password
Cambiar contraseña.
```json
// Request
{
  "currentPassword": "old123",
  "newPassword": "new456!"
}
// Response 200: { message: "Contraseña actualizada" }
```

### 3.3 Productos

#### GET /api/productos
Listar productos (público).
```
Query params:
  ?tipo=cafe
  &region=Copán
  &pais=Honduras
  &precioMin=50
  &precioMax=200
  &certificaciones=Orgánico,Fair Trade
  &busqueda=texto (busca en nombre, región, variedad, país)
  &estado=disponible
  &productorId=uuid
  &sort=precio:asc|createdAt:desc
  &page=1
  &limit=20
Response 200:
{
  "data": IProducto[],
  "meta": { "total": 50, "page": 1, "limit": 20, "totalPages": 3 }
}
```

#### GET /api/productos/:id
Detalle de producto (público). Response 200: `IProducto`

#### POST /api/productos
Crear producto (rol: productor).
```json
// Request
{
  "nombre": "Café Caturra Orgánico",
  "tipo": "cafe",
  "precio": 150,
  "stock": 50,
  "humedad": 12,
  "variedad": "Caturra",
  "region": "Copán",
  "pais": "Honduras",
  "altura": "1500-1700 msnm",
  "certificaciones": ["Orgánico", "Fair Trade"],
  "descripcion": "Café de altura...",
  "imagen": "https://...",
  "lat": 14.9167,
  "lon": -88.8833
}
// Response 201: IProducto (productor y productorId se toman del token JWT)
```

#### PATCH /api/productos/:id
Actualizar producto (rol: productor, solo productos propios).
Response 200: `IProducto` actualizado

#### DELETE /api/productos/:id
Eliminar producto (rol: productor, solo productos propios). Response 204

### 3.4 Pedidos (requiere auth)

#### GET /api/pedidos
Listar pedidos del usuario autenticado.
```
Query params:
  ?rol=comprador (filtra por compradorId = currentUser.id)
  &rol=productor (filtra por productorId = currentUser.id)
  &rol=agencia   (filtra por agenciaId = currentUser.id)
  &estado=solicitado
  &fechaInicio=2026-01-01
  &fechaFin=2026-12-31
  &busqueda=texto (busca en nombreProducto, productor)
  &page=1
  &limit=20
Response 200:
{
  "data": IPedidoDetalle[],
  "meta": { "total": 10, "page": 1, "limit": 20, "totalPages": 1 }
}
```

#### GET /api/pedidos/:id
Detalle de pedido. Response 200: `IPedidoDetalle`

#### POST /api/pedidos
Crear pedido (rol: comprador).
```json
// Request
{
  "productoId": "uuid",
  "cantidadQuintales": 2
}
// Backend auto-completa: nombreProducto, compradorNombre, productor, productorId,
// precioUnitario, total, estado: "solicitado", createdAt
// También crea el primer TrackingEvento automáticamente
// Response 201: IPedidoDetalle
```

#### PATCH /api/pedidos/:id/estado
Actualizar estado del pedido.
```json
// Request
{ "estado": "confirmado" }
// Response 200: IPedidoDetalle
// Backend crea automáticamente un TrackingEvento con el nuevo estado
// Roles permitidos según el estado:
//   solicitado → confirmado/rechazado (productor)
//   confirmado → en puerto (agencia)
//   en puerto → en tránsito (agencia)
//   en tránsito → entregado (agencia/comprador)
//   cualquier estado → cancelado (comprador o productor)
```

#### DELETE /api/pedidos/:id
Cancelar pedido (solo si estado = 'solicitado' y es el comprador). Response 204

### 3.5 Tracking (requiere auth)

#### GET /api/pedidos/:pedidoId/tracking
Historial de tracking de un pedido.
```
Query params: ?sort=createdAt:asc
Response 200: ITrackingEvento[]
```

#### POST /api/pedidos/:pedidoId/tracking
Agregar evento manual de tracking (rol: agencia/productor).
```json
// Request
{
  "estado": "en puerto",
  "descripcion": "Producto llegó al puerto de San Lorenzo"
}
// Response 201: ITrackingEvento
```

### 3.6 Favoritos (requiere auth, rol: comprador)

#### GET /api/favoritos
Listar favoritos del comprador autenticado.
Response 200: `IFavoritoDetalle[]` (cada uno con `producto` embebido)

#### POST /api/favoritos
Agregar favorito.
```json
// Request
{ "productoId": "uuid" }
// Response 201: IFavorito
```

#### DELETE /api/favoritos/:id
Quitar favorito. Response 204

### 3.7 Contactos (requiere auth)

#### GET /api/contactos
Listar conversaciones del usuario (rol: comprador ve los que envió, productor ve los que recibió).
Response 200: `Contacto[]`

#### POST /api/contactos
Enviar mensaje a productor.
```json
// Request
{
  "productoId": "uuid",
  "productor": "Nombre Productor",
  "mensaje": "Estoy interesado en tu café"
}
// Response 201: Contacto
```

### 3.8 Mensajes de Contacto (público)

#### POST /api/contacto-general
Formulario de contacto para visitantes.
```json
// Request
{
  "nombre": "Carlos López",
  "email": "carlos@email.com",
  "telefono": "+504 8888-7777",
  "asunto": "Consulta sobre precios",
  "mensaje": "Quiero información sobre..."
}
// Response 201: { message: "Mensaje recibido" }
```

### 3.9 Dashboard/Estadísticas (requiere auth)

#### GET /api/dashboard/resumen
Resumen para el dashboard del usuario según su rol.

**Comprador:**
```json
{
  "activos": 3,
  "entregados30": 5,
  "totalInvertido": 12500.00,
  "favoritosCount": 4
}
```

**Productor:**
```json
{
  "pedidosPendientes": 2,
  "totalVendidoQq": 150,
  "ingresosEstimados": 22500.00,
  "productosActivos": 8
}
```

**Agencia:**
```json
{
  "pedidosAsignados": 5,
  "pedidosEnTransito": 3,
  "pedidosEntregadosMes": 7
}
```

---

## 4. ESTRUCTURA DE CARPETAS SUGERIDA (Backend)

```
backend/
├── prisma/
│   └── schema.prisma          # Modelo de datos
├── src/
│   ├── config/
│   │   ├── database.ts        # Conexión a BD
│   │   ├── auth.ts            # Config JWT
│   │   └── env.ts             # Variables de entorno
│   ├── middleware/
│   │   ├── auth.ts            # Verificar JWT
│   │   ├── authorize.ts       # Verificar rol
│   │   └── validate.ts        # Validar schemas
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── auth.controller.ts
│   │   │   ├── auth.service.ts
│   │   │   └── auth.schema.ts  # Zod/class-validator
│   │   ├── users/
│   │   │   ├── users.controller.ts
│   │   │   ├── users.service.ts
│   │   │   └── users.schema.ts
│   │   ├── productos/
│   │   ├── pedidos/
│   │   ├── tracking/
│   │   ├── favoritos/
│   │   ├── contactos/
│   │   └── dashboard/
│   ├── shared/
│   │   ├── types/
│   │   │   └── index.ts        # Interfaces compartidas
│   │   └── utils/
│   │       ├── pagination.ts
│   │       └── errors.ts
│   ├── app.ts                  # Express app setup
│   └── server.ts               # Entry point
├── tests/
│   ├── auth.test.ts
│   ├── productos.test.ts
│   └── pedidos.test.ts
├── .env.example
├── package.json
└── tsconfig.json
```

---

## 5. REGLAS DE NEGOCIO

1. **Registro:** El email debe ser único (case-insensitive). La contraseña se almacena hasheada con bcrypt.
2. **Login:** Retorna accessToken (corta duración: 15min) + refreshToken (larga duración: 7 días).
3. **Productos:** Solo usuarios con rol `productor` pueden crear/editar/eliminar. Solo pueden modificar sus propios productos.
4. **Pedidos:** Solo `comprador` puede crear. El precio y total se calculan del producto al momento de crear el pedido.
5. **Estados de pedido:** Cada cambio de estado crea automáticamente un TrackingEvento. El flujo es unidireccional (no se puede regresar a un estado anterior).
6. **Tracking:** La línea de tiempo se construye ordenando TrackingEvento por createdAt ASC.
7. **Favoritos:** Par (compradorId, productoId) debe ser único. Solo usuarios `comprador` pueden gestionar favoritos.
8. **Contactos:** Mensajes entre comprador y productor vinculados a un producto.
9. **Dashboard:** Los resúmenes se calculan en base a los pedidos del usuario según su rol.
10. **Pagínación:** Todos los endpoints de listas deben soportar paginación con `page` y `limit`.

---

## 6. MAPEO COMPLETO FRONTEND → BACKEND

| Acción Frontend | Archivo Frontend | Endpoint Backend | Método |
|---|---|---|---|
| Login | `componentes/Login.vue` | `/api/auth/login` | POST |
| Registro | `componentes/Registro.vue` | `/api/auth/register` | POST |
| Cargar catálogo | `useCatalogoProductos.ts` | `/api/productos` | GET |
| Cargar destacados | `useProductos.ts` | `/api/productos?limit=4&estado=disponible` | GET |
| Detalle producto | `DetalleProducto.vue` | `/api/productos/:id` | GET |
| Hacer pedido | `useMarketplaceActions.ts` | `/api/pedidos` | POST |
| Contactar productor | `useMarketplaceActions.ts` | `/api/contactos` | POST |
| Toggle favorito | `useMarketplaceActions.ts` | `/api/favoritos` | POST/DELETE |
| Enviar mensaje contacto | `Contacto.vue` | `/api/contacto-general` | POST |
| Cargar pedidos comprador | `pedidoStore.ts` | `/api/pedidos?rol=comprador` | GET |
| Cargar pedidos productor | `pedidoStore.ts` | `/api/pedidos?rol=productor` | GET |
| Cargar pedido individual | `pedidoStore.ts` | `/api/pedidos/:id` | GET |
| Actualizar estado pedido | `pedidoStore.ts` | `/api/pedidos/:id/estado` | PATCH |
| Cargar tracking | `trackingStore.ts` | `/api/pedidos/:pedidoId/tracking` | GET |
| Cargar favoritos | `favoritoStore.ts` | `/api/favoritos` | GET |
| Eliminar favorito | `favoritoStore.ts` | `/api/favoritos/:id` | DELETE |
| Cargar perfil | `authStore.ts` | `/api/users/me` | GET |
| Actualizar perfil | `authStore.ts` | `/api/users/me` | PATCH |
| Cargar productos del productor | `productoStore.ts` | `/api/productos?productorId=uuid` | GET |
| Crear producto | `productoStore.ts` | `/api/productos` | POST |
| Editar producto | `productoStore.ts` | `/api/productos/:id` | PATCH |
| Eliminar producto | `productoStore.ts` | `/api/productos/:id` | DELETE |
| Dashboard resumen | Dashboard* | `/api/dashboard/resumen` | GET |

---

## 7. SEGURIDAD

- **JWT:** accessToken 15 min, refreshToken 7 días (httpOnly cookie o body)
- **bcrypt:** 10-12 rounds de salt
- **Rate limiting:** 100 requests/min por IP (login: 5 intentos/min)
- **CORS:** Solo permitir origen del frontend
- **Validación:** Zod/class-validator en todos los inputs
- **SQL Injection:** Prevenido por ORM (Prisma/TypeORM)
- **Helmet:** Headers de seguridad HTTP
- **Roles:** Middleware de autorización por endpoint

---

## 8. VARIABLES DE ENTORNO (.env)

```env
NODE_ENV=development
PORT=3000

DATABASE_URL=postgresql://user:pass@localhost:5432/agroconet

JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=15m
JWT_REFRESH_SECRET=your-refresh-secret
JWT_REFRESH_EXPIRES_IN=7d

CORS_ORIGIN=http://localhost:5173

# Opcionales para features futuros
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1
COMMODITIES_API_KEY=
```

---

## 9. NOTAS IMPORTANTES

1. El frontend actual usa `http://localhost:3001` como baseURL. Cuando el backend real esté listo, cambiar a `http://localhost:3000/api` en `src/composables/useApi.ts`.
2. El frontend NO tiene manejo de tokens JWT todavía. Habrá que modificar `useAuth.ts` para almacenar el accessToken y agregar un interceptor en Axios para incluir `Authorization: Bearer <token>` en cada request.
3. El frontend filtra pedidos/favoritos client-side. El backend DEBE enviar ya filtrado por el usuario autenticado.
4. Clima: Open-Meteo es una API pública gratuita que el frontend llama directamente. No requiere backend pero se puede optar por un proxy si es necesario.
5. Precios de mercado: Actualmente son estimaciones en el frontend. El backend puede integrar una API real (Commodities-API, API Ninjas) y servir los precios en los endpoints de productos.
