# AgroConet 🌾

Marketplace agrícola B2B/B2C moderno y dinámico construido con **Vue 3** y **Tailwind CSS 4** para el frontend, y **Flask (Python)** para el backend con base de datos **SQLite** en desarrollo.

---

## 🚀 Requisitos de Entorno

### Frontend
- **Node.js** (compatible con Vite 8)
- **npm**

### Backend
- **Python 3.10+** (y gestor de paquetes `pip`)

---

## 🛠️ Configuración e Inicialización

### 1. Clonar el Proyecto e Instalar el Frontend
Desde el directorio raíz del proyecto:
```bash
# Instalar las dependencias del frontend
npm install
```

### 2. Configurar e Inicializar el Backend
Navega a la carpeta del backend para configurar el entorno virtual de Python, instalar dependencias e inicializar la base de datos local:

```bash
cd backend

# Crear el entorno virtual (usando launcher de Python 'py' en Windows)
py -m venv .venv

# Activar el entorno virtual e instalar dependencias
.venv\Scripts\pip install -r requirements.txt

# Ejecutar las migraciones para estructurar la base de datos SQLite
$env:FLASK_APP="run.py"
.venv\Scripts\flask db upgrade

# Sembrar los datos demo desde db.json a SQLite
.venv\Scripts\python seed.py

# Regresar a la raíz
cd ..
```

> [!TIP]
> Si estás en un sistema Unix/macOS, puedes activar el entorno virtual con `source .venv/bin/activate` e instalar las dependencias con `pip install -r requirements.txt`. Las migraciones se corren definiendo la variable: `export FLASK_APP=run.py && flask db upgrade`.

---

## 💻 Desarrollo (Ejecución de Servidores)

Para arrancar los servidores en modo desarrollo local, abre dos pestañas o terminales distintas:

### Ejecutar el Backend (Puerto 3000)
Desde el directorio raíz:
```bash
npm run dev:api
```
*(O de forma directa: `cd backend && .venv\Scripts\python run.py`)*

### Ejecutar el Frontend (Puerto 5173)
Desde el directorio raíz:
```bash
npm run dev
```

El frontend llamará automáticamente a la API en `http://localhost:3000/api`.

---

## 👥 Usuarios Demo (Sembrados)

Los usuarios de demostración iniciales se importan directamente desde `db.json` con contraseñas encriptadas (seguridad por Bcrypt) listas para usar:

* **Comprador:** `comprador@agroconet.test` / `demo123`
* **Productor:** `productor@agroconet.test` / `demo123`
* **Agencia:** `agencia@agroconet.test` / `demo123`

---

## 📂 Scripts Útiles

```bash
npm run typecheck   # Chequeo estático de tipos de Vue/TS
npm run build       # Compilación del frontend para producción
npm run preview     # Vista previa del build local de producción
```

---

## ✨ Alcance e Integración Actual

- **Frontend:** Landing page, catálogo interactivo con filtros avanzados, consulta de clima en tiempo real desde *Open-Meteo*, detalles de producto, panel de control de compradores/productores.
- **Backend:** Autenticación de sesiones JWT, persistencia de relaciones de base de datos en SQLite (Usuarios, Productos, Pedidos, Eventos de Tracking, Favoritos).
- **Conectividad:** Axios con interceptores personalizados para transformar automáticamente respuestas a *camelCase* en JS y solicitudes a *snake_case* en Python.
