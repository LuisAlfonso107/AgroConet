
---

### Historia de Usuario US-001
**Visualizar Landing Page (Home) – Pantalla de bienvenida principal**
**Como** visitante (potencial comprador o productor agrícola)  
**Quiero** acceder a una pantalla de inicio atractiva, clara y rápida de cargar  
**Para** entender inmediatamente qué es la plataforma, confiar en ella y decidir si quiero explorar como comprador o registrarme/publicar como productor

**Criterios de Aceptación**

**Escenario 1: Carga inicial – Hero section impactante (mobile & desktop)**
Dado que el usuario abre la aplicación por primera vez (en móvil o desktop)  
Cuando la página Home se carga completamente  
Entonces:
- Se muestra un **hero section** ocupando al menos el 80-90% del viewport inicial (full-width en móvil)
- El hero incluye un **carrusel o fondo dinámico** con 3–5 imágenes reales y de alta calidad rotando automáticamente (cada 6–8 segundos):
  - Fotos de fincas de café en cosecha, granos de maíz secando al sol, sacos en finca, manos recolectando, paisaje rural auténtico
  - **No** usar fotos stock genéricas; simular con imágenes placeholder realistas (puedes usar Unsplash o db.json con urls)
- Sobre las imágenes aparece texto grande y legible (contraste alto WCAG AA):
  - Título principal: “Del campo directo a tu negocio o mesa”
  - Subtítulo: “Conecta productores agrícolas con compradores honestos. Café, maíz, frijol y más – sin intermediarios innecesarios.”
- Dos **CTAs principales prominentes** y diferenciados visualmente:
  - Botón primario (verde/agro, grande): “Explorar productos disponibles” → lleva a /catalogo
  - Botón secundario (outline o color tierra): “Soy productor – publica tu cosecha” → lleva a /registro?rol=productor o directamente a login/registro con rol preseleccionado
- En móvil: los botones se apilan verticalmente, texto se reduce pero sigue legible (>16px), padding generoso para dedos

**Escenario 2: Secciones de valor rápido debajo del hero**
Dado que el usuario ha hecho scroll después del hero  
Cuando visualiza las primeras secciones  
Entonces aparecen al menos 3 bloques/cards horizontales o en columna (en móvil se apilan):
- Card 1 – “Para compradores”:
  - Icono/título: “Encuentra granos de calidad directo de finca”
  - Texto breve: “Variedades, taza, humedad, certificaciones, precios transparentes. Compra por quintal o contenedor.”
  - Imagen: tostador revisando granos o sacos listos para envío
  - Botón: “Ver catálogo ahora” → /catalogo
- Card 2 – “Para productores”:
  - Icono/título: “Vende sin intermediarios caros”
  - Texto breve: “Publica tu café, maíz o frijol. Llega a tostadores, molinos y exportadores. Controla precios y condiciones.”
  - Imagen: agricultor con celular en finca subiendo foto
  - Botón: “Comenzar a vender” → /registro?rol=productor
- Card 3 – “Trazabilidad y confianza”:
  - Icono/título: “Seguimiento completo + conexión real”
  - Texto breve: “Agencias exportadoras actualizan estados. Sabes dónde está tu pedido o tu compra en todo momento.”
  - Imagen: mapa simple o timeline de embarque
  - Botón sutil: “Cómo funciona” → futura página estática o modal

**Escenario 3: Productos destacados (social proof inicial)**
Dado que el usuario sigue scrolleando  
Cuando llega a la sección “Cosechas destacadas”  
Entonces se muestran 2–4 cards de productos reales traídos de json-server (/productos?_limit=4&estado=disponible&_sort=createdAt&_order=desc):
- Cada card muestra: foto principal, nombre (“Café Caturra Orgánico – Finca La Esperanza”), precio por quintal, región, humedad, calificación promedio del productor
- En móvil: scroll horizontal o grid 1 columna
- CTA en cada card: “Ver detalles” → /producto/:id

**Escenario 4: Rendimiento y accesibilidad básica (mobile-first obligatorio)**
- La página debe cargar en < 3 segundos en 3G (imágenes optimizadas, lazy loading en secciones bajas)
- Todo texto legible en móvil (mínimo 16px body, 24–32px títulos)
- Contraste suficiente en textos sobre imágenes
- Navegación superior mínima (solo logo + menú hamburguesa con “Catálogo”, “Iniciar sesión”, “Registro”)

**Notas**
- Prioridad absoluta: **mobile-first** – la mayoría de productores acceden desde celulares Android económicos en zonas rurales con internet lento.
- Usa datos estáticos para textos e imágenes del hero; solo los productos destacados vienen de json-server.
- Evita animaciones pesadas en hero para no afectar performance.
- Colores sugeridos iniciales: verde agrícola (#2E7D32 / #4CAF50), tierra (#8D6E63), blanco/crema fondo, acentos naranja/amarillo cosecha.
- En fase 1 no implementar login real; los botones de “Soy productor” pueden ir a una vista Registro.vue con select de rol.

**Tareas (orden sugerido)**
- TK-001-01 Crear el archivo vistas/Home.vue y definir estructura base (sections)
- TK-001-02 Implementar hero section con fondo/imágenes rotativas + overlay texto + 2 CTAs principales
- TK-001-03 Diseñar y maquetar las 3 cards de valor (“Para compradores”, “Para productores”, “Trazabilidad”)
- TK-001-04 Crear sección “Cosechas destacadas” con fetch a json-server (/productos) y renderizar 4 cards
- TK-001-05 Asegurar responsive design + mobile-first (usar media queries o Tailwind/Bootstrap si lo usas)
- TK-001-06 Conectar botón “Explorar productos” a ruta /catalogo (preparar placeholder si router no está aún)
- TK-001-07 Optimizar imágenes (lazy loading, tamaños adecuados) y probar carga en red lenta (Chrome DevTools)


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