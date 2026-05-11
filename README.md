# AgroConet

Marketplace agrícola B2B/B2C construido con Vue 3, Vite, Vue Router, Tailwind CSS 4 y `json-server` como API mock.

## Requisitos

- Node.js compatible con Vite 8
- npm

## Instalación

```bash
npm install
```

## Desarrollo

Ejecutar la API mock:

```bash
npm run mock
```

Ejecutar el frontend:

```bash
npm run dev
```

La API mock usa `db.json` en `http://localhost:3001`.

## Usuarios demo

- Comprador: `comprador@agroconet.test` / `demo123`
- Productor: `productor@agroconet.test` / `demo123`
- Agencia: `agencia@agroconet.test` / `demo123`

## Scripts útiles

```bash
npm run typecheck
npm run build
npm run preview
```

## Alcance actual

- Landing page, navegación responsive y páginas informativas.
- Catálogo con filtros, clima desde Open-Meteo y precios estimados.
- Detalle de producto con acciones mínimas de pedido, contacto y favoritos.
- Registro/login mock contra `json-server`.
