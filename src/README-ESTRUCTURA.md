# Estructura de Carpetas - Proyecto GranoDirecto

## Organización

```
src/
├── assets/           # Imágenes, iconos, logos (todo estático)
├── components/       # Solo componentes reutilizables (CardProducto, Button, Modal, etc.)
├── composables/      # Toda la lógica: useApi.ts, useProductos.ts, usePedidos.ts, useAuth.ts
├── router/           # Configuración de rutas (index.ts)
├── stores/           # Pinia stores (Sprint 2)
├── vistas/           # Solo páginas completas (Home.vue, Catalogo.vue, etc.)
├── utils/            # Helpers pequeños (formatPrice.ts, validateHumedad.ts)
├── App.vue
└── main.ts
```

## Reglas de Ubicación

### Vistas (`src/vistas/`)
- Cualquier página completa con `<template>` que representa una ruta
- Nunca contienen lógica de negocio ni fetch directo
- Importan toda lógica desde composables

### Componentes (`src/components/`)
- Componentes reutilizables (Card, Button, Modal, etc.)
- Nunca contienen lógica de negocio ni fetch directo

### Composables (`src/composables/`)
- Toda la lógica, fetch a json-server, cálculos, estados reactivos
- Composable personalizados para cada funcionalidad

### Datos de Prueba
- Los datos de prueba (productos, productores, pedidos) → Solo en `db.json` (raíz)

## Notas

- La carpeta `vistas/` (no `views/`) porque el equipo trabaja en español
- El `db.json` queda en raíz para que json-server lo lea fácil
- Esta estructura es escalable a Pinia, TypeScript y backend real
