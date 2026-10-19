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
| HU-02 | Carga de pedidos (formulario + CSV) | 5 | ✅ Hecho* | ✅ Ventana horaria y peso/volumen · ✅ CSV con informe de errores por fila · ⚠️ geocodificación con Nominatim y coordenadas como lat/lng (RFC-004) |
| HU-03 | Optimización de rutas (VRP) | 13 | ✅ Hecho | ✅ < 30 s para 100 pedidos (3 s) · ✅ capacidad respetada · ✅ ventanas horarias respetadas o pedido marcado · ✅ mapa con orden de paradas y km |
| | **Total** | **34** | **34 / 34 SP** | |

\* Aceptada por el PO con la desviación registrada en RFC-004.

**Fuera de plan:** opción "equilibrar carga entre conductores" (RFC-003).

---

## 3. Métricas del sprint

| Métrica | Valor | Objetivo |
| --- | --- | --- |
| Velocity | **34 SP** | 34 SP |
| Compromiso cumplido | 100 % | ≥ 80 % |
| Tests automatizados | 47 backend + 8 frontend | — |
| Cobertura de tests (backend) | **83 %** | ≥ 40 % en S6 |
| Ahorro de km frente a la planificación manual (40 pedidos de demo) | 59–67 % | ≥ 15 % (objetivo O2) |
| Tiempo de optimización (40 pedidos, 4 vehículos) | 3 s | < 30 s |
| Defectos detectados durante el sprint | 3 (corregidos) | — |
| Defectos abiertos al cierre | 0 | — |
| RFC del sprint | 2 (RFC-003, RFC-004) | — |
| Burndown | `[exportar del tablero]` | — |
| Horas reales del equipo | `[completar con el registro de horas]` | 360 h planificadas en el mes 1 |

### Defectos detectados y corregidos

1. **Horarios de ruta poco realistas:** las rutas salían tarde y esperaban en la primera parada. Se corrigió el orden de optimización de los horarios (primero terminar antes, luego salir lo más tarde posible).
2. **Vista del conductor vacía:** el optimizador podía dejar sin ruta al conductor con cuenta. Se resolvió con el reparto equilibrado (RFC-003).
3. **El backend no arrancaba en Docker:** el healthcheck de PostgreSQL daba el servicio por listo antes de tiempo. Se corrigió el healthcheck y se registró el riesgo R15.

---

## 4. Demo (Sprint Review)

Guion en el [README](../README.md#guion-de-la-demo-sprint-review-h3):

1. Admin → alta de vehículo y validaciones.
2. Despachador → pedidos del día e importación CSV.
3. Optimizar → mapa, ETA, carga y **% de ahorro**.
4. Comparar el modo equilibrado con el de mínimos km.
5. Conductor → solo ve su ruta (control de acceso por rol).
6. Swagger y CI en verde.

**Feedback del Sponsor:** `[completar tras la presentación]`

---

## 5. Retrospectiva *(borrador: completar en la reunión del equipo)*

### ¿Qué fue bien?
- Usar OR-Tools en lugar de programar el algoritmo desde cero (respuesta a R01) permitió cerrar el VRP en un solo sprint.
- Los tests automáticos detectaron errores antes de la demo.
- Los datos sintéticos de Madrid permiten enseñar el producto sin datos reales de clientes.

### ¿Qué se puede mejorar?
- Varios defectos aparecieron solo al probar la aplicación completa (navegador, Docker), no en los tests unitarios.
- El desarrollo local usa SQLite y staging usa PostgreSQL: riesgo de diferencias (R15).
- `[aportaciones del equipo]`

### Acciones de mejora para el Sprint 2

| Acción | Responsable | Cómo se mide |
| --- | --- | --- |
| Probar con `docker compose` (PostgreSQL) antes de cada review | M6 | Checklist de la review |
| Añadir una prueba E2E del flujo login → optimizar | M6 | Test en CI |
| Registrar horas diariamente en el tablero para el EVM | M1 | AC disponible en el reporte mensual |
| `[acción propuesta por el equipo]` | | |

**Satisfacción del equipo (1–5):** `[encuesta]`

---

## 6. Sprint 2 (20/10 – 02/11) — próximo objetivo

> *"El conductor recibe su ruta en el móvil y registra las entregas con evidencia."*

HU-17 (Mapbox + SMS) · HU-04 (asignación + push) · HU-05 (app del repartidor) · HU-06 (evidencia de entrega) → **34 SP**.

**Cambio de calendario (19/10/2026, RFC-005):** entregas el 09/11 y el 30/11. Quedan 3 sprints de 2 semanas; RF13 y RF20 salen del compromiso (18 requerimientos comprometidos).
