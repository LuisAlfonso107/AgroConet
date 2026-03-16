
## 1. Visión y Objetivo del Proyecto
AgroConet es un **marketplace agrícola B2B + B2C** que conecta directamente:
- **Productores agrícolas** (caficultores, maiceros, etc. en Honduras, Guatemala, Nicaragua, El Salvador y diferentes parste de latinoamerica y el mundo)
- **Compradores** (tostadores, molinos, supermercados, exportadores pequeños, consumidores premium)
- **Agencias exportadoras** (tercer actor que gestiona logística, documentos y tracking)

**Misión:** Eliminar intermediarios innecesarios y dar trazabilidad completa desde la finca hasta el puerto o el cliente final.

**Fase actual:** Solo Frontend con Vue 3 + Vite + json-server (db.json).  
**Nombre provisional de la app:** GranoDirecto

## 2. Actores y Roles
- **Productor** (rol 1) – publica cosechas, gestiona stock y ve pedidos recibidos
- **Comprador** (rol 2) – explora catálogo, hace pedidos, ve tracking
- **Agencia Exportadora** (rol 3) – ve pedidos asignados y actualiza estados
- **Visitante** (sin login, pero al intentar interactuar, se le redirige a login) – solo ve Home y Catálogo y puede interactuar con el catálogo

## 3. Stack Tecnológico (Fase 1 - Frontend puro)
- Vue 3 (Composition API + <script setup>)
- Vite
- json-server (puerto 3001)
- Axios o fetch para llamadas
- Pinia (para estado de usuario y rol – se activará en Sprint 2)
- Vue Router
- Tailwind CSS o Bootstrap 5 (recomendado Tailwind para mobile-first)
- Responsive 100% mobile-first (agricultores usan Android económicos en el campo)

siempre sigue al pie de la letra las historias de usuario y las tareas