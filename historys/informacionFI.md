# 📊 INFORME DETALLADO DE EVALUACIÓN Y PLAN DE AVANCE: AGROCONET (GRANO DIRECTO)

Este informe proporciona una evaluación exhaustiva del estado actual del proyecto **AgroConet** (nombre comercial provisional "GranoDirecto"), cubriendo tanto el **Frontend** (Vue 3) como el **Backend** (Flask + SQLAlchemy + PostgreSQL), identificando baches y brechas de desarrollo (*gaps*), y trazando la ruta de desarrollo (*roadmap*) necesaria para convertir el prototipo actual en un producto de nivel empresarial avanzado.

---

## 1. Introducción y Visión del Proyecto

**AgroConet** es una plataforma de mercado agrícola digital (**B2B + B2C**) orientada a conectar de manera directa a tres actores fundamentales del ecosistema productivo en Latinoamérica y el mundo:
1. **Productores Agrícolas**: Publican cosechas, especifican características físicas del grano (como variedad, altura de cultivo y porcentaje de humedad), gestionan su inventario y controlan los precios.
2. **Compradores (Tostadores, Molinos, Supermercados, Exportadores)**: Exploran el catálogo geolocalizado, adquieren cosechas por quintal o contenedor, guardan favoritos y realizan el seguimiento del flete.
3. **Agencias Exportadoras / Logísticas**: Actúan como terceros actores que gestionan la logística del transporte, recopilan documentación aduanera y actualizan el estado geográfico del cargamento.

**Objetivo Fundamental**: Eliminar la intermediación especulativa ineficiente, otorgar precios justos y transparentes al productor, y proveer una trazabilidad integral desde la finca original hasta el puerto de destino final.

---

## 2. Diagnóstico del Estado Actual del Stack

### A. Frontend (Vue 3 + Vite + Tailwind CSS v4 + TypeScript)
*   **Estado**: Prototipo funcional avanzado (Sprint 1 Completado).
*   **Alcance UI Implementado**:
    *   **Vistas Públicas**: 
        *   `Home.vue`: Landing page con propuesta de valor, carrusel dinámico de imágenes agrícolas y lista de productos destacados.
        *   `CatalogoProductos.vue`: Buscador avanzado con filtros dinámicos (tipo de grano, rango de precios, país, certificaciones). Cada card muestra el clima de la región del productor (consumido desde la API externa de *Open-Meteo*) y una estimación del valor de mercado.
        *   `DetalleProducto.vue`: Ficha técnica extendida del lote (humedad, variedad, altura, etc.) con sección de geolocalización, clima y acciones del mercado.
        *   `ComoFunciona.vue`, `QuienesSomos.vue` y `Contacto.vue`: Páginas institucionales. El formulario de contacto ya persiste datos.
    *   **Paneles Privados**:
        *   **Comprador**: Resumen del panel (`ResumenComprador.vue`), lista e historial de pedidos con timeline de tracking interactivo (`TrackingPedido.vue`), y lista de favoritos (`FavoritosList.vue`).
        *   **Productor**: Formulario de publicación y edición de productos (`ProductoForm.vue`), listado de stock (`ProductoList.vue`), y ventas recibidas (`PedidosRecibidos.vue`).
        *   **Agencia Exportadora**: Cuenta únicamente con un archivo placeholder vacío: [DashboardPendiente.vue](file:///c:/Users/Luis%20Alfonso/AgroConet/src/vistas/DashboardPendiente.vue).
*   **Estrategia de Datos y Auth (Simulada/Mock)**:
    *   La API base en [useApi.ts](file:///c:/Users/Luis%20Alfonso/AgroConet/src/composables/useApi.ts) apunta al puerto `3001` gestionado por `json-server` a través del archivo de base de datos simulado [db.json](file:///c:/Users/Luis%20Alfonso/AgroConet/db.json).
    *   La lógica en [useAuth.ts](file:///c:/Users/Luis%20Alfonso/AgroConet/src/composables/useAuth.ts) simula el registro e inicio de sesión de los usuarios. La validación se realiza a nivel del cliente (el frontend descarga la lista de usuarios y compara la contraseña en texto plano), lo cual representa un riesgo crítico de seguridad y debe sustituirse por un flujo de autenticación real.

### B. Backend (Flask + SQLAlchemy + JWT-Extended + Marshmallow + PostgreSQL)
*   **Estado**: Estructura arquitectónica base implementada, pero sin lógica de negocio (0% de lógica real).
*   **Alcance Técnico Implementado**:
    *   **Estructura y Modularidad (SOLID)**: El backend está estructurado bajo las mejores prácticas SOLID. Cada módulo (`auth`, `users`, `productos`, `pedidos`, `tracking`, `favoritos`, `contactos`, `mensajes`, `notificaciones`, `dashboard`) tiene sus propias capas desacopladas:
        *   `models.py`: Declaración de tablas y relaciones ORM.
        *   `schemas.py`: Validación de entrada y serialización de salida con Marshmallow.
        *   `services.py`: Contratos y definición de firma de métodos para la lógica de negocio.
        *   `controllers/`: Extracción de requests HTTP y delegación a los servicios.
        *   `routes.py`: Mapeo de rutas HTTP y control de seguridad de entrada.
    *   **Base de Datos y Migraciones**: Se definieron 8 modelos SQLAlchemy. Existe un archivo de migración Alembic inicial listo para crear las 8 tablas en PostgreSQL.
    *   **Pruebas Automatizadas**: 16 tests de integración ejecutados con `pytest` en `backend/tests/` para verificar el registro de blueprints de rutas y el correcto levantamiento del servidor.
*   **Inconsistencias y Bugs Identificados en el Backend**:
    1.  **Servicios Incompletos (Stubs)**: Absolutamente todos los métodos de los servicios (por ejemplo, registro, login, creación de productos, órdenes, y cálculo de dashboards) lanzan la excepción `raise NotImplementedError`.
    2.  **Error Crítico de Contexto en el Middleware**: En [auth_middleware.py](file:///c:/Users/Luis%20Alfonso/AgroConet/backend/app/middleware/auth_middleware.py), el decorador de token `@jwt_required_custom` solo inyecta el identificador del usuario (`g.current_user_id`), pero omite inyectar el rol (`g.current_user_type`). Sin embargo, en [role_middleware.py](file:///c:/Users/Luis%20Alfonso/AgroConet/backend/app/middleware/role_middleware.py) y en [dashboard_controller.py](file:///c:/Users/Luis%20Alfonso/AgroConet/backend/app/api/dashboard/controllers/dashboard_controller.py) se lee la propiedad `g.current_user_type`. Esto generará excepciones fatales de tipo `AttributeError` en tiempo de ejecución.
    3.  **Vulnerabilidad de Endpoints de Autenticación**: En [routes.py](file:///c:/Users/Luis%20Alfonso/AgroConet/backend/app/api/auth/routes.py), las rutas `/api/auth/refresh` y `/api/auth/logout` no aplican el decorador `@jwt_required_custom`, pero sus respectivos controladores intentan leer `g.current_user_id`, lo que causará fallos inmediatos por falta de contexto de usuario.

---

## 3. Próximos Avances Requeridos (Plan de Trabajo / Roadmap)

Para lograr un sistema integrado, seguro y robusto listo para producción, se plantean las siguientes cuatro fases de desarrollo:

### 🚀 Fase 1: Implementación de la Lógica del Backend
*   **Meta**: Hacer que la API de Flask y la base de datos PostgreSQL sean 100% funcionales.
1.  **Seguridad y Autenticación Real**:
    *   Implementar el registro cifrando las contraseñas con `Flask-Bcrypt` (12 salt rounds sugeridos).
    *   Implementar la autenticación real en [services.py](file:///c:/Users/Luis%20Alfonso/AgroConet/backend/app/api/auth/services.py) para emitir tokens JWT válidos usando `Flask-JWT-Extended`.
    *   Corregir el middleware [auth_middleware.py](file:///c:/Users/Luis%20Alfonso/AgroConet/backend/app/middleware/auth_middleware.py) para cargar el rol de usuario (`user_type`) en el objeto global `g.current_user_type` desde el token o base de datos.
    *   Asegurar que los endpoints de refresh y logout utilicen los decoradores de seguridad adecuados y gestionen la invalidación de tokens expirados.
2.  **Lógica del Negocio (SQLAlchemy)**:
    *   **Catálogo**: Implementar consultas de búsqueda filtrada con paginación avanzada (usando la utilidad de paginación existente en el core).
    *   **Pedidos y Transacciones**: Implementar la lógica para crear un pedido, calcular automáticamente el total del flete sumando posibles impuestos, y descontar los quintales correspondientes del stock del producto.
    *   **Trazabilidad**: Automatizar la creación de registros en la tabla de `tracking_eventos` cada vez que el estado de una orden sea modificado por el productor o la agencia.
    *   **Métricas del Dashboard**: Escribir las funciones agregadas en `DashboardService` para generar estadísticas reales en tiempo de ejecución (ingresos proyectados para productores, volumen total invertido para compradores y despachos activos para agencias).

### 🔗 Fase 2: Conexión e Integración Frontend-Backend
*   **Meta**: Sustituir el servidor mock (`json-server`) por el backend real de Flask.
1.  **Redirección de API**:
    *   Modificar la `baseURL` en [useApi.ts](file:///c:/Users/Luis%20Alfonso/AgroConet/src/composables/useApi.ts) para redirigir las peticiones HTTP al puerto del backend real (puerto `3000/api`).
2.  **Adaptación del Flujo de Sesión (Frontend)**:
    *   Actualizar [useAuth.ts](file:///c:/Users/Luis%20Alfonso/AgroConet/src/composables/useAuth.ts) para que almacene y gestione el access token y refresh token reales devueltos por el backend.
    *   Agregar un interceptor de peticiones en Axios que inserte de forma automática la cabecera `Authorization: Bearer <accessToken>` en cada solicitud protegida.
    *   Añadir un interceptor de respuesta que escuche errores `401` (No Autorizado) e invoque silenciosamente al endpoint `/api/auth/refresh` para renovar el token expitado sin interrumpir la experiencia de navegación del usuario.

### 📦 Fase 3: Implementación del Dashboard y Flujo de la Agencia Exportadora
*   **Meta**: Habilitar la interacción del tercer actor del sistema en el flete agrícola.
1.  **Construcción de la Interfaz**:
    *   Reemplazar [DashboardPendiente.vue](file:///c:/Users/Luis%20Alfonso/AgroConet/src/vistas/DashboardPendiente.vue) por una pantalla integral de administración logística.
    *   Diseñar tarjetas de control, paneles de búsqueda y tablas responsivas orientadas a la agencia.
2.  **Lógica de Operación**:
    *   Permitir que la agencia visualice las órdenes de compra en estado `"confirmado"`.
    *   Desarrollar componentes interactivos para actualizar el estado del flete a `"en puerto"` o `"en tránsito"`, exigiendo ingresar una bitácora o descripción del evento (ej: *"El cargamento ha zarpado de Puerto Cortés en el contenedor HL-992"*).

### 📈 Fase 4: Características Avanzadas y Optimización
*   **Meta**: Transformar AgroConet en un producto comercial de alta tecnología.
1.  **Integración de Precios de Commodities Reales**:
    *   Reemplazar las estimaciones deterministas del catálogo por un servicio proxy en el backend que consulte APIs globales (como Commodities-API) para mostrar la cotización real diaria del saco de café, maíz o arroz en la bolsa de Nueva York.
2.  **Seguimiento Satelital y Trazabilidad Visual**:
    *   Integrar un mapa (ej: Leaflet o Google Maps) en la vista de seguimiento utilizando las coordenadas de latitud/longitud de las fincas y los puertos para dar visualización geográfica al comprador de la ruta física que recorre su alimento.
3.  **Auditoría y Monitoreo**:
    *   Establecer logs detallados de transacciones monetarias y registrar errores del backend en una plataforma de telemetría (como Sentry).

---

## 4. Resumen Visual de Prioridades y Gaps

| Componente | Estado Actual | Clasificación | Acción Inmediata |
| :--- | :--- | :--- | :--- |
| **Seguridad** | Client-side (mock en frontend) | 🔴 Crítico | Cifrado con bcrypt y autenticación JWT real en base de datos. |
| **Middleware Backend** | Incompleto (gaps en variables de rol `g`) | 🔴 Crítico | Configurar `g.current_user_type` y proteger rutas de token. |
| **Lógica del Negocio** | Inexistente (NotImplementedError) | 🟡 Alto | Implementar consultas SQL, mutaciones de inventario y pedidos. |
| **Agencia Logística** | Vista vacía (placeholder) | 🟡 Alto | Crear la interfaz completa y los endpoints de actualización de fletes. |
| **Precios de Commodities**| Estimados estáticamente | 🟢 Medio | Conectar con APIs financieras globales de commodities en tiempo real. |
| **Mapa de Trazabilidad**| Visualización en timeline de texto | 🟢 Bajo | Integrar mapa interactivo con las coordenadas geográficas de los lotes. |

---

*Informe compilado y estructurado para su revisión técnica y planificación de sprints.*
