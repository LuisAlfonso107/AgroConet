### Historia de Usuario US-015
**Implementar el Catálogo de Productos con integración de APIs gratuitas para datos reales**
**Como** usuario de la aplicación (comprador o visitante)  
**Quiero** ver un catálogo dinámico y actualizado de productos agrícolas (café, maíz, frijol, etc.)  
**Para** obtener información realista y útil (precios actuales, clima relacionado, estadísticas de producción) y decidir qué comprar o explorar

**Criterios de Aceptación**

**Escenario 1: Carga inicial del catálogo**
Dado que el usuario accede a la ruta /catalogo  
Cuando la página se carga  
Entonces:
- Se muestra un grid responsive de cards de productos (mobile: 1 columna, tablet: 2, desktop: 3–4)
- Cada card incluye al menos: foto (de db.json o API), nombre, región/finca, precio por quintal (de API real si disponible), humedad/variedad (de db.json), botón “Ver detalles”
- Loading spinner o skeleton cards mientras se cargan datos
- Filtros básicos superiores o laterales: por tipo de grano (Café, Maíz, Frijol, Arroz), región, precio (rango), certificaciones

**Escenario 2: Integración de APIs gratuitas para enriquecer el catálogo**
Dado que el catálogo está cargando  
Cuando se obtienen los datos base de db.json  
Entonces se enriquecen automáticamente con llamadas a APIs gratuitas:
- Precios actuales o promedio de commodities (maíz, café, frijol) → desde Commodities-API o API Ninjas (free tier)
  - Mostrar en cada card: “Precio mercado hoy: $XXX/quintal” (con fuente y fecha)
- Datos climáticos recientes de la región del producto → desde Open-Meteo (sin key)
  - Mostrar ícono + texto: “Temperatura suelo actual: 22°C | Humedad: 78%” (para estimar calidad de cosecha)
- Estadísticas históricas o producción por país/región → desde FAOSTAT o USDA Quick Stats (si se obtiene key)
  - Opcional en card o tooltip: “Producción Honduras 2025: 1.2M qq de café”
- Si falla la API → fallback a datos mock de db.json + mensaje sutil “Datos de mercado aproximados”

**Escenario 3: Detalle de producto enriquecido**
Dado que el usuario hace clic en una card  
Cuando abre /producto/:id  
Entonces:
- Muestra ficha completa: fotos, descripción, variedad, altura, humedad, certificaciones (de db.json)
- Sección adicional “Mercado y Clima”:
  - Precio real-time del commodity relacionado (ej: “Café Caturra: $328/quintal hoy – fuente: Commodities-API”)
  - Clima local reciente (Open-Meteo)
  - Estadística breve (ej: “Producción promedio en Santa Bárbara: X quintales/ha – fuente: FAOSTAT”)
- Botones: “Hacer pedido”, “Contactar productor”, “Agregar a favoritos” (si logueado)

**Escenario 4: Filtros y búsqueda**
Dado que el usuario está en el catálogo  
Cuando aplica filtros o busca  
Entonces:
- Filtros reactivos (usar composable useFiltrosProductos.js)
- Búsqueda por nombre/región/variedad (input con debounce)
- Paginación o infinite scroll si hay muchos productos

**Escenario 5: Rendimiento y manejo de errores**
- Caché simple (localStorage o Pinia) para evitar llamadas repetidas a APIs
- Error handling: si API falla → mostrar datos de db.json + toast “Datos de mercado no disponibles en este momento”
- Loading progresivo: primero db.json, luego enriquecimiento con APIs
- Mobile-first: cards cuadradas, touch-friendly, filtros colapsables

**Notas**
- Priorizar APIs sin key o con free tier generoso: Open-Meteo (clima), Commodities-API / API Ninjas (precios), FAOSTAT (estadísticas)
- No exceder límites free (ej: 1,000 llamadas/día en OpenWeather si se usa)
- En fase 1: fallback siempre a db.json para desarrollo offline
- Composable recomendado: useCatalogoProductos.js (fetch db.json + APIs paralelas con Promise.all)
- Librerías opcionales: axios o fetch, date-fns para formateo de fechas
- Inspiración visual: catálogos como Mercado Libre, Etsy o plataformas agrícolas (cards limpias, precios destacados)

**Tareas**
TK-015-01 Crear vistas/CatalogoProductos.vue con grid responsive y skeleton loading
TK-015-02 Implementar composable useCatalogoProductos.js (fetch db.json + APIs)
TK-015-03 Integrar al menos 1 API de precios (Commodities-API o API Ninjas) en cada card
TK-015-04 Añadir datos climáticos con Open-Meteo (por región del producto)
TK-015-05 Implementar filtros básicos (tipo grano, región, precio) con composable useFiltrosProductos.js
TK-015-06 Crear vistas/DetalleProducto.vue con sección “Mercado y Clima” enriquecida
TK-015-07 Manejo de errores y fallback a db.json
TK-015-08 Pruebas: catálogo carga offline, APIs enriquecen cuando hay conexión
TK-015-09 Commit: “US-015: Catálogo dinámico con APIs gratuitas implementado”

**Prioridad**  
Alta – El catálogo es el corazón de la app para compradores y visitantes

**Dependencias**  
- US-002 (versión inicial del catálogo mock)
- US-014 (Header con enlace a /catalogo)

**APIs recomendadas para empezar YA**
1. Open-Meteo (clima) – sin key: https://open-meteo.com/
2. Commodities-API (precios) – free tier con key: https://commodities-api.com
3. FAOSTAT (estadísticas) – gratis: https://www.fao.org/faostat/en/#data