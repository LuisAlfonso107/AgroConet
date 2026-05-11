### Historia de Usuario US-017
**Implementar dentro de la vista "Cómo Funciona" con explicación clara, visual y paso a paso**
**Como** visitante o usuario nuevo (productor o comprador)  
**Quiero** tener una página que explique de forma sencilla y visual cómo funciona la plataforma  
**Para** entender rápidamente el proceso, sentirme seguro y decidir si registrarme o explorar más

**Criterios de Aceptación**

**Escenario 1: Carga inicial y diseño general**
Dado que el usuario accede a la ruta /como-funciona  
Cuando la página carga  
Entonces:
- Animación de entrada suave (2–4 segundos): fade-in + slide-up secuencial de secciones
- Hero section impactante (full-width, 70–90% viewport inicial en móvil):
  - Imagen o ilustración dinámica: flujo simple (finca → productor → plataforma → comprador → entrega)
  - Título principal: “Cómo Funciona AgroConet – Simple, directo y transparente”
  - Subtítulo: “Del campo a tu mesa en pocos pasos. Sin intermediarios caros, con trazabilidad total.”
  - CTA grande: “Explorar catálogo ahora” → /catalogo

**Escenario 2: Secciones paso a paso (flujo visual principal)**
La página debe tener una sección central con 4–6 pasos claros, visualmente guiados:

1. **Paso 1: Regístrate gratis**  
   - Texto: “Crea tu cuenta en 1 minuto. Elige si eres Productor o Comprador.”
   - Ilustración: celular con formulario + ícono de rol (finca vs taza de café)
   - Botón pequeño: “Registrarme” → /registro

2. **Paso 2: Publica o busca productos**  
   - Para productores: “Sube fotos reales de tu cosecha, precio, humedad y certificaciones.”
   - Para compradores: “Explora el catálogo con filtros por variedad, región y precio.”
   - Ilustración: grid de cards de productos + agricultor subiendo foto

3. **Paso 3: Conecta directamente**  
   - Texto: “Contacta al productor o comprador vía WhatsApp o mensaje interno. Negocia precio y cantidad sin intermediarios.”
   - Ilustración: chat bubbles + manos estrechándose

4. **Paso 4: Gestiona tu pedido**  
   - Texto: “Crea el pedido, confirma detalles y paga seguro (próximamente).”
   - Ilustración: carrito → factura → seguimiento

5. **Paso 5: Trazabilidad completa**  
   - Texto: “Sigue tu pedido en tiempo real: desde la finca, puerto, hasta entrega. Agencias exportadoras actualizan estados.”
   - Ilustración: timeline horizontal o mapa simple con íconos (finca → puerto → destino)

6. **Paso 6: Recibe y disfruta**  
   - Texto: “Recibe tu café o maíz fresco. Califica la transacción y ayuda a mejorar la comunidad.”
   - Ilustración: saco llegando + estrellas de calificación

Cada paso debe ser una card o bloque con:
- Número grande (1, 2, 3...)
- Ícono o ilustración central
- Título corto + descripción 1–2 líneas
- Animación al scroll (fade-in o slide desde izquierda/derecha alternado)

**Escenario 3: Secciones complementarias**
- **Beneficios clave** (después de los pasos): 4–5 íconos con texto breve
  - Precios justos
  - Trazabilidad real
  - Sin intermediarios
  - Comunidad fuerte
  - Fácil desde tu celular
- **Preguntas frecuentes (FAQ)** (acordeón colapsable):
  - ¿Es gratis registrarse?
  - ¿Cómo se pagan los productos?
  - ¿Qué hago si hay problemas?
  - ¿Funciona en zonas con internet lento?
- **CTA final grande**: “¿Listo para empezar?” con botones “Explorar catálogo” y “Registrarme”

**Escenario 4: Diseño y experiencia**
- Estilo premium consistente: glassmorphism en cards, gradientes verde-tierra, sombras suaves
- Animaciones ligeras: fade-in al scroll, números animados, hover glow en cards
- Mobile-first: pasos apilados verticalmente, texto legible (>16px), padding amplio
- Accesibilidad: alt en ilustraciones, aria-label en botones, contraste WCAG AA
- Responsive: en desktop pasos en grid o timeline horizontal, en móvil vertical

**Escenario 5: Contenido flexible**
- Todo texto en JSON local (src/data/como-funciona.json) o hardcodeado
- Ilustraciones: placeholders de Unsplash o SVG gratuitos (finca, celular, timeline)
- Opcional: carrusel de testimonios cortos (fase futura)

**Notas**
- Página pública (sin login)
- Enfocada en simplicidad y confianza (imágenes reales de campo, texto en español claro)
- Usa Tailwind + Framer Motion para animaciones (ya presente en login/registro)
- Inspiración: páginas “How it works” de Airbnb, Rappi, o plataformas como Kiva / Fair Trade

**Tareas**
TK-017-01 Crear vistas/ComoFunciona.vue con hero y estructura base
TK-017-02 Implementar animación de entrada y fade-in por scroll
TK-017-03 Diseñar sección de pasos con cards/timeline visual
TK-017-04 Añadir sección Beneficios con íconos
TK-017-05 Implementar FAQ acordeón colapsable
TK-017-06 Crear CTA final con botones grandes
TK-017-07 Asegurar responsive + accesibilidad
TK-017-08 Agregar enlace en Navbar: “Cómo Funciona” → /como-funciona
TK-017-09 Commit: “US-017: Vista Cómo Funciona implementada”

**Prioridad**  
Media-Alta – Reduce dudas y aumenta conversiones de visitantes a usuarios

**Dependencias**  
- US-014 (Header con enlace a esta ruta)
- Componentes reutilizables (cards, botones, acordeón si existe)