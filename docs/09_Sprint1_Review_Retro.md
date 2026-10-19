# Sprint 1 — Review y Retrospectiva — RutaSmart (P05)

> Sprint 1 · Semanas 3–4 (05/10 – 18/10/2026) · Hito **H3 – Demo Sprint 1**
> Facilitador: Miembro 3 (SM) · Aprobación de historias: Miembro 2 (PO)

---

## 1. Objetivo del sprint

> *"Tener la base técnica del producto (repositorio, autenticación, CI) y que un despachador pueda dar de alta su flota, cargar los pedidos del día y obtener rutas optimizadas."*

**Resultado: ✅ Objetivo cumplido.**

---

## 2. Historias comprometidas y resultado

| ID | Historia | SP | Estado | Criterios de aceptación |
| --- | --- | --- | --- | --- |
| EN-01 | Setup del proyecto (repo, estructura, Docker) | 3 | ✅ Hecho | ✅ `docker compose up` levanta frontend + API + PostgreSQL/PostGIS |
| HU-15 | Autenticación por rol (JWT) | 5 | ✅ Hecho | ✅ Login con token · ✅ 403 si el rol no tiene permiso · ✅ contraseñas con bcrypt |
| HU-18 | Pipeline CI | 3 | ✅ Hecho | ✅ Lint + tests + build en GitHub Actions · ✅ cobertura mínima del 40 % obligatoria |
| HU-01 | Alta de flota (conductores y vehículos) | 5 | ✅ Hecho | ✅ CRUD · ✅ capacidad en kg y m³ · ✅ matrículas duplicadas y capacidad ≤ 0 rechazadas |
| HU-02 | Carga de pedidos (formulario + CSV) | 5 | ✅ Hecho* | ✅ Ventana horaria y peso/volumen · ✅ CSV con informe de errores por fila · ⚠️ geocodificación provisional con OpenStreetMap (Nominatim) hasta integrar Mapbox |
| HU-03 | Optimización de rutas (VRP) | 13 | ✅ Hecho | ✅ < 30 s para 100 pedidos (3 s) · ✅ capacidad respetada · ✅ ventanas horarias respetadas o pedido marcado · ✅ mapa con orden de paradas y km |
| | **Total** | **34** | **34 / 34 SP** | |

\* Aceptada por el PO: la geocodificación usa OpenStreetMap de forma provisional y las coordenadas se guardan como latitud/longitud; Mapbox y los tipos geográficos de PostGIS llegan en los sprints 2 y 3.

**Cambios aprobados durante el sprint:** mapa con OpenStreetMap desde el Sprint 1 (RFC-001) y opción «equilibrar carga entre conductores» (RFC-002).

---

## 3. Métricas del sprint

| Métrica | Valor | Objetivo |
| --- | --- | --- |
| Velocity | **34 SP** | 34 SP |
| Compromiso cumplido | 100 % | ≥ 80 % |
| Tests automatizados | 47 backend + 8 frontend | — |
| Cobertura de tests (backend) | **83 %** | ≥ 40 % al 02/11 |
| Ahorro de km frente a la planificación manual (40 pedidos de demo) | 59–67 % | ≥ 15 % (objetivo O2) |
| Tiempo de optimización (40 pedidos, 4 vehículos) | 3 s | < 30 s |
| Defectos detectados durante el sprint | 3 (corregidos) | — |
| Defectos abiertos al cierre | 0 | — |
| RFC del sprint | 2 (RFC-001, RFC-002) | — |
| Burndown | `[exportar del tablero]` | — |
| Horas reales del equipo (mes 1) | ≈ 130 h (estimación de cada integrante) | 144 h planificadas |

### Defectos detectados y corregidos

1. **Horarios de ruta poco realistas:** las rutas salían tarde y esperaban en la primera parada. Se corrigió el orden de optimización de los horarios (primero terminar antes, luego salir lo más tarde posible).
2. **Vista del conductor vacía:** el optimizador podía dejar sin ruta al conductor con cuenta. Se resolvió con el reparto equilibrado (RFC-002).
3. **El backend no arrancaba en Docker:** el healthcheck de PostgreSQL daba el servicio por listo antes de tiempo. Se corrigió el healthcheck y se registró el riesgo R15.

---

## 4. Demo (Sprint Review)

Guion en el [README](../README.md#guion-de-la-demo-sprint-review-h3):

1. Admin → alta de vehículo y validaciones.
2. Despachador → pedidos del día e importación CSV.
3. Optimizar → mapa, ETA, carga y **% de ahorro**.
4. Comparar el modo equilibrado con el de mínimos km.
5. Conductor → solo ve su ruta (control de acceso por rol).
6. Documentación de la API (Swagger, en /docs).

**Feedback del Sponsor:** `[completar tras la presentación]`

---

## 5. Retrospectiva

### ¿Qué fue bien?
- El algoritmo de rutas quedó funcionando en el primer sprint gracias a usar una librería probada (OR-Tools).
- Terminamos todo lo comprometido (34 de 34 SP).
- Los tests automáticos detectaron errores antes de la demo.

### ¿Qué se puede mejorar?
- Algunos errores solo aparecieron al probar la aplicación completa, no en los tests.
- Las horas se estimaron al final del mes en lugar de registrarlas cada día.
- Dedicamos menos horas de las planificadas (≈ 5 h/semana por persona en lugar de 6).

### Acciones para el Sprint 2

| Acción | Responsable | Cómo se mide |
| --- | --- | --- |
| Probar la aplicación completa antes de cada review | M6 | Checklist de la review |
| Registrar las horas cada día en el tablero | M1 | Horas disponibles para el reporte mensual |
| Revisar la dedicación de cada uno en la Sprint Planning | M3 | Capacidad comprometida vs. real |

**Satisfacción del equipo (1–5):** `[encuesta]`

---

## 6. Sprint 2 (20/10 – 02/11) — próximo objetivo

> *"El conductor recibe su ruta en el móvil y registra las entregas con evidencia."*

HU-17 (Mapbox + SMS) · HU-04 (asignación + push) · HU-05 (app del repartidor) · HU-06 (evidencia de entrega) → **34 SP**.

**Ajuste del calendario (19/10/2026, RFC-003):** revisión intermedia el 09/11 y cierre el 30/11. Quedan 3 sprints de 2 semanas; RF13 y RF20 salen del compromiso (18 requerimientos comprometidos).
