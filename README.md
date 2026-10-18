# RutaSmart — Optimizador de rutas de entrega

MVP del proyecto **P05 · RutaSmart** (Bootcamp Gestión de Proyectos TI). Plataforma web para empresas de reparto de última milla: gestión de flota y pedidos, **optimización automática de rutas** y, en próximos sprints, seguimiento en vivo y app del repartidor.

> Estado: **Sprint 1 terminado** (semanas 3–4, hito H3). Ver [docs/](docs/) para la documentación de gestión.

## Funcionalidades del Sprint 1

| Req. | Historia | Estado |
| --- | --- | --- |
| EN-01 | Repositorio, estructura del proyecto y Docker | ✅ |
| RF15 | Autenticación JWT con roles (admin, despachador, conductor) | ✅ |
| RF18 | Pipeline CI en GitHub Actions (lint + tests + build) | ✅ |
| RF1 | Alta de flota: conductores y vehículos con capacidad (kg y m³) | ✅ |
| RF2 | Carga de pedidos (formulario e importación CSV) con ventana horaria y peso/volumen | ✅ |
| RF3 | Optimización automática de rutas (VRP con capacidad y ventanas horarias) | ✅ |

## Stack

- **Backend:** Python 3.12 · FastAPI · SQLAlchemy 2 · Google OR-Tools · JWT (PyJWT + bcrypt)
- **Base de datos:** PostgreSQL 16 + PostGIS (Docker) · SQLite para desarrollo local rápido
- **Frontend:** React 18 · Vite · React Router · Leaflet (OpenStreetMap)
- **Calidad / DevOps:** pytest + cobertura · Ruff · ESLint · Vitest · GitHub Actions · Docker Compose

## Requisitos

| Herramienta | Versión | Comprobar con |
| --- | --- | --- |
| Python | 3.12 | `python --version` |
| Node.js | 22 LTS | `node --version` |
| Git | cualquiera | `git --version` |
| Docker Desktop | *solo para la opción B* | `docker --version` |

> En Windows, al instalar Python marca **"Add python.exe to PATH"**. Si `python` no se reconoce, prueba con `py`.

## Opción A · Desarrollo local (recomendada)

La primera vez tarda unos minutos (descarga de dependencias). Necesitas **dos terminales** abiertas a la vez.

### 0. Descargar el proyecto

```powershell
git clone https://github.com/Gaby20785/RutaSmart.git
cd RutaSmart
```

### 1. Backend (terminal 1)

**Windows (PowerShell o CMD):**

```powershell
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements-dev.txt
.venv\Scripts\python -m app.seed --reset
.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

**macOS / Linux:**

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m app.seed --reset
.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

- `app.seed --reset` **borra la base de datos** y crea usuarios, flota y 40 pedidos de prueba **para hoy**. Para otra fecha: `--date 2026-10-19`.
- Está listo cuando aparece `Uvicorn running on http://127.0.0.1:8000`. **Deja esta terminal abierta.**
- No hace falta base de datos ni archivo `.env`: en local se usa SQLite (`backend/rutasmart.db`) y valores por defecto. Para cambiarlos, copia `backend/.env.example` a `backend/.env`.

### 2. Frontend (terminal 2)

```powershell
cd frontend
npm install
npm run dev
```

### 3. Abrir

- Aplicación: <http://localhost:5173>
- Documentación interactiva de la API (Swagger): <http://localhost:8000/docs>

Para parar: `Ctrl + C` en cada terminal. Las siguientes veces solo hace falta el último comando de cada terminal (`uvicorn …` y `npm run dev`).

## Opción B · Entorno completo con Docker (PostgreSQL + PostGIS)

Con Docker Desktop **abierto** y las terminales de la opción A paradas (usan los mismos puertos):

```powershell
docker compose up --build -d
docker compose exec backend python -m app.seed
```

- Aplicación en <http://localhost:8080> · API en <http://localhost:8000/docs>
- Parar: `docker compose down` (los datos se conservan). Borrar también los datos: `docker compose down -v`.

## Usuarios de demo

| Rol | Email | Contraseña |
| --- | --- | --- |
| Administrador | admin@rutasmart.dev | Admin1234 |
| Despachador | despacho@rutasmart.dev | Despacho1234 |
| Conductor | conductor1@rutasmart.dev | Conductor1234 |

La pantalla de login tiene botones para rellenarlos automáticamente.

## Guion de la demo (Sprint Review H3)

1. **Login como Admin** → *Vehículos* y *Conductores*: alta de un vehículo; validación de capacidad > 0 y matrícula duplicada.
2. **Login como Despachador** → *Pedidos*: 40 pedidos sintéticos del día; **Importar CSV** con `backend/sample_data/pedidos_ejemplo.csv` (fecha 20/10/2026).
3. *Rutas* → **Optimizar rutas**: rutas por vehículo en el mapa, ETA de cada parada, carga y **ahorro de km frente a la asignación manual**.
4. Desmarcar *Equilibrar carga entre conductores* y volver a optimizar: menos km pero trabajo desigual (decisión de negocio).
5. **Login como Conductor** → *Mis rutas*: solo ve su ruta. Intentar entrar en `/vehiculos` redirige (control de acceso por rol).
6. Swagger (`/docs`) y pipeline de CI en GitHub Actions en verde.

## Tests

Son las mismas comprobaciones que ejecuta el CI en GitHub; si pasan aquí, pasarán allí. Desde la carpeta raíz del proyecto:

```powershell
cd backend
.venv\Scripts\ruff check .
.venv\Scripts\python -m pytest --cov=app
cd ..\frontend
npm run lint
npm test
npm run build
```

Resultado esperado: **47 tests de backend (cobertura ≈ 83 %) y 8 de frontend en verde**. En macOS/Linux usa `.venv/bin/` y `cd ../frontend`.

## Problemas frecuentes

| Síntoma | Causa y solución |
| --- | --- |
| `python` no se reconoce (Windows) | Python no está en el PATH: reinstálalo marcando "Add python.exe to PATH", o usa `py` en lugar de `python`. |
| `El token '&&' no es un separador válido` | PowerShell de Windows no admite `&&`: ejecuta los comandos uno por línea, como en este README. |
| No se pueden ejecutar scripts (`Activate.ps1`…) | No hace falta activar el entorno: usa las rutas `.venv\Scripts\python` tal como aparecen arriba. |
| Error de puerto en uso, **o la app muestra datos antiguos** | Hay otro backend abierto en el puerto 8000 (en Windows pueden convivir dos sin avisar). Cierra todas las terminales del proyecto, o en PowerShell: `Get-NetTCPConnection -LocalPort 8000 -State Listen` y `Stop-Process -Id <OwningProcess>`. |
| La pantalla de login dice «Email o contraseña incorrectos» con los usuarios de demo | No se ha cargado la demo: ejecuta `.venv\Scripts\python -m app.seed --reset`. |
| «No hay pedidos para planificar en esa fecha» | La fecha de la pantalla no coincide con la de los datos. Cambia la fecha o vuelve a cargar la demo con `--date AAAA-MM-DD`. |
| El mapa se ve gris | El mapa (OpenStreetMap) necesita conexión a internet. |
| Error al crear un pedido sin latitud/longitud | La geocodificación usa Nominatim y necesita internet; o indica las coordenadas a mano. |
| `docker compose` no conecta | Abre Docker Desktop y espera a que indique que está en marcha. |

## Estructura

```text
backend/
  app/
    main.py            # API FastAPI
    models.py          # Modelo de datos (SQLAlchemy)
    schemas.py         # Validación (Pydantic)
    routers/           # auth, drivers, vehicles, orders, routes
    services/
      optimizer.py     # Motor VRP (OR-Tools)
      geo.py           # Distancias y geocodificación
    seed.py            # Datos de demo sintéticos
  tests/               # pytest
frontend/src/
  pages/               # Login, Rutas, Pedidos, Vehículos, Conductores, Mis rutas
  components/          # Layout, RouteMap
docs/                  # Documentación de gestión del proyecto
.github/workflows/     # CI
```

## Limitaciones conocidas (planificadas para próximos sprints)

- Distancias en línea recta × factor de carretera 1,3; el trazado real por calles y la matriz de tiempos llegan con **Mapbox (RF17, Sprint 2)**.
- La geocodificación usa Nominatim (OpenStreetMap) como solución provisional; requiere conexión a internet.
- Coordenadas guardadas como latitud/longitud; el uso de tipos geográficos de PostGIS y migraciones con Alembic está previsto para el Sprint 3.
- Un único almacén de salida (configurable en `backend/.env`).
