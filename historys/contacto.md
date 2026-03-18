### Historia de Usuario US-018
**Implementar la vista "Contacto" con formulario funcional y diseño limpio**

**Como** visitante o usuario de la aplicación (productor, comprador o interesado)  
**Quiero** tener una página de contacto clara, accesible y profesional  
**Para** poder enviar consultas, reportar problemas, solicitar información o proponer colaboraciones de forma rápida y sin complicaciones

**Criterios de Aceptación**

**Escenario 1: Carga inicial y diseño general**  
Dado que el usuario accede a la ruta /contacto  
Cuando la página carga  
Entonces:  
- Animación de entrada suave (fade-in + slide-up de secciones, 1–3 segundos)  
- Hero section sencilla (no tan grande como en home):  
  - Fondo sutil (gradiente crema-verde o imagen ligera de manos conectadas/finca)  
  - Título principal: “Contacto – Estamos aquí para ayudarte”  
  - Subtítulo: “¿Dudas? ¿Problemas? ¿Ideas? Escríbenos y te respondemos en menos de 24 horas.”  
- CTA visible desde arriba: botón “Enviar mensaje” que scrollea al formulario

**Escenario 2: Información de contacto rápida (zona superior o lateral)**  
Dado que el usuario está en la página  
Entonces debe ver inmediatamente:  
- **WhatsApp directo** (botón grande con ícono + número): “Chatea con nosotros ahora” → abre wa.me/+504... (número ficticio o real de soporte)  
- **Correo electrónico** destacado: soporte@agroconet.hn o hola@agroconet.com  
- **Redes sociales** (íconos pequeños): Instagram, Facebook, X/Twitter (links ficticios o placeholders)  
- **Ubicación** (opcional): “Basados en San Pedro Sula, Honduras – pero conectamos toda Centroamérica”  
- Todo en cards o bloques con hover effect sutil

**Escenario 3: Formulario de contacto completo y validado**  
Dado que el usuario quiere enviar un mensaje  
Cuando llena el formulario  
Entonces debe incluir estos campos (obligatorios con *):  
- Nombre completo*  
- Correo electrónico* (validación formato)  
- Teléfono / WhatsApp* (formato internacional, ej: +50499887766)  
- Asunto* (select o input: Consulta general, Problema técnico, Quiero ser productor, Soy comprador, Colaboración, Otro)  
- Mensaje* (textarea, mínimo 10 caracteres)  
- Checkbox: “Acepto la política de privacidad”* (enlace a futura página /privacidad)  

Validaciones en tiempo real:  
- Bordes verdes/rojos + íconos check/cruz animados  
- Mensaje de error claro debajo de cada campo  
- Botón “Enviar” deshabilitado hasta que todo sea válido

**Escenario 4: Envío y feedback**  
Dado que el usuario completa el formulario correctamente  
Cuando hace clic en “Enviar”  
Entonces:  
- Aparece loading spinner + texto “Enviando...”  
- Simulación de envío (POST a un endpoint mock o console.log por ahora)  
- Mensaje de éxito con animación (check verde + confeti sutil):  
  “¡Mensaje enviado! Te responderemos pronto. Gracias por contactarnos.”  
- Opcional: redirección suave a /catalogo o home después de 3–5 segundos  
- Si error (simulado): toast rojo “Hubo un problema, intenta de nuevo o contáctanos por WhatsApp”

**Escenario 5: Diseño y experiencia**  
- Estilo consistente: glassmorphism en formulario y cards, gradientes agro, sombras suaves  
- Mobile-first: formulario apilado, campos grandes (≥48px touch), teclado no tapa botón enviar  
- Animaciones ligeras: fade-in al scroll, ripple en botón enviar, shake en error  
- Accesibilidad: alt en íconos, aria-label en botones, labels asociados a inputs, contraste WCAG AA  
- Responsive: en desktop formulario + info lateral, en móvil todo apilado vertical

**Escenario 6: Contenido adicional (opcional pero recomendado)**  
- Mapa simple embebido (iframe OpenStreetMap o Google Maps) con ubicación aproximada  
- Horario de atención: “Lunes a Viernes 8:00 AM – 5:00 PM (hora Honduras)”  
- Enlace a FAQ: “¿Ya revisaste nuestras preguntas frecuentes?” → /como-funciona o futura /faq

**Notas**  
- Página pública (sin login requerido)  
- En fase 1: envío simulado (console.log o POST a json-server /mensajes)  
- En fase 2: integrar API real (Supabase, Formspree, EmailJS o backend propio)  
- Usa Tailwind + Framer Motion para animaciones (ya presentes)  
- Inspiración visual: páginas de contacto de Notion, Linear, Shopify, o apps agrícolas como AgriWebb

**Tareas**  
TK-018-01 Crear vistas/Contacto.vue con hero y estructura base  
TK-018-02 Implementar zona de contacto rápido (WhatsApp, email, redes)  
TK-018-03 Diseñar y validar formulario completo con campos y checkbox  
TK-018-04 Añadir animaciones de entrada y feedback de éxito/error  
TK-018-05 Implementar simulación de envío (POST mock o console)  
TK-018-06 Asegurar responsive + accesibilidad básica  
TK-018-07 Agregar enlace en Navbar: “Contacto” → /contacto  
TK-018-08 Commit: “US-018: Vista Contacto con formulario implementada”

**Prioridad**  
Media – Importante para soporte y confianza, pero no bloquea funcionalidades principales

**Dependencias**  
- US-014 (Header/Navbar con enlace a esta ruta)  
- Componentes reutilizables (botones, cards, inputs)