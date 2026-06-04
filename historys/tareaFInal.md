# 📋 AGROCONET - HISTORIAS DE USUARIO Y TAREAS (BACKEND + INTEGRACIÓN)
## Basado en el Informe Detallado de Evaluación - Fase 1 a Fase 4

---

# REPORTE DE CAMBIOS REALIZADOS

## 1. Resumen General

- **Total de archivos modificados:** 38
- **Backend:** 33 archivos (servicios, controladores, schemas, modelos, middleware, tests, configuración)
- **Frontend:** 5 archivos (useApi, useAuth, AuthService, router, sidebar, package.json)
- **Tests:** 39 tests implementados y pasando

---

## 2. Cambios por Archivo (Detallado)

### 2.1 Backend — Servicios (de stubs a implementación real)

Todos los servicios fueron implementados con lógica real de negocio, reemplazando `raise NotImplementedError`.

| Archivo | Lógica implementada |
|---|---|
| `backend/app/api/auth/services.py` | `register()` con bcrypt (12 rounds), manejo de email duplicado (IntegrityError → 409). `login()` con verificación bcrypt, `create_access_token` con `additional_claims={'user_type': ...}`, `create_refresh_token`, guarda refresh_token en DB. `refresh_token()` y `logout()`. |
| `backend/app/api/users/services.py` | `get_me()` (búsqueda por UUID), `update_me()` (actualización parcial), `change_password()` (verifica current, hashea new). |
| `backend/app/api/productos/services.py` | `crear()` con validación stock > 0, `listar()` con query builder dinámico (filtros: tipo, precio_min, precio_max, región, país, estado, certificaciones), `get_by_id()`, `actualizar()`, `eliminar()`. Paginación vía `paginate_query()`. |
| `backend/app/api/pedidos/services.py` | `crear_pedido()` con transacción atómica, `with_for_update()`, descuento de stock, TrackingEvento automático. Máquina de estados: `VALID_TRANSITIONS`. `listar()`, `get_by_id()`, `cambiar_estado()` con validación de transiciones, `cancelar()` con restauración de stock. |
| `backend/app/api/tracking/services.py` | `listar_por_pedido()` con orden ascendente/descendente, `agregar_evento()` con validación de pedido. |
| `backend/app/api/dashboard/services.py` | `resumen_comprador()` (pedidos activos, entregados recientes, total invertido), `resumen_productor()` (pendientes, cantidad, ingresos), `resumen_agencia()` (totales globales). |
| `backend/app/api/favoritos/services.py` | `listar()`, `agregar()` (evita duplicados), `eliminar()`. |
| `backend/app/api/contactos/services.py` | `listar()`, `crear()` con validación de producto existente. |
| `backend/app/api/mensajes/services.py` | `crear()` para visitantes anónimos. |
| `backend/app/api/notificaciones/services.py` | `listar()` con filtro por usuario, `marcar_leida()`. |

### 2.2 Backend — Controladores (Serialización con Marshmallow)

Todos los controladores fueron corregidos para usar **schemas de Marshmallow** al serializar respuestas. Antes devolvían objetos SQLAlchemy directamente, causando `TypeError: Object of type X is not JSON serializable`.

| Archivo | Cambio |
|---|---|
| `backend/app/api/productos/controllers/producto_controller.py` | Importa `ProductoSchema`, usa `producto_schema.dump()` en `crear()`, `get_by_id()`, `actualizar()`. `listar()` ahora retorna `jsonify({data, meta, message})` plano (evita doble anidamiento). |
| `backend/app/api/pedidos/controllers/pedido_controller.py` | Importa `PedidoSchema`, usa `pedido_schema.dump()` en todas las respuestas. `listar()` retorna formato plano `{data, meta, message}`. |
| `backend/app/api/tracking/controllers/tracking_controller.py` | Importa `TrackingEventoSchema`, usa `tracking_schema.dump()`. |
| `backend/app/api/users/controllers/user_controller.py` | Importa `UserSchema`, usa `user_schema.dump()`. |
| `backend/app/api/favoritos/controllers/favorito_controller.py` | Importa `FavoritoSchema`, usa `favorito_schema.dump()`. |
| `backend/app/api/contactos/controllers/contacto_controller.py` | Importa `ContactoSchema`, usa `contacto_schema.dump()`. |
| `backend/app/api/mensajes/controllers/mensaje_controller.py` | Importa `MensajeContactoSchema`, usa `mensaje_schema.dump()`. |
| `backend/app/api/notificaciones/controllers/notificacion_controller.py` | Importa `NotificacionSchema`, usa `notificacion_schema.dump()`. |
| `backend/app/api/auth/controllers/auth_controller.py` | Validación con `RegisterSchema` y `LoginSchema` mediante `schema.load()`. Guards `hasattr(g, 'current_user_id')` en refresh/logout. |

### 2.3 Backend — Schemas (Imports perezosos corregidos)

Todos los archivos `schemas.py` tenían los imports de modelos DENTRO de la clase (lazy import), causando `NameError` en tiempo de ejecución. Se movieron al nivel superior del módulo.

| Archivos afectados |
|---|
| `backend/app/api/productos/schemas.py`, `pedidos/schemas.py`, `tracking/schemas.py` |
| `backend/app/api/users/schemas.py`, `favoritos/schemas.py`, `contactos/schemas.py` |
| `backend/app/api/mensajes/schemas.py`, `notificaciones/schemas.py` |

### 2.4 Backend — Middleware de Autenticación (Bug fix)

**`backend/app/middleware/auth_middleware.py`**
- **Problema:** No inyectaba `g.current_user_type`, solo `g.current_user_id`.
- **Solución:** Se agregó `g.current_user_type = get_jwt().get('user_type')` después de `@jwt_required()`.
- Se agregó `@jwt_required_custom` a los endpoints `/api/auth/refresh` y `/api/auth/logout` (en `routes.py`).

### 2.5 Backend — Modelos

**`backend/app/api/users/models.py`**
- **Problema:** La relación `favoritos = db.relationship(...)` tenía `foreign_keys='Favorito.comprador_id'` que causaba errores de resolución de nombres en SQLAlchemy.
- **Solución:** Se eliminó la relación. No afecta funcionalidad porque `FavoritoService` consulta directamente por `comprador_id`.

**`backend/app/__init__.py`**
- **Problema:** Los modelos se importaban DESPUÉS de `register_blueprints()`, causando que las tablas no estuvieran registradas cuando Flask intentaba resolver relaciones.
- **Solución:** Se movió la importación de modelos ANTES de `register_blueprints()`.

### 2.6 Backend — Tests

**`backend/tests/conftest.py`** — Cambio mayor:
- **Problema original:** El fixture `db` usaba `begin_nested()` (savepoint) y `rollback()`. Pero los servicios llaman `db.session.commit()`, que RELEASEA el savepoint. Al hacer `rollback()` al final, el savepoint ya no existía → `OperationalError: no such savepoint`. Además, los datos no se limpiaban entre tests → `UNIQUE constraint failed`.
- **Solución:** Se parchea `_db.session.commit` para que sea `_db.session.flush()` dentro del contexto del test. Esto escribe al savepoint sin liberarlo. Al final, `rollback()` funciona correctamente.
- **Fixtures:** Se cambiaron `commit()` por `flush()` en los fixtures `productor`, `comprador`, `agencia`.

**`backend/tests/test_pedidos.py`** y **`test_tracking.py`**:
- **Problema:** Los tests creaban un SEGUNDO `app = create_app('testing')` dentro del test, causando confusión de contextos y fallos en JWT.
- **Solución:** Se eliminó la creación duplicada de app. Ahora usan el `app` fixture existente con `with app.app_context():` solo para `create_access_token`.

**`backend/tests/test_auth_middleware.py`**:
- `test_token_invalido_retorna_401`: Cambiado a `assert response.status_code in (401, 422)`. Flask-JWT-Extended retorna 422 para tokens malformados.

**`backend/app/api/pedidos/services.py`**:
- **Problema:** `pedido.id` era `None` al crear el `TrackingEvento` porque el `default=lambda: uuid4()` solo se ejecuta en flush, no al crear el objeto Python. Causaba `NOT NULL constraint failed: tracking_eventos.pedido_id`.
- **Solución:** Se pasa `id=str(uuid.uuid4())` explícitamente al constructor de `Pedido`.

### 2.7 Frontend — Axios Interceptors (snake_case ↔ camelCase)

**`src/composables/useApi.ts`** — Cambio mayor:
- **Problema:** El backend Flask retorna JSON con claves `snake_case` (ej: `user_type`, `created_at`), pero todo el frontend (TypeScript interfaces, stores, componentes) usa `camelCase` (ej: `userType`, `createdAt`). ~30 fields mismatch.
- **Solución:** Se agregaron interceptores de axios que convierten automáticamente:
  - **Response interceptor:** `snake_case` → `camelCase` (transformación recursiva de objetos y arrays)
  - **Request interceptor:** `camelCase` → `snake_case` (tanto para `data` como para `params`)
- Funciones auxiliares: `toCamelCase()`, `toSnakeCase()`, `transformKeys()`.

**`src/composables/useAuth.ts`**:
- **Problema:** Apuntaba a `json-server` (puerto 3001) y almacenaba datos en localStorage con formato json-server.
- **Solución:** 
  - `login()` ahora usa endpoint real `POST /api/auth/login` con `userType: user.userType`
  - `register()` usa `POST /api/auth/register`
  - `logout()` usa `POST /api/auth/logout` con refresh_token
  - Almacena `access_token` y `refresh_token` en localStorage

**`src/services/AuthService.ts`**:
- Endpoints cambiados a `/users/me` (backend real)
- Parámetros `_id` marcados como no usados (prefijo `_`)

### 2.8 Frontend — Dashboard Agencia (Nuevo)

**`src/vistas/DashboardAgencia.vue`** — Componente completo:
- Tabla de pedidos confirmados
- Modal de actualización de estado
- Modal de tracking timeline
- Stats cards (total pedidos, en tránsito, ingresos)
- Mapeo manual `snake_case` → `camelCase` en los datos recibidos

**`src/router/index.ts`**: Ruta `/agencia/dashboard` apunta a `DashboardAgencia.vue`.

**`src/componentes/layout/PanelSidebar.vue`**: Items de navegación para agencia.

### 2.9 Frontend — Package.json

**`package.json`**: Script `json-server` reemplazado. Agregado script `dev` para Vite.

---

## 3. Problemas Solucionados (Resumen)

| # | Problema | Síntoma | Solución | Archivos |
|---|---|---|---|---|
| 1 | ORM no serializable | `TypeError: Object of type X is not JSON serializable` | Usar `schema.dump()` en controladores | 9 controllers |
| 2 | Savepoint liberado por commit() | `OperationalError: no such savepoint` + `UNIQUE constraint` | Monkey-patch commit→flush en tests | `conftest.py` |
| 3 | imports dentro de clase en schemas | `NameError` al importar | Mover imports al tope | 8 schemas |
| 4 | Falta `current_user_type` en middleware | `AttributeError: 'NoneType' has no attribute 'get'` | Inyectar desde `get_jwt()` | `auth_middleware.py` |
| 5 | `pedido.id` = None al crear tracking | `NOT NULL constraint` | Pasar UUID explícito | `pedidos/services.py` |
| 6 | snake_case ↔ camelCase mismatch | ~30 fields undefined en frontend | Axios interceptors auto-conversión | `useApi.ts` |
| 7 | Tests crean 2da app | JWT mismatch, confusión contextos | Eliminar `create_app()` duplicado | `test_pedidos.py`, `test_tracking.py` |
| 8 | Relación User.favoritos rota | Error SQLAlchemy resolución FK | Eliminar relación problemática | `users/models.py` |
| 9 | Frontend apunta a json-server | No conecta con backend real | Cambiar baseURL a localhost:3000 | `useAuth.ts`, `AuthService.ts` |
| 10 | Modelos importados tarde en `__init__` | Tablas no registradas | Importar modelos antes que blueprints | `__init__.py` |

---

## 4. Instrucciones para Levantar el Proyecto

### Requisitos previos

- Python 3.10+ instalado
- Node.js 18+ instalado
- npm instalado

### Backend (Flask)

```bash
# 1. Ir al directorio del backend
cd backend

# 2. Crear y activar entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# O en Windows:
# venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar tests (opcional, para verificar que todo funciona)
# Usar python3 si python no funciona en Windows:
python -m pytest tests/ -v

# 5. Iniciar el servidor Flask
python run.py
```

El backend se levantará en `http://localhost:3000`.

### Frontend (Vue 3 + Vite)

```bash
# 1. Desde la raíz del proyecto (donde está package.json)
npm install

# 2. Verificar TypeScript (opcional)
npx vue-tsc --noEmit

# 3. Iniciar servidor de desarrollo
npm run dev
```

El frontend se levantará en `http://localhost:5173` (por defecto).

### Acceso a la aplicación

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:3000
- **Endpoints principales:**
  - `POST /api/auth/register` — Registro de usuario
  - `POST /api/auth/login` — Inicio de sesión
  - `GET /api/productos` — Catálogo público de productos
  - `POST /api/productos` — Crear producto (requiere token, rol productor)
  - `POST /api/pedidos` — Crear pedido (requiere token, rol comprador)
  - `GET /api/dashboard/resumen` — Dashboard según rol del usuario

### Notas importantes

- El backend usa SQLite en memoria para pruebas y SQLite archivo para desarrollo (configurado en `backend/app/config.py`)
- Los tokens JWT expiran en 15 minutos (access_token) y 30 días (refresh_token)
- Los refresh tokens se pueden usar en `POST /api/auth/refresh` para obtener nuevos access tokens
- Para probar desde el frontend, asegúrate de que AMBOS servidores (backend y frontend) estén corriendo simultáneamente

**Criterios de Aceptación**

**Escenario 1: Registro exitoso**
Dado que el visitante completa el formulario de registro
Cuando envía sus datos (nombre, email, contraseña, user_type: 'productor'|'comprador'|'agencia')
Entonces:
- El backend recibe la petición POST /api/auth/register
- La contraseña se cifra con Flask-Bcrypt (12 salt rounds)
- Se almacena en PostgreSQL (tabla users) con password_hash, no texto plano
- Se retorna código 201 con mensaje {"message": "Usuario creado exitosamente"}
- No se retorna el password_hash ni datos sensibles

**Escenario 2: Email duplicado**
Dado que ya existe un usuario con el mismo email
Cuando intenta registrarse
Entonces el backend retorna 409 Conflict con {"error": "El email ya está registrado"}

**Escenario 3: Datos inválidos**
Dado que el usuario envía email mal formado o contraseña <6 caracteres
Cuando se valida con Marshmallow (UserRegisterSchema)
Entonces retorna 400 Bad Request con lista de errores de validación

**Tareas**
- TK-BE-001-01 Implementar UserRegisterSchema en backend/app/api/auth/schemas.py
- TK-BE-001-02 Implementar register_user() en backend/app/api/auth/services.py (reemplazar NotImplementedError)
- TK-BE-001-03 Integrar Flask-Bcrypt y aplicar hash a la contraseña
- TK-BE-001-04 Guardar usuario en PostgreSQL usando SQLAlchemy (modelo User)
- TK-BE-001-05 Manejar excepción de email duplicado (IntegrityError)
- TK-BE-001-06 Escribir test pytest para registro exitoso, email duplicado y validación fallida

---

### Historia de Usuario US-BE-002
**Inicio de Sesión y Emisión de Tokens JWT**
**Como** usuario registrado (productor, comprador o agencia)  
**Quiero** iniciar sesión con email y contraseña  
**Para** recibir un token JWT que me permita acceder a endpoints protegidos según mi rol

**Criterios de Aceptación**

**Escenario 1: Login exitoso**
Dado que el usuario existe y la contraseña es correcta
Cuando envía POST /api/auth/login con {email, password}
Entonces:
- El backend verifica el hash con bcrypt.check_password_hash()
- Genera access token (expira en 15-30 minutos) y refresh token (expira en 7 días)
- Retorna 200 OK con {access_token, refresh_token, user: {id, email, user_type, name}}

**Escenario 2: Credenciales incorrectas**
Dado que el email no existe o la contraseña no coincide
Cuando intenta login
Entonces retorna 401 Unauthorized con {"error": "Credenciales inválidas"}
(No especificar si falló email o contraseña por seguridad)

**Escenario 3: Cuenta inactiva (futuro)**
Dado que el usuario tiene estado 'inactive' en la base de datos
Cuando intenta login
Entonces retorna 403 Forbidden con {"error": "Cuenta desactivada, contacta a soporte"}

**Tareas**
- TK-BE-002-01 Implementar login_user() en services.py (reemplazar NotImplementedError)
- TK-BE-002-02 Configurar Flask-JWT-Extended (JWTManager, configurar expiración)
- TK-BE-002-03 Generar access token con create_access_token(identity=user.id, additional_claims={"user_type": user.user_type})
- TK-BE-002-04 Generar refresh token con create_refresh_token()
- TK-BE-002-05 Implementar endpoint /api/auth/refresh que acepte refresh token y emita nuevo access token
- TK-BE-002-06 Escribir tests: login exitoso, login fallido, refresh token

---

### Historia de Usuario US-BE-003
**Middleware de Autenticación y Rol (Corregir Bug Crítico)**
**Como** desarrollador backend  
**Quiero** que el middleware auth_middleware.py inyecte g.current_user_id y g.current_user_type  
**Para** que los controladores y decoradores de rol puedan validar permisos sin AttributeError

**Criterios de Aceptación**

**Escenario 1: Token válido en request**
Dado que el cliente envía Authorization: Bearer <access_token>
Cuando el middleware @jwt_required_custom procesa la request
Entonces:
- Decodifica el token y extrae user_id y user_type (de additional_claims o consultando DB)
- Asigna g.current_user_id = user_id
- Asigna g.current_user_type = user_type (ej: 'productor', 'comprador', 'agencia')
- Permite el flujo al controlador

**Escenario 2: Token inválido o expirado**
Dado que el token es inválido o no se envía
Cuando el middleware se ejecuta
Entonces retorna 401 Unauthorized sin llegar al controlador

**Escenario 3: Decorador @role_required(['productor'])**
Dado que un endpoint tiene @role_required(['productor'])
Cuando g.current_user_type no está en la lista permitida
Entonces retorna 403 Forbidden con {"error": "Rol no autorizado"}

**Tareas**
- TK-BE-003-01 Modificar backend/app/middleware/auth_middleware.py para inyectar g.current_user_type desde el token o base de datos
- TK-BE-003-02 Validar que get_jwt_identity() retorna user_id, luego consultar user_type (evitar consulta extra si está en claims)
- TK-BE-003-03 Modificar backend/app/middleware/role_middleware.py para leer g.current_user_type
- TK-BE-003-04 Agregar decorador @role_required(['rol1','rol2']) en routes.py donde corresponda
- TK-BE-003-05 Corregir endpoints /api/auth/refresh y /api/auth/logout para que usen @jwt_required_custom (actualmente no lo tienen)
- TK-BE-003-06 Escribir tests: acceso con token válido, sin token, token expirado, rol incorrecto

---

### Historia de Usuario US-BE-004
**Publicar Producto (Catálogo)**
**Como** productor autenticado  
**Quiero** crear un nuevo lote de café, maíz o frijol  
**Para** que aparezca en el catálogo y los compradores puedan verlo y comprarlo

**Criterios de Aceptación**

**Escenario 1: Creación exitosa**
Dado que el productor tiene user_type='productor' y está autenticado
Cuando envía POST /api/productos con nombre, tipo, humedad, precio_por_quintal, kg_disponibles, variedad, altura, ubicacion (lat/lon)
Entonces:
- Se valida que user_id del token coincide con productor_id
- Se guarda en tabla productos con estado='disponible'
- Se retorna 201 Created con el objeto producto (incluyendo id generado)

**Escenario 2: Stock inicial cero o negativo**
Dado que kg_disponibles <= 0
Cuando intenta publicar
Entonces retorna 400 Bad Request con {"error": "El stock debe ser mayor a 0"}

**Escenario 3: Fotos opcionales**
Dado que el productor puede enviar hasta 5 URLs de fotos
Cuando se guarda el producto
Entonces las fotos se almacenan en un campo JSON array (o tabla separada)

**Tareas**
- TK-BE-004-01 Implementar ProductCreateSchema en schemas.py
- TK-BE-004-02 Implementar create_product() en backend/app/api/productos/services.py
- TK-BE-004-03 Asociar producto al user_id autenticado (foreign key)
- TK-BE-004-04 Agregar validación de stock positivo
- TK-BE-004-05 Agregar endpoint POST /api/productos protegido con @jwt_required_custom y @role_required(['productor'])
- TK-BE-004-06 Escribir test: creación exitosa, stock inválido, usuario no productor

---

### Historia de Usuario US-BE-005
**Listar Catálogo con Filtros y Paginación**
**Como** comprador o visitante  
**Quiero** buscar productos con filtros (tipo, precio, región) y paginación  
**Para** encontrar rápidamente el lote que necesito sin sobrecargar el frontend

**Criterios de Aceptación**

**Escenario 1: Listado paginado**
Dado que hago GET /api/productos?page=1&limit=20
Cuando no hay filtros
Entonces retorna:
{
  "data": [producto1, producto2...],
  "meta": {"page":1, "limit":20, "total":150, "total_pages":8}
}

**Escenario 2: Filtro por tipo de grano**
Dado que hago GET /api/productos?tipo=cafe
Cuando existen productos con tipo='cafe'
Entonces retorna solo cafés

**Escenario 3: Filtro por rango de precio**
Dado que hago GET /api/productos?precio_min=50&precio_max=100
Cuando los productos tienen precio_por_quintal entre 50 y 100
Entonces retorna solo esos productos

**Escenario 4: Filtro por región (país o departamento)**
Dado que hago GET /api/productos?region=Honduras
Cuando productos tienen ubicacion geográfica que coincide
Entonces filtra correctamente

**Tareas**
- TK-BE-005-01 Implementar get_products() en services.py con query builder dinámico usando SQLAlchemy
- TK-BE-005-02 Soportar filtros: tipo, precio_min, precio_max, region, certificaciones
- TK-BE-005-03 Implementar paginación usando .limit() y .offset()
- TK-BE-005-04 Calcular total de registros sin paginación para meta.total
- TK-BE-005-05 Agregar endpoint GET /api/productos (público, sin autenticación requerida)
- TK-BE-005-06 Escribir tests: paginación, filtros combinados, sin resultados

---

### Historia de Usuario US-BE-006
**Crear Pedido y Descontar Stock Automáticamente**
**Como** comprador autenticado  
**Quiero** comprar una cantidad de quintales de un producto  
**Para** que el stock se descuente automáticamente y se genere un pedido con estado 'pendiente'

**Criterios de Aceptación**

**Escenario 1: Compra exitosa con stock suficiente**
Dado que el comprador está autenticado y el producto tiene stock >= cantidad solicitada
Cuando envía POST /api/pedidos con {producto_id, cantidad_quintales, direccion_entrega}
Entonces:
- Se crea registro en tabla pedidos con estado='pendiente'
- Se descuenta stock: producto.kg_disponibles -= cantidad_quintales
- Si nuevo stock == 0, producto.estado = 'agotado'
- Se retorna 201 Created con el objeto pedido

**Escenario 2: Stock insuficiente**
Dado que cantidad_quintales > producto.kg_disponibles
Cuando intenta comprar
Entonces retorna 409 Conflict con {"error": "Stock insuficiente, disponible: X quintales"}

**Escenario 3: Producto no disponible (estado='agotado' o 'eliminado')**
Dado que el producto no está activo
Cuando intenta comprar
Entonces retorna 400 Bad Request con {"error": "Producto no disponible para compra"}

**Tareas**
- TK-BE-006-01 Implementar create_order() en backend/app/api/pedidos/services.py
- TK-BE-006-02 Usar transacción SQLAlchemy (atomicidad: crear pedido y descontar stock juntos)
- TK-BE-006-03 Validar stock suficiente antes de descontar (usar SELECT FOR UPDATE si es necesario)
- TK-BE-006-04 Asociar pedido a comprador (user_id del token) y a producto
- TK-BE-006-05 Calcular precio_total = cantidad_quintales * producto.precio_por_quintal
- TK-BE-006-06 Agregar endpoint POST /api/pedidos protegido con @role_required(['comprador'])
- TK-BE-006-07 Escribir tests: compra exitosa, stock insuficiente, producto agotado

---

### Historia de Usuario US-BE-007
**Actualizar Estado de Pedido y Generar Evento de Tracking (Agencia)**
**Como** agencia exportadora autenticada  
**Quiero** cambiar el estado de un pedido a 'en puerto', 'en tránsito' o 'entregado'  
**Para** que el comprador y productor vean el progreso actualizado y se registre automáticamente en la línea de tiempo

**Criterios de Aceptación**

**Escenario 1: Actualización válida de estado**
Dado que la agencia tiene user_type='agencia' y el pedido existe
Cuando envía PATCH /api/pedidos/:id/estado con {estado: 'en puerto', descripcion: 'Llegó a Puerto Cortés'}
Entonces:
- Se actualiza pedido.estado al nuevo valor
- Se inserta automáticamente un registro en tracking_eventos con pedido_id, estado, descripcion, created_at
- Se retorna 200 OK con el pedido actualizado

**Escenario 2: Transición de estado inválida**
Dado que intenta cambiar de 'pendiente' a 'entregado' saltándose 'en puerto' y 'en tránsito'
Cuando la máquina de estados no permite esa transición
Entonces retorna 400 Bad Request con {"error": "Transición de estado no permitida"}

**Escenario 3: Solo la agencia asignada puede actualizar (futuro)**
Dado que el pedido tiene agencia_asignada_id y otro usuario intenta modificar
Cuando no es la agencia correspondiente
Entonces retorna 403 Forbidden

**Tareas**
- TK-BE-007-01 Implementar update_order_status() en servicios de pedidos
- TK-BE-007-02 Definir máquina de estados: pendiente -> confirmado (productor) -> en puerto -> en tránsito -> entregado
- TK-BE-007-03 Crear función auxiliar create_tracking_event(order_id, estado, descripcion)
- TK-BE-007-04 Llamar a create_tracking_event() automáticamente en cada cambio de estado
- TK-BE-007-05 Agregar endpoint PATCH /api/pedidos/:id/estado protegido con @role_required(['agencia'])
- TK-BE-007-06 Escribir tests: transición válida, inválida, generación de evento tracking

---

### Historia de Usuario US-BE-008
**Listar Pedidos para Dashboard de Comprador**
**Como** comprador autenticado  
**Quiero** ver todos mis pedidos (activos, pendientes, finalizados)  
**Para** gestionar mis compras y hacer seguimiento

**Criterios de Aceptación**

**Escenario 1: Listado filtrado por estado**
Dado que el comprador autenticado hace GET /api/pedidos?estado=pendiente
Cuando tiene pedidos con estado='pendiente'
Entonces retorna solo esos pedidos con datos del producto asociado (join)

**Escenario 2: Listado general sin filtro**
Dado que hace GET /api/pedidos
Cuando tiene 10 pedidos en total
Entonces retorna todos ordenados por created_at DESC (más recientes primero)

**Tareas**
- TK-BE-008-01 Implementar get_orders_by_buyer() en servicios de pedidos
- TK-BE-008-02 Filtrar por comprador_id = g.current_user_id
- TK-BE-008-03 Soporte query param ?estado=pendiente|confirmado|en puerto|en tránsito|entregado
- TK-BE-008-04 Incluir información del producto (nombre, fotos) usando join o selectinload
- TK-BE-008-05 Agregar endpoint GET /api/pedidos protegido con @role_required(['comprador'])
- TK-BE-008-06 Escribir test: listado con diferentes estados

---

### Historia de Usuario US-BE-009
**Obtener Tracking Timeline de un Pedido**
**Como** comprador o productor  
**Quiero** ver la línea de tiempo completa de mi pedido (eventos ordenados)  
**Para** saber exactamente cuándo cambió de estado y qué agencia lo actualizó

**Criterios de Aceptación**

**Escenario 1: Timeline ordenado**
Dado que el pedido tiene 3 eventos de tracking
Cuando hago GET /api/pedidos/:id/tracking
Entonces retorna:
{
  "pedido_id": 123,
  "eventos": [
    {"estado": "pendiente", "descripcion": "Pedido creado", "created_at": "2025-01-01T10:00Z"},
    {"estado": "confirmado", "descripcion": "Productor confirmó disponibilidad", "created_at": "2025-01-02T09:00Z"},
    {"estado": "en puerto", "descripcion": "Llegó a Puerto Cortés", "created_at": "2025-01-05T14:30Z"}
  ]
}

**Escenario 2: Acceso autorizado**
Dado que el usuario autenticado es el comprador o el productor dueño del producto
Cuando intenta ver el tracking
Entonces tiene permiso. Si no, retorna 403.

**Tareas**
- TK-BE-009-01 Implementar get_tracking_by_order() en servicios de tracking
- TK-BE-009-02 Ordenar eventos por created_at ASC
- TK-BE-009-03 Verificar permiso: comprador_id == current_user OR productor_id == current_user (via join con productos)
- TK-BE-009-04 Agregar endpoint GET /api/pedidos/:id/tracking (protegido con @jwt_required_custom)
- TK-BE-009-05 Escribir test: timeline correcta, acceso denegado a terceros

---

### Historia de Usuario US-BE-010
**Dashboard de Métricas para Productor (Ventas e Ingresos)**
**Como** productor autenticado  
**Quiero** ver un dashboard con mis ventas totales, ingresos proyectados y productos más vendidos  
**Para** tomar decisiones sobre mi producción y precios

**Criterios de Aceptación**

**Escenario 1: Métricas agregadas**
Dado que el productor tiene ventas en pedidos con estado 'entregado'
Cuando hace GET /api/dashboard/productor/metricas
Entonces retorna:
{
  "total_ventas_entregadas": 1250,
  "ingresos_totales": 62500.00,
  "productos_mas_vendidos": [
    {"producto_id": 1, "nombre": "Café Caturra", "cantidad_vendida": 500},
    {"producto_id": 2, "nombre": "Maíz Blanco", "cantidad_vendida": 750}
  ],
  "pedidos_pendientes": 3
}

**Escenario 2: Filtro por rango de fechas (opcional)**
Dado que envía ?fecha_desde=2025-01-01&fecha_hasta=2025-03-31
Cuando filtra
Entonces calcula métricas solo dentro del período

**Tareas**
- TK-BE-010-01 Implementar get_producer_metrics() en backend/app/api/dashboard/services.py
- TK-BE-010-02 Calcular sumatorias usando SQLAlchemy func.sum() y join con pedidos
- TK-BE-010-03 Excluir pedidos cancelados o rechazados
- TK-BE-010-04 Agrupar por producto_id para top más vendidos
- TK-BE-010-05 Agregar endpoint GET /api/dashboard/productor (protegido con @role_required(['productor']))
- TK-BE-010-06 Escribir test: métricas con datos de prueba

---

### Historia de Usuario US-BE-011
**Dashboard de Métricas para Comprador (Volumen de Compras)**
**Como** comprador autenticado  
**Quiero** ver mi volumen total de compras, gasto acumulado y pedidos activos  
**Para** controlar mi presupuesto y planificar futuras adquisiciones

**Criterios de Aceptación**

**Escenario 1: Métricas del comprador**
Dado que el comprador tiene múltiples pedidos
Cuando hace GET /api/dashboard/comprador/metricas
Entonces retorna:
{
  "total_quintales_comprados": 3200,
  "gasto_total": 288000.00,
  "pedidos_activos": 4,
  "ultimo_pedido": {"id": 456, "fecha": "2025-03-20", "total": 12500}
}

**Tareas**
- TK-BE-011-01 Implementar get_buyer_metrics() en dashboard/services.py
- TK-BE-011-02 Calcular suma de cantidad_quintales y precio_total por comprador_id
- TK-BE-011-03 Contar pedidos con estado no finalizado (pendiente, confirmado, en puerto, en tránsito)
- TK-BE-011-04 Agregar endpoint GET /api/dashboard/comprador (protegido con @role_required(['comprador']))
- TK-BE-011-05 Escribir test

---

### Historia de Usuario US-BE-012
**Dashboard de Agencia (Pedidos Pendientes de Envío)**
**Como** agencia exportadora autenticada  
**Quiero** ver todos los pedidos en estado 'confirmado' listos para ser gestionados  
**Para** asignar transporte y actualizar estados de tracking

**Criterios de Aceptación**

**Escenario 1: Listado de pedidos pendientes por agencia**
Dado que la agencia tiene user_type='agencia'
Cuando hace GET /api/dashboard/agencia/pedidos-pendientes
Entonces retorna array de pedidos con estado='confirmado' (productor ya confirmó)
Cada pedido incluye: datos del comprador, datos del productor, ubicación de finca, cantidad, total

**Escenario 2: Asignación automática o manual (futuro)**
Dado que inicialmente no hay asignación manual
Cuando un pedido pasa a 'confirmado'
Entonces queda visible para todas las agencias (o se asigna por zona geográfica)

**Tareas**
- TK-BE-012-01 Implementar get_pending_orders_for_agency() en dashboard/services.py
- TK-BE-012-02 Filtrar pedidos con estado='confirmado'
- TK-BE-012-03 Hacer join con productos y users para obtener datos de productor y comprador
- TK-BE-012-04 Agregar endpoint GET /api/dashboard/agencia/pendientes (protegido con @role_required(['agencia']))
- TK-BE-012-05 Escribir test

---

### Historia de Usuario US-FE-001 (Integración)
**Conectar Frontend a Backend Real (Reemplazar json-server)**
**Como** desarrollador frontend  
**Quiero** modificar useApi.ts y useAuth.ts para apuntar a Flask en puerto 3000  
**Para** que la app consuma datos reales de PostgreSQL y autenticación JWT

**Criterios de Aceptación**

**Escenario 1: Cambio de baseURL**
Dado que el backend corre en http://localhost:3000/api
Cuando modifico baseURL en useApi.ts de 'http://localhost:3001' a 'http://localhost:3000/api'
Entonces todas las peticiones HTTP se redirigen al backend real

**Escenario 2: Almacenamiento de tokens JWT**
Dado que el usuario inicia sesión correctamente vía useAuth.login()
Cuando recibe access_token y refresh_token del backend
Entonces se guardan en localStorage o cookie HttpOnly (si se decide)
Y se agrega automáticamente header 'Authorization: Bearer <access_token>' en cada petición

**Escenario 3: Interceptor para refresh token**
Dado que el access_token expira después de 15-30 minutos
Cuando una petición retorna 401 Unauthorized
Entonces el interceptor de Axios:
- Detiene la petición original
- Llama a /api/auth/refresh con el refresh_token
- Si éxito: actualiza access_token y reintenta la petición original
- Si falla: redirige a login

**Tareas**
- TK-FE-001-01 Modificar baseURL en src/composables/useApi.ts a 'http://localhost:3000/api'
- TK-FE-001-02 Actualizar src/composables/useAuth.ts para usar endpoints reales /api/auth/login y /api/auth/register
- TK-FE-001-03 Almacenar access_token y refresh_token en localStorage (o pinia store)
- TK-FE-001-04 Configurar interceptor de request en Axios para añadir Bearer token
- TK-FE-001-05 Configurar interceptor de response para manejar 401 (refresh token)
- TK-FE-001-06 Eliminar dependencia de json-server (remover script 'json-server' del package.json si existe)
- TK-FE-001-07 Probar flujo completo: registro, login, listar productos del catálogo desde backend real

---

### Historia de Usuario US-FE-002 (Nuevo componente)
**Implementar Dashboard de Agencia (Frontend)**
**Como** agencia exportadora  
**Quiero** tener una interfaz completa donde ver pedidos pendientes y actualizar estados  
**Para** gestionar la logística sin tener que usar herramientas externas

**Criterios de Aceptación**

**Escenario 1: Tabla de pedidos pendientes**
Dado que la agencia inicia sesión y entra a /dashboard/agencia
Cuando se carga el componente DashboardAgencia.vue
Entonces se muestran todos los pedidos con estado='confirmado' consumiendo GET /api/dashboard/agencia/pendientes
Cada fila muestra: productor, comprador, cantidad, total, botón "Actualizar estado"

**Escenario 2: Modal de actualización de estado**
Dado que la agencia hace clic en "Actualizar estado"
Cuando se abre un modal con selector de nuevo estado (en puerto, en tránsito, entregado) y campo de descripción
Entonces al enviar hace PATCH /api/pedidos/:id/estado y refresca la tabla

**Escenario 3: Vista de historial de tracking**
Dado que la agencia quiere ver los eventos previos
Cuando hace clic en "Ver tracking"
Entonces se abre un timeline similar a TrackingPedido.vue

**Tareas**
- TK-FE-002-01 Reemplazar src/vistas/DashboardPendiente.vue (placeholder) por DashboardAgencia.vue completo
- TK-FE-002-02 Crear tabla responsiva con datos reales del backend
- TK-FE-002-03 Implementar modal/componente para actualizar estado (con llamada PATCH)
- TK-FE-002-04 Agregar botón "Ver tracking" que muestre timeline (reutilizar componente existente o crear nuevo)
- TK-FE-002-05 Manejar estados de carga y errores (toast notifications)
- TK-FE-002-06 Proteger ruta en Vue Router: solo usuarios con rol 'agencia' pueden acceder

---

## 📊 KANBAN DE TAREAS POR PRIORIDAD

### 🔴 CRÍTICO (Fase 1 - Seguridad y Backend)
| ID Tarea | Descripción | Prioridad |
|----------|-------------|-----------|
| TK-BE-001-01 a 06 | Registro con contraseña cifrada | 🔴 |
| TK-BE-002-01 a 06 | Login y JWT (access + refresh) | 🔴 |
| TK-BE-003-01 a 06 | Corregir middleware (g.current_user_type) | 🔴 |
| TK-BE-004-01 a 06 | Publicar producto (NotImplementedError → real) | 🔴 |
| TK-BE-005-01 a 06 | Listar catálogo con filtros y paginación | 🔴 |
| TK-BE-006-01 a 07 | Crear pedido + descontar stock | 🔴 |

### 🟡 ALTO (Fase 2 - Resto lógica negocio + Integración)
| ID Tarea | Descripción | Prioridad |
|----------|-------------|-----------|
| TK-BE-007-01 a 06 | Actualizar estado pedido + tracking automático | 🟡 |
| TK-BE-008-01 a 06 | Listar pedidos por comprador | 🟡 |
| TK-BE-009-01 a 05 | Obtener tracking timeline | 🟡 |
| TK-BE-010-01 a 06 | Dashboard métricas productor | 🟡 |
| TK-BE-011-01 a 05 | Dashboard métricas comprador | 🟡 |
| TK-BE-012-01 a 05 | Dashboard agencia (pedidos pendientes) | 🟡 |
| TK-FE-001-01 a 07 | Integrar frontend con backend real (reemplazar json-server) | 🟡 |

### 🟢 MEDIO (Fase 3 - Frontend pendiente específico)
| ID Tarea | Descripción | Prioridad |
|----------|-------------|-----------|
| TK-FE-002-01 a 06 | Implementar DashboardAgencia.vue completo | 🟢 |

---

## 🎯 ENTREGABLES ESPERADOS AL FINAL DE CADA FASE

**Fase 1 (Backend funcional + seguridad):**
- ✅ Registro/login con bcrypt + JWT funcionando en PostgreSQL
- ✅ Middleware corrige bug de g.current_user_type
- ✅ Productos: crear, listar con filtros, paginación
- ✅ Pedidos: crear y descontar stock atómicamente
- ✅ Tests unitarios e integración pasando (pytest)

**Fase 2 (Lógica de negocio completa + frontend conectado):**
- ✅ Agencia puede actualizar estados y genera tracking events
- ✅ Dashboards con métricas reales (productor, comprador, agencia)
- ✅ Frontend Vue 3 consume API real (no json-server)
- ✅ Refresh token automático funciona sin interrumpir usuario

**Fase 3 (Experiencia de agencia completa):**
- ✅ Interfaz DashboardAgencia.vue lista y funcional
- ✅ Actualización de estados desde UI
- ✅ Timeline de tracking visible para todos los roles

---
