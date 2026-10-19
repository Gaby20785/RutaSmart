# Equipo y Matriz RACI — RutaSmart (P05)

> Versión 1.0 · Hito H2 (Baseline) · Responsable: Miembro 1 (PM)
> *Asignación de roles propuesta; pendiente de validación por el equipo.*

---

## 1. Roles del equipo

| Miembro | Rol principal | Rol secundario | Backup de… |
| --- | --- | --- | --- |
| Miembro 1 | Project Manager | QA de documentación y testing | M2 (PO) |
| Miembro 2 | Product Owner | UX/UI (mockups) | M1 (PM) |
| Miembro 3 | Scrum Master | Dev Frontend (panel web) | M6 (mobile) |
| Miembro 4 | Dev Backend (API, auth, tracking) | Seguridad | M5 (algoritmo) |
| Miembro 5 | Dev Backend (algoritmo VRP, GIS) | Integraciones (Mapbox, SMS) | M4 (backend) |
| Miembro 6 | QA / DevOps | Dev Mobile (PWA) | M3 (frontend) |

**Sponsor:** Profesor/a – Panel evaluador.

---

## 2. Matriz RACI

**R** = Responsable (ejecuta) · **A** = Aprobador (rinde cuentas, solo uno) · **C** = Consultado · **I** = Informado

### Gestión del proyecto

| Actividad / Entregable | M1 PM | M2 PO | M3 SM | M4 | M5 | M6 | Sponsor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Project Charter | R/A | C | C | I | I | I | C |
| Registro de stakeholders | R/A | C | I | I | I | I | I |
| WBS y cronograma (Gantt) | R/A | C | C | C | C | C | I |
| Presupuesto base y EVM mensual | R/A | I | C | I | I | I | I |
| Matriz de riesgos | R/A | C | C | C | C | C | I |
| Plan de comunicaciones | R/A | C | C | I | I | I | I |
| Control de cambios (RFC / CCB) | A | R | C | C | C | C | I |
| Reportes de avance quincenales | R/A | C | C | I | I | I | I |
| Lecciones aprendidas y cierre | A | C | R | C | C | C | I |

### Producto y Scrum

| Actividad / Entregable | M1 PM | M2 PO | M3 SM | M4 | M5 | M6 | Sponsor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Product Backlog e historias | C | R/A | C | C | C | C | I |
| Priorización MoSCoW | C | R/A | I | C | C | C | C |
| Sprint Planning | C | A | R | C | C | C | — |
| Daily Scrum | I | C | R/A | C | C | C | — |
| Sprint Review (demo) | C | A | R | C | C | C | I |
| Retrospectiva | C | C | R/A | C | C | C | — |
| Métricas ágiles (velocity, burndown, lead/cycle time) | C | I | R/A | I | I | C | I |
| Mockups UX/UI | I | R/A | C | I | I | C | — |
| Prueba de uso con personas externas (UAT) | C | R/A | C | I | I | C | I |

### Desarrollo técnico

| Actividad / Entregable | M1 PM | M2 PO | M3 SM | M4 | M5 | M6 | Sponsor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Arquitectura del sistema | I | C | C | R | A | C | — |
| Setup del repositorio y Docker | I | I | C | C | C | R/A | — |
| Pipeline CI/CD y entornos | I | I | C | C | C | R/A | — |
| Autenticación y roles | I | C | C | R/A | I | C | — |
| Flota, conductores y pedidos (API) | I | C | C | R/A | C | I | — |
| Motor de optimización VRP | I | C | I | C | R/A | I | — |
| Integración Mapbox y SMS | I | I | C | C | R/A | C | — |
| Tracking en tiempo real (WebSocket) | I | C | C | R/A | C | C | — |
| Panel web (React) | I | C | R/A | C | I | C | — |
| App repartidor (PWA, offline) | I | C | C | C | I | R/A | — |
| Tests y cobertura | C | I | C | R | R | A | — |
| Pruebas de carga y latencia | I | I | I | R | C | A | — |
| Documentación técnica y del algoritmo | A | I | C | R | R | C | — |
| Dashboard DORA | I | I | C | I | I | R/A | I |

---

## 3. Distribución de carga (horas planificadas)

| Miembro | Gestión y diseño (WBS 1–2) | Desarrollo (WBS 3–7) | Testing y docs (WBS 8–9) | Total |
| --- | --- | --- | --- | --- |
| Miembro 1 (PM) | 110 | 0 | 40 | 150 |
| Miembro 2 (PO) | 70 | 50 | 30 | 150 |
| Miembro 3 (SM) | 15 | 125 | 10 | 150 |
| Miembro 4 | 5 | 135 | 10 | 150 |
| Miembro 5 | 10 | 125 | 15 | 150 |
| Miembro 6 | 5 | 135 | 10 | 150 |
| **Total** | **215** | **570** | **115** | **900** |

> Cada miembro: 15 h/semana × 10 semanas = 150 h (re-baseline RFC-003; antes 165 h con 11 semanas). La carga está **equilibrada** (rúbrica: "RACI documentado; asignaciones equilibradas").
> Los totales por columna coinciden con la WBS. El tiempo de ceremonias Scrum de los desarrolladores se imputa a su paquete de desarrollo.

---

## 4. Acuerdos de equipo

1. Las tareas se gestionan en el tablero (Jira/Trello); nada se trabaja fuera del tablero.
2. Todo código entra por pull request con al menos una revisión.
3. Un bloqueo de más de 24 h se comunica en el canal del equipo y en la siguiente daily.
4. Las ausencias se anotan en el calendario compartido con al menos 48 h de antelación.
5. Los conflictos se resuelven primero entre las partes, después con el SM y, si persisten, con el PM.
6. Se mide la satisfacción del equipo (1–5) al final de cada mes.
