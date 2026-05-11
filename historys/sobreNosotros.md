### Historia de Usuario US-016
**Implementar la vista "Quiénes Somos" con diseño emocional y profesional**
**Como** visitante de la aplicación (potencial comprador o productor)  
**Quiero** tener una página clara y atractiva que explique quiénes somos y por qué existe AgroConet  
**Para** generar confianza, entender la misión y sentirme motivado a registrarme o explorar el catálogo

**Criterios de Aceptación**

**Escenario 1: Carga inicial y estructura visual**
Dado que el usuario accede a la ruta /quienes-somos  
Cuando la página carga  
Entonces:
- Se muestra una animación de entrada suave (2–4 segundos): fade-in + slide-up de secciones, con fondo gradiente crema-verde o imagen sutil de finca/café/maíz
- Hero section full-width (80–100% viewport inicial en móvil): 
  - Imagen o ilustración grande de agricultores trabajando + compradores recibiendo productos
  - Título principal: “Quiénes Somos – Conectando el campo directo con el mundo”
  - Subtítulo: “Una plataforma nacida en Centroamérica para eliminar intermediarios y dar voz a los productores reales”
  - CTA grande: “Explorar catálogo” → /catalogo y “Unirse como productor” → /registro?rol=productor

**Escenario 2: Secciones clave de contenido (orden descendente)**
La página debe tener al menos estas secciones con transiciones suaves al hacer scroll:

1. **Nuestra Misión**  
   - Texto breve (3–5 líneas): “En AgroConet creemos que el café, maíz y granos básicos deben llegar directamente del productor al comprador. Sin intermediarios innecesarios, con precios justos y trazabilidad total.”
   - Ícono o ilustración central (corazón + cadena rota o mano agricultor → mano comprador)

2. **Nuestra Historia / Origen**  
   - Narrativa corta: “Nacimos en Honduras en 2025, inspirados en caficultores de Santa Bárbara que perdían hasta 40% de su ganancia por intermediarios. Hoy conectamos fincas de toda Centroamérica con tostadores, molinos y familias en el mundo.”
   - Timeline simple horizontal (mobile: vertical) con 3–4 hitos (ej: “Idea 2025”, “Primer lote vendido 2026”, “+500 productores conectados”)

3. **Valores Principales**  
   - 4–5 cards o bloques con ícono + título + descripción corta:
     - Transparencia (precios reales y trazabilidad)
     - Justicia (precios justos para productores)
     - Sostenibilidad (apoyo a certificaciones orgánicas)
     - Comunidad (conexión directa campo-mesa)
     - Innovación (tecnología accesible para agricultores)

4. **Equipo / Fundadores** (opcional pero recomendado para confianza)  
   - 2–3 perfiles simples: foto (placeholder o ilustración), nombre, rol, frase corta (“Caficultor de 3ª generación”, “Tostador con 15 años de experiencia”)

5. **Impacto Actual**  
   - Estadísticas visuales (contadores animados o cards):
     - +X productores conectados
     - +Y quintales vendidos
     - Z países alcanzados
   - Fuente: “Datos propios – Marzo 2026”

6. **CTA Final**  
   - Sección grande al final: “¿Listo para ser parte del cambio?”
   - Dos botones grandes: “Explorar productos” y “Registrarme como productor”

**Escenario 3: Diseño y experiencia**
- Estilo consistente con el resto de la app: glassmorphism sutil en cards/secciones, gradientes agro (verde-tierra), sombras suaves
- Animaciones: fade-in al scroll (usar Intersection Observer o Framer Motion), contadores animados (de 0 a valor real)
- Responsive total: en móvil las secciones se apilan, texto legible (>16px), padding generoso
- Accesibilidad: alt en imágenes, aria-label en botones, contraste WCAG AA

**Escenario 4: Contenido estático o semi-dinámico**
- Todo el texto puede venir de un JSON local (src/data/quienes-somos.json) o hardcodeado en la vista
- Opcional futuro: cargar desde Supabase o API para editar fácilmente

**Notas**
- Esta vista es pública (sin login requerido)
- Enfocada en generar confianza y emoción (imágenes reales o ilustraciones de fincas, agricultores sonrientes, granos)
- Usa librerías ya presentes: Tailwind, Framer Motion (para animaciones)
- Inspiración visual: páginas “About Us” de Notion, Fair Trade apps, o plataformas como Kiva.org / Mercado Libre Rural

**Tareas**
TK-016-01 Crear vistas/QuienesSomos.vue con estructura base y hero section
TK-016-02 Implementar animación de entrada y fade-in por sección
TK-016-03 Diseñar y maquetar sección Misión + Historia (timeline)
TK-016-04 Crear cards de Valores con íconos e ilustraciones
TK-016-05 Añadir sección Impacto con contadores animados
TK-016-06 Implementar CTA final con botones grandes
TK-016-07 Asegurar responsive + accesibilidad básica
TK-016-08 Agregar enlace en Navbar: “Quiénes Somos” → /quienes-somos
TK-016-09 Commit: “US-016: Vista Quiénes Somos implementada con diseño emocional”

**Prioridad**  
Media-Alta – Ayuda a convertir visitantes en usuarios registrados

**Dependencias**  
- US-014 (Header/Navbar con enlace a esta ruta)
- Componentes reutilizables ya existentes (cards, botones)