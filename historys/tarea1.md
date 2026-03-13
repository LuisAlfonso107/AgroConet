
---

### Historia de Usuario US-001
**Visualizar Landing Page (Home)**
Como visitante  
Quiero ver la pantalla principal de la aplicación  
Para entender qué es GranoDirecto y acceder rápidamente a las secciones principales

**Criterios de Aceptación**  
Escenario 1: Carga inicial  
Dado que el usuario abre la app  
Cuando carga la página Home  
Entonces se muestra un hero con foto de finca de café, título “Del campo al comprador directo”, botón “Explorar catálogo” y botón “Soy productor”  

Escenario 2: Secciones destacadas  
Entonces aparecen 3 cards grandes: “Catálogo de productos”, “Para productores” y “Para compradores” con imágenes reales  

**Notas**  
• Usa datos estáticos + 2 productos destacados del json-server  
• Responsive mobile-first (agricultores usan celular en el campo)

**Tareas**  
TK-001-01 Crear vistas/Home.vue  
TK-001-02 Implementar hero y cards de acceso rápido  
TK-001-03 Conectar botón “Explorar catálogo” a ruta /catalogo

---

### Historia de Usuario US-002
**Visualizar Catálogo de Productos**
Como usuario (comprador o productor)  
Quiero ver todos los productos agrícolas disponibles  
Para poder explorar café, maíz, arroz, frijol, etc.

**Criterios de Aceptación**  
Escenario 1: Carga del catálogo  
Dado que el usuario accede a /catalogo  
Cuando se carga la vista  
Entonces se muestran cards cuadradas (misma altura) con foto, nombre, precio por quintal, humedad y región  

Escenario 2: Filtros  
Entonces puede filtrar por tipo (café/maíz/etc.), región, precio y certificaciones  

**Notas**  
• Datos vienen de /productos en db.json  
• Orden alfabético por defecto

**Tareas**  
TK-002-01 Crear vistas/CatalogoProductos.vue  
TK-002-02 Implementar grid responsive de cards  
TK-002-03 Añadir filtros laterales o superior

---

### Historia de Usuario US-003
**Ver Detalle de un Producto**
Como usuario  
Quiero hacer clic en cualquier card del catálogo  
Para ver toda la ficha técnica del lote de café o maíz

**Criterios de Aceptación**  
Escenario 1: Navegación  
Dado que estoy en el catálogo  
Cuando hago clic en una card  
Entonces se abre vistas/DetalleProducto.vue con el id en la URL  

Escenario 2: Información completa  
Entonces veo: foto grande, nombre, variedad, altura, humedad, taza (si es café), defectos, precio, kg disponibles, botón “Hacer pedido” y botón “Contactar productor”

**Notas**  
• Recibe parámetro :id  
• Depende de US-002

**Tareas**  
TK-003-01 Crear vistas/DetalleProducto.vue  
TK-003-02 Mostrar toda la información del producto  
TK-003-03 Preparar botón “Hacer pedido”

---

### Historia de Usuario US-004
**Ver Perfil Público de Productor**
Como usuario  
Quiero ver el perfil de un productor  
Para conocer su finca y confianza antes de comprar

**Criterios de Aceptación**  
Escenario 1: Acceso desde detalle  
Dado que estoy en DetalleProducto  
Cuando hago clic en “Ver perfil del productor”  
Entonces se abre vistas/PerfilProductor.vue con id del productor  

Escenario 2: Información  
Entonces veo nombre, ubicación, calificación, foto de finca, lista de otros productos que vende y contacto WhatsApp

**Tareas**  
TK-004-01 Crear vistas/PerfilProductor.vue  
TK-004-02 Mostrar datos de /productores del json-server

---

### Historia de Usuario US-005
**Dashboard del Productor**
Como agricultor/productor  
Quiero tener mi panel personal  
Para gestionar mis productos y ver mis ventas

**Criterios de Aceptación**  
Escenario 1: Acceso  
Dado que inicio sesión como productor  
Cuando entro al dashboard  
Entonces veo mis productos publicados, stock actual y pedidos recibidos  

**Tareas**  
TK-005-01 Crear vistas/DashboardProductor.vue  
TK-005-02 Mostrar tabla de mis productos

---

### Historia de Usuario US-006
**Publicar Nuevo Producto**
Como productor  
Quiero agregar un nuevo lote de café o maíz  
Para que aparezca en el catálogo

**Criterios de Aceptación**  
Escenario 1: Formulario  
Dado que estoy en mi dashboard  
Cuando hago clic en “Publicar nuevo producto”  
Entonces se abre vistas/NuevoProducto.vue con formulario completo (nombre, tipo, humedad, kg, precio, fotos, etc.)

**Tareas**  
TK-006-01 Crear vistas/NuevoProducto.vue  
TK-006-02 Formulario con todos los campos que existen en db.json

---

### Historia de Usuario US-007
**Dashboard del Comprador**
Como comprador (tostador, molino, tienda)  
Quiero ver mis pedidos y estado  
Para saber qué está en camino

**Criterios de Aceptación**  
Escenario 1: Lista de pedidos  
Entonces veo tabla con pedidos en curso, pendientes y finalizados

**Tareas**  
TK-007-01 Crear vistas/DashboardComprador.vue

---

### Historia de Usuario US-008
**Ver Mis Pedidos**
Como comprador o productor  
Quiero ver todos mis pedidos  
Para seguir el proceso completo

**Tareas**  
TK-008-01 Crear vistas/MisPedidos.vue

---

### Historia de Usuario US-009
**Ver Detalle de Pedido**
Como cualquier usuario  
Quiero ver el detalle completo de un pedido  
Para ver cantidad, precio, estado y agencia asignada

**Tareas**  
TK-009-01 Crear vistas/DetallePedido.vue

---

### Historia de Usuario US-010
**Tracking / Seguimiento de Pedido**
Como comprador o productor  
Quiero ver el estado en tiempo real  
Para saber si ya salió del puerto, está en tránsito o llegó

**Criterios de Aceptación**  
Escenario 1: Estados visuales  
Entonces veo timeline: Pendiente → Aprobado → En puerto → En tránsito → Entregado + alertas de agencia

**Tareas**  
TK-010-01 Crear vistas/TrackingPedido.vue

---

### Historia de Usuario US-011
**Dashboard de Agencia Exportadora**
Como agencia (Exportadora Cafetalera HN)  
Quiero ver todos los pedidos que debo gestionar  
Para actualizar estados, documentos y notificar a ambas partes

**Criterios de Aceptación**  
Escenario 1: Lista de pedidos pendientes  
Entonces veo tabla con pedidos asignados + botón para cambiar estado

**Tareas**  
TK-011-01 Crear vistas/DashboardAgencia.vue

---

### Historia de Usuario US-012 y US-013
**Login y Registro**  
(Se crean vistas/Login.vue y Registro.vue con selección de rol: Productor / Comprador / Agencia)

---

## Kanban del Proyecto - Vistas (Sprint 1 - Frontend)

**Tareas Preparadas**  
**Backlog (pendientes de Sprint 1)**  
- TK-001-01 Crear vistas/Home.vue  
- TK-002-01 Crear vistas/CatalogoProductos.vue  
- TK-003-01 Crear vistas/DetalleProducto.vue  
- TK-004-01 Crear vistas/PerfilProductor.vue  
- TK-005-01 Crear vistas/DashboardProductor.vue  
- TK-006-01 Crear vistas/NuevoProducto.vue  
- TK-007-01 Crear vistas/DashboardComprador.vue  
- TK-008-01 Crear vistas/MisPedidos.vue  
- TK-009-01 Crear vistas/DetallePedido.vue  
- TK-010-01 Crear vistas/TrackingPedido.vue  
- TK-011-01 Crear vistas/DashboardAgencia.vue  

**Doing**  
(nada aún)

**Done**  
(nada aún)

---

**Instrucciones finales para ti:**  
1. Crea la carpeta `src/vistas/`  
2. Abre este archivo markdown  
3. Ve una por una las historias en orden (US-001 primero)  
4. Crea el archivo .vue correspondiente y marca la tarea como Done cuando termines la vista  

Cuando termines las primeras 4 vistas (Home, Catálogo, Detalle y Perfil), me avisas y te paso la siguiente fase (rutas con Vue Router + Pinia para los roles).

¡Listo! Ahora tienes el mapa completo y ordenado de TODAS las vistas que necesita tu app.  
¿Quieres que te genere el siguiente bloque (rutas + navegación) o empezamos creando la primera vista paso a paso sin código? Dime y seguimos. ☕🚀