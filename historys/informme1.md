# Informe de estado del proyecto AgroConet

## Fecha de evaluación

11 de mayo de 2026

## Resumen ejecutivo

AgroConet se encuentra en una fase de prototipo frontend avanzado. La base visual y de navegación ya existe: hay landing page, navbar responsive, catálogo, detalle de producto, registro, login, páginas informativas y formulario de contacto. El proyecto usa Vue 3, Vite, Vue Router, Tailwind CSS 4, Axios y json-server como backend simulado.

El estado general es prometedor para una primera entrega de interfaz. Después de la intervención del 11 de mayo de 2026, la verificación de TypeScript y el build de producción pasan correctamente. El proyecto todavía no es un producto completo de marketplace, pero ya cuenta con una base funcional más estable: sesión mock, registro/login contra `json-server`, acciones mínimas de pedido/contacto/favorito y persistencia mock para formularios.

## Estado técnico actual

### Stack y configuración

- Proyecto Vue 3 con Composition API y Vite.
- Vue Router configurado con rutas para home, catálogo, detalle, registro, login, quienes somos, cómo funciona y contacto.
- Tailwind CSS 4 integrado desde `src/style.css`.
- json-server previsto en el puerto `3001` usando `db.json`.
- Axios centralizado en `src/composables/useApi.ts` con `baseURL: http://localhost:3001`.
- TypeScript está activo con configuración estricta.

### Verificaciones ejecutadas

- `npm run typecheck`: pasa correctamente.
- `npm run build`: pasa correctamente.

El error principal original del build era:

```text
Rolldown failed to resolve import "@/composables/useApi" from "src/componentes/Registro.vue"
```

Esto ocurría porque `Registro.vue` usaba el alias `@/composables/useApi`, pero `vite.config.ts` no definía el alias `@` hacia `src`. Se resolvió configurando el alias en `vite.config.ts` y añadiendo `baseUrl`/`paths` en `tsconfig.json`.

También se eliminó la referencia de build a `tsconfig.node.json` y se desactivó la emisión de artefactos de configuración duplicados (`vite.config.js` y `vite.config.d.ts`).

## Funcionalidades implementadas

### Home

La vista `src/vistas/Home.vue` contiene:

- Hero con imágenes rotativas.
- Mensaje principal orientado a conectar productores y compradores.
- CTAs hacia catálogo y registro de productor.
- Cards de valor para compradores, productores y trazabilidad.
- Sección de cosechas destacadas consumiendo `useProductos`.
- Fallback de productos cuando la API local no responde.
- Footer básico integrado en la misma vista.

Estado: funcional como landing, aunque todavía conviene limpiar código no usado como `mobileMenuOpen` y alinear textos/estilos con el resto del sistema.

### Navbar

`src/componentes/Navbar.vue` ya incluye:

- Navegación fija.
- Menú responsive móvil.
- Enlaces principales.
- Botones de catálogo, login y registro.
- Composable propio `useNavbar`.

Estado: avanzado y usable. Falta validar visualmente todas las rutas en móvil y homogeneizar el uso de iconos/emojis.

### Catálogo

`src/vistas/CatalogoProductos.vue` implementa:

- Grid responsive de productos.
- Skeleton loading.
- Filtros por búsqueda, tipo, región, precio y certificaciones.
- Cards con imagen, tipo, certificaciones, precio local, precio de mercado estimado y clima.
- Navegación al detalle del producto.
- Manejo básico de error y fallback visual.

`src/composables/useCatalogoProductos.ts` implementa:

- Carga desde `/db.json`.
- Cache en `localStorage`.
- Enriquecimiento con clima usando Open-Meteo.
- Precios de mercado estimados con fallback local.

Estado: es una de las partes más completas del proyecto. Los precios no vienen todavía de una API real de commodities; son estimados con variación determinista para evitar cambios aleatorios en cada carga. También se corrigió la sincronización de `productosEnriquecidos` para conservar clima y mercado al mismo tiempo.

### Detalle de producto

`src/vistas/DetalleProducto.vue` incluye:

- Ficha completa del producto.
- Imagen, productor, precio, certificaciones, variedad, humedad, altura y descripción.
- Sección de mercado y clima.
- Análisis rápido según tipo de producto.
- Botones de “Hacer pedido”, “Contactar productor” y “Favorito”.
- Trazabilidad inicial del producto.

Estado: visualmente avanzado y con acciones mínimas conectadas al mock API. Falta evolucionar el flujo hacia pedidos completos con cantidades, confirmación, estados y paneles por rol.

### Registro y login

`src/componentes/Registro.vue` incluye:

- Formulario con nombre, email, contraseña y tipo de usuario.
- Validación básica.
- POST a `/users` con Axios.
- Inicio de sesión local tras registro exitoso.
- Redirección al catálogo tras crear cuenta.

`src/componentes/Login.vue` incluye:

- Formulario visual de login.
- Campo email y contraseña.
- Botón social de Google como interfaz.
- Autenticación mock contra `/users`.
- Redirección al catálogo tras login correcto.

Estado: funcional como autenticación mock para desarrollo si `json-server` está corriendo. No debe considerarse autenticación segura de producción.

### Páginas informativas

Existen vistas para:

- `ComoFunciona.vue`
- `QuienesSomos.vue`
- `Contacto.vue`

Estado: visualmente trabajadas. Contacto tiene validación de formulario y ahora persiste mensajes en el recurso mock `mensajesContacto`. En `QuienesSomos.vue` se usa una directiva local de visibilidad que funciona como prototipo.

## Problemas y riesgos detectados

### Prioridad alta

1. La autenticación sigue siendo mock; todavía no hay backend real ni hashing de contraseñas.
2. La gestión por rol existe como base de sesión, pero faltan paneles específicos para productor, comprador y agencia.
3. Los botones de negocio ya tienen una acción mínima, pero falta un flujo completo de pedido con estados, cantidades editables y confirmación.
4. Los precios de mercado siguen siendo estimados, no vienen de una API real de commodities.
5. Falta una suite de pruebas automatizadas.

### Prioridad media

1. Hay componentes antiguos o placeholders como `src/componentes/Catalogo.vue` y `src/componentes/ProductoDetalle.vue`.
2. La arquitectura documentada habla de `src/components`, pero el proyecto usa `src/componentes`; conviene unificar criterio.
3. El catálogo usa `/db.json` desde public root, mientras otras partes usan `http://localhost:3001/productos`. Esto genera dos modelos de datos y ejecución distintos.
4. Falta una estrategia clara de entorno: variables `.env`, URLs de API y modo offline.

### Prioridad baja

1. Hay textos y estilos con emojis mezclados con UI formal; se puede pulir después de estabilizar funcionalidad.
2. Algunas imágenes dependen de URLs externas de Unsplash.
3. Falta revisar accesibilidad completa: labels, contraste, foco, navegación por teclado y estados de error.

## Estado frente a las historias actuales

### US-015 Catálogo con APIs gratuitas

Estado: parcialmente completada.

Completado:

- Vista de catálogo responsive.
- Skeleton loading.
- Filtros básicos.
- Detalle de producto enriquecido.
- Open-Meteo integrado para clima.
- Fallback a datos locales.
- Cache local.

Pendiente:

- Integración real de precios con Commodities-API, API Ninjas u otra fuente equivalente.
- Estadísticas de producción con FAOSTAT/USDA si se decide mantener ese alcance.
- Paginación o infinite scroll.
- Toast o mensaje no invasivo cuando fallen datos externos.
- Prueba manual documentada con y sin conexión/API.

## Pasos a seguir recomendados

### 1. Reemplazar autenticación mock por autenticación real

- Crear backend real o servicio de autenticación.
- Hash de contraseñas y manejo de tokens/sesión segura.
- Guards de rutas por rol.

### 2. Ordenar arquitectura

- Eliminar o archivar placeholders que ya no se usan.
- Decidir si el proyecto trabajará con `componentes` en español o `components` en inglés, y actualizar la documentación.

### 3. Unificar la fuente de datos

- Elegir una estrategia para desarrollo:
  - usar siempre `json-server` (`http://localhost:3001`), o
  - usar `db.json` estático como fallback offline.
- Crear variables de entorno para la URL base de API.
- Mantener sincronizados los contratos de datos mock y los composables que los consumen.

### 4. Completar paneles por rol

- Productor: productos publicados, pedidos recibidos y edición de stock.
- Comprador: pedidos, favoritos y conversaciones.
- Agencia: pedidos asignados y actualización de tracking.

### 5. Completar flujo de marketplace

- Añadir cantidades editables, confirmación y resumen antes de crear pedido.
- Añadir estados reales de pedido: solicitado, aceptado, en preparación, enviado, entregado, cancelado.
- Crear historial o panel básico por rol.

### 6. Pulir catálogo

- Reemplazar precios estimados por una fuente real o dejar claro que son estimaciones.
- Añadir paginación si crece la cantidad de productos.
- Mejorar mensajes de error y estados vacíos.

### 7. Documentar y probar

- Mantener `README.md` actualizado con nuevas rutas, usuarios demo y scripts.
- Añadir checklist manual de pruebas por ruta.
- Considerar pruebas unitarias para composables y pruebas de interfaz para flujos críticos.

## Conclusión

AgroConet ya tiene una base frontend sólida para demostrar la idea del marketplace agrícola. El catálogo, el detalle de producto y las páginas informativas muestran claramente la visión del producto. Después de la intervención, el build está estabilizado y varias acciones simuladas pasaron a tener persistencia mock.

La prioridad inmediata ya no es corregir compilación, sino avanzar desde mock frontend hacia producto: backend real, seguridad, paneles por rol, pedidos completos, trazabilidad y pruebas automatizadas.

## Proceso de resolución aplicado

### Cambios realizados el 11 de mayo de 2026

1. Se corrigió el build de producción configurando el alias `@` en `vite.config.ts` y los paths en `tsconfig.json`.
2. Se eliminó la emisión de configuraciones duplicadas de Vite quitando la referencia de build a `tsconfig.node.json`, manteniendo `vite.config.ts` como única fuente.
3. Se creó `src/composables/useAuth.ts` para centralizar sesión, usuario actual, rol, login, logout y persistencia en `localStorage`.
4. Se creó `src/composables/useMarketplaceActions.ts` para centralizar acciones de negocio: pedido, contacto con productor y favoritos.
5. Se conectó `Registro.vue` con validación de contraseña, prevención de emails duplicados, alta en `/users` e inicio de sesión tras registro.
6. Se conectó `Login.vue` con autenticación mock contra `/users`.
7. Se crearon vistas wrapper `src/vistas/Registro.vue` y `src/vistas/Login.vue` para que el router cargue vistas y no componentes directamente.
8. Se conectó `DetalleProducto.vue` a las acciones reales mock: hacer pedido, contactar productor y guardar/quitar favorito.
9. Se añadió una sección de trazabilidad inicial en el detalle del producto.
10. Se corrigió `useCatalogoProductos.ts` para que clima y mercado no se sobrescriban en `productosEnriquecidos`.
11. Se reemplazó la variación aleatoria de precios estimados por una variación determinista.
12. Se conectó el formulario de `Contacto.vue` al recurso mock `/mensajesContacto`.
13. Se amplió `db.json` con `users`, `pedidos`, `contactos`, `mensajesContacto`, `favoritos` y `tracking`.
14. Se actualizó `README.md` con instalación, scripts, API mock y usuarios demo.
15. Se limpió código no usado en `Home.vue`.

### Principios SOLID aplicados

- Responsabilidad única: la sesión quedó en `useAuth`, las acciones de marketplace en `useMarketplaceActions` y las vistas se limitan a orquestar UI.
- Abierto/cerrado: los composables permiten ampliar acciones o proveedores de autenticación sin reescribir las vistas.
- Sustitución de dependencias: la API se sigue consumiendo mediante `useApi`, lo que permite cambiar la base mock por un backend real con menor impacto.
- Segregación de interfaces: cada composable expone solo lo que la pantalla necesita.
- Inversión de dependencias: las vistas dependen de abstracciones locales (`useAuth`, `useMarketplaceActions`, `useApi`) y no de llamadas HTTP dispersas.

### Verificaciones finales

- `npm run typecheck`: correcto.
- `npm run build`: correcto.

### Limitaciones que quedan

- La autenticación es solo mock y no es segura para producción.
- Los precios de commodities siguen siendo estimados.
- Los pedidos todavía son mínimos: falta cantidad editable, confirmación, estados completos y paneles por rol.
- No se añadieron pruebas automatizadas todavía.
