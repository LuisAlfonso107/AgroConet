### Historia de Usuario US-014
**Diseñar e implementar el Header (barra de navegación superior) con enfoque premium y mobile-first**
**Como** usuario de la aplicación (visitante, productor o comprador)  
**Quiero** tener una barra de navegación superior limpia, moderna, rápida y fácil de usar  
**Para** poder acceder rápidamente a las secciones principales de la app desde cualquier página, sin importar si estoy en móvil o desktop

**Criterios de Aceptación**

**Escenario 1: Diseño general y apariencia visual (premium y consistente)**
Dado que el usuario abre cualquier página de la aplicación  
Cuando carga la página  
Entonces el header debe cumplir con:
- Estar **fijo en la parte superior** (fixed o sticky) con fondo semi-transparente (backdrop-blur-md) y sombra sutil
- Usar **glassmorphism** ligero o fondo blanco/crema con transparencia para que combine con el hero y el resto del diseño
- Colores principales: verde agrícola (#2E7D32 o #4CAF50), crema (#FFF8E1), gris oscuro para textos secundarios
- Tipografía: sans-serif moderna (Inter o Roboto), títulos 1.5–2rem en desktop, legibles en móvil (>16px)
- Espaciado generoso: padding vertical 0.75–1rem, max-width 7xl (1280px) centrado
- Hover y focus states con glow sutil o scale(1.05) + transition 200–300ms

**Escenario 2: Elementos siempre visibles (independiente del estado de login)**
Dado que el usuario está navegando  
Entonces el header siempre muestra (de izquierda a derecha):
- **Logo/Marca** a la izquierda: “🌾 AgroConet” (texto + ícono pequeño), enlace a Home (/)
- En móvil: solo logo + ícono de hamburguesa a la derecha
- En desktop (md+): logo + enlaces principales horizontales + zona de acciones a la derecha

**Escenario 3: Menú hamburguesa en móvil**
Dado que el usuario está en pantalla < md (móvil o tablet pequeña)  
Cuando hace tap en el ícono hamburguesa  
Entonces:
- Se abre un menú lateral o dropdown desde arriba/abajo con fondo blanco o glassmorphism
- Enlaces en columna grande (padding 1rem, font 1.1rem, hover fondo claro)
- Cierre con X o tap fuera
- Animación suave (slide-in o fade + scale)

**Escenario 4: Enlaces principales (visibles en desktop, en menú en móvil)**
Los enlaces deben ser:
- Catálogo → /catalogo (prioridad alta, destacado)
- Cómo funciona → página estática o sección
- Contacto / Ayuda → enlace a WhatsApp o formulario
- (Opcional futuro) Buscar → ícono lupa que abre input o modal

**Escenario 5: Zona de acciones a la derecha (sin lógica de rol por ahora)**
Dado que el header está visible  
Entonces en la zona derecha (desktop) o dentro del menú (móvil) se muestra:
- Botón “Explorar catálogo” (verde primario, destacado) → /catalogo
- Botón “Iniciar sesión” (outline o texto) → /login
- Botón “Registrarse” (verde sólido o gradiente) → /registro
- En móvil: botones grandes, apilados verticalmente si es necesario

**Escenario 6: Responsive y mobile-first obligatorio**
- < 768px (móvil): logo centrado o izquierda + hamburguesa derecha, sin enlaces visibles
- 768px+ (tablet/desktop): enlaces horizontales + acciones derecha
- Altura del header: ~64–80px en móvil, ~80px en desktop
- No tapa contenido (z-50), scroll suave
- Prueba en DevTools: iPhone SE, Galaxy S20, iPad

**Escenario 7: Accesibilidad y rendimiento**
- Contraste WCAG AA (texto sobre fondo)
- aria-label en íconos (ej: aria-label="Menú principal")
- Focus visible en enlaces y botones
- Imágenes/íconos con loading="lazy" si aplica
- Sin animaciones pesadas (max 300ms transitions)

**Notas**
- Esta US se centra **solo en diseño y estructura visual** → NO incluye lógica de sesión, dropdown de usuario logueado, ni redirecciones por rol (eso va en US-012 o US posteriores)
- Usa Tailwind para todo el estilo
- Componente recomendado: `components/Navbar.vue` o `components/Header.vue`
- Inspiración visual 2026: headers de Linear.app, Notion, Figma, Vercel (glassmorphism + minimalismo + micro-interacciones)
- No instales librerías extras para el header (solo Framer Motion si ya está por las animaciones de login/registro)

**Tareas**
TK-014-01 Crear componente `components/Navbar.vue` (o Header.vue) con estructura base
TK-014-02 Implementar logo + enlaces principales (desktop)
TK-014-03 Implementar menú hamburguesa + mobile menu (slide-in o dropdown)
TK-014-04 Añadir zona de acciones derecha (Explorar, Iniciar sesión, Registrarse)
TK-014-05 Aplicar glassmorphism, gradientes, hover effects y transiciones suaves
TK-014-06 Asegurar responsive total + pruebas en móvil (DevTools)
TK-014-07 Añadir accesibilidad básica (aria-label, focus styles)
TK-014-08 Integrar el Navbar en App.vue (usar <Navbar /> en todas las páginas)
TK-014-09 Commit: “US-014: Header premium mobile-first implementado”

**Prioridad**  
Alta – El header es lo primero que ve todo usuario y afecta la percepción de calidad de la app

**Dependencias**  
Ninguna (se puede hacer antes o después de US-012, pero idealmente antes para consistencia visual)

---

## 📋 INFORME DE EJECUCIÓN - US-014

### Tareas completadas:

    ✅ **TK-014-01** - Creado componente `src/componentes/Navbar.vue` con estructura completa  
    ✅ **TK-014-02** - Implementado logo + enlaces principales (Catálogo, Cómo funciona, Contacto) en desktop  
    ✅ **TK-014-03** - Implementado menú hamburguesa con animación slide-in + overlay glassmorphism para móvil  
    ✅ **TK-014-04** - Añadida zona de acciones derecha (Explorar catálogo, Iniciar sesión, Registrarse)  
    ✅ **TK-014-05** - Aplicados glassmorphism, gradientes, hover effects (scale 1.05) y transiciones suaves (200-300ms)  
    ✅ **TK-014-06** - Responsive total: mobile-first con breakpoint md (768px), header fixed con backdrop-blur  
    ✅ **TK-014-07** - Accesibilidad: aria-labels, aria-expanded, focus-visible states, contraste WCAG AA  
    ✅ **TK-014-08** - Integración en `src/App.vue` - Navbar visible en todas las páginas  
    ✅ **TK-014-09** - Commit listo para realizar

    ### Archivos creados/modificados:
        - **Creado**: `src/componentes/Navbar.vue` (230 líneas)
        - **Creado**: `src/componentes/Login.vue` (118 líneas) - necesario para enlace del navbar
        - **Modificado**: `src/App.vue` - import y uso del componente Navbar
        - **Modificado**: `src/router/index.ts` - añadida ruta /login

        ### Características implementadas:
            - Header fixed con efecto scroll (cambia de estilo al hacer scroll)
            - Glassmorphism con backdrop-blur-md
            - Gradientes verde agrícola (#2E7D32 → #4CAF50)
            - Menú móvil con animación Transition de Vue
            - Botones con hover scale(1.05) y sombras
            - Focus states para accesibilidad
            - Mobile-first design (64-80px móvil, 80px desktop)

            ### Build: ✅ EXITOSO