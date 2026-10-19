# Proceso de Control de Cambios — RutaSmart (P05)

> Versión 1.0 · Hito H2 (Baseline) · Responsable: Miembro 2 (PO) · Aprobador: Miembro 1 (PM)

---

## 1. Comité de Control de Cambios (CCB)

| Miembro | Rol en el CCB |
| --- | --- |
| Miembro 1 (PM) | Preside y aprueba; evalúa impacto en tiempo y coste |
| Miembro 2 (PO) | Recibe las RFC; evalúa impacto en alcance y valor |
| Miembro 3 (SM) | Evalúa impacto en el sprint y en la capacidad del equipo |
| Responsable técnico del área afectada (M4, M5 o M6) | Evalúa impacto técnico y esfuerzo |

Se reúne tras el refinamiento semanal (jueves) o de forma extraordinaria si el cambio es urgente.

---

## 2. Flujo

1. **Solicitud:** cualquier stakeholder rellena una RFC (plantilla abajo).
2. **Registro:** el PO asigna un ID y la añade al registro de cambios.
3. **Análisis de impacto:** alcance, tiempo, coste, calidad y riesgos.
4. **Decisión del CCB:** aprobada / rechazada / aplazada.
5. **Actualización de la baseline** (si se aprueba): backlog, Gantt, presupuesto, riesgos.
6. **Comunicación:** al equipo y, si afecta a un hito o al presupuesto, al Sponsor.

**Regla:** los cambios no entran en el sprint en curso salvo que sean urgentes y el CCB los apruebe.

---

## 3. Plantilla RFC

| Campo | Contenido |
| --- | --- |
| ID / Fecha | RFC-XXX · dd/mm/aaaa |
| Solicitante | |
| Descripción del cambio | |
| Justificación | |
| Impacto en alcance | |
| Impacto en tiempo | |
| Impacto en coste | |
| Impacto en calidad / riesgos | |
| Alternativas | |
| Decisión CCB | Aprobada / Rechazada / Aplazada |
| Fecha de decisión y firmantes | |

---

## 4. Registro de cambios

| ID | Fecha | Descripción | Solicitante | Alcance | Tiempo | Coste | Decisión |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RFC-001 | 02/10/2026 | Adelantar RF15 (autenticación por rol) y RF18 (pipeline CI) al Sprint 1, y RF17 (integración Mapbox) al Sprint 2 | M1 (PM) | Sin cambio en el nº de requerimientos; RF15 pasa de Should a Must | Sin impacto en la fecha final; reordena sprints | 0 € | ✅ Aprobada |
| RFC-002 | 02/10/2026 | Reagrupar los requerimientos de 7 sprints estimados (hoja P05) a los 5 sprints del calendario real | M2 (PO) | Sin cambio | Ajusta la carga por sprint (~34 SP) | 0 € | ✅ Aprobada |
| RFC-003 | 15/10/2026 | Añadir al optimizador la opción "Equilibrar carga entre conductores" (activada por defecto) | M5 (Dev) | Mejora de RF3, sin historias nuevas | +1 SP absorbido en el Sprint 1 | 0 € | ✅ Aprobada |
| RFC-004 | 15/10/2026 | Guardar coordenadas como lat/lng (no como tipo geográfico PostGIS) y usar Nominatim como geocodificador provisional hasta Mapbox | M4 (Dev) | Criterio de aceptación de HU-02 parcialmente aplazado | Tipos PostGIS + Alembic pasan al Sprint 3 (+2 SP) | 0 € | ✅ Aprobada |
| RFC-005 | 19/10/2026 | Nuevo calendario del Sponsor: Entrega 2 el 09/11 y Entrega 3 el 30/11 (antes ~16/11 y ~07/12) | Sponsor | RF13 y RF20 salen del compromiso: 18 requerimientos, 136 SP | De 11 a 10 semanas; 3 sprints de 2 semanas | BAC de $15.000.000 a $13.650.000 CLP | ✅ Aprobada |

### Detalle RFC-003

- **Motivo:** en las pruebas, el optimizador en modo "mínimos km" usaba 3 de los 4 vehículos: un conductor hacía 25 paradas y otro ninguno. Un despachador real necesita repartir la jornada.
- **Solución:** penalizar la ruta más larga en la función objetivo. Con los datos de demo: 88 km con 3 vehículos frente a 102 km con 4 vehículos equilibrados (10–14 paradas cada uno). El ahorro frente a la planificación manual sigue en torno al 60 %.
- **Decisión:** se deja como opción para que el despachador elija entre menos km y reparto equilibrado.

### Detalle RFC-004

- **Motivo:** priorizar el objetivo del sprint (optimización funcionando) frente a la infraestructura geoespacial, que no aporta valor visible hasta tener consultas espaciales (Sprint 3).
- **Riesgo asociado:** R06 (cuotas de APIs). Nominatim limita a 1 petición/s; los CSV con coordenadas no hacen ninguna petición.

### Detalle RFC-001

- **Justificación:** el hito H3 (Demo Sprint 1) exige "setup + auth + pipeline CI", pero la hoja de requerimientos sitúa RF15 en el Sprint 5 y RF18 en el Sprint 6. Además, la app del repartidor (RF5, Sprint 2) depende de la integración de mapas (RF17).
- **Impacto en el alcance:** ninguno; los 20 requerimientos se mantienen.
- **Impacto en el tiempo:** el Sprint 1 pasa a 34 SP; se compensa moviendo RF13 y RF16 al Sprint 5.
- **Riesgo asociado:** R01 (el Sprint 1 concentra el algoritmo VRP); se mitiga con OR-Tools.
- **Decisión:** aprobada por el CCB antes de fijar la baseline (H2).

### Detalle RFC-005

- **Origen:** el Sponsor (profesor) fija las fechas de entrega el 19/10/2026. El calendario de 11 semanas del curso era referencial.
- **Análisis de impacto:**
  - *Tiempo:* quedan 6 semanas (20/10 – 30/11) en lugar de 7. Se organizan 3 sprints de 2 semanas para mantener las Sprint Reviews quincenales; la Entrega 2 (09/11) cae a mitad del Sprint 3 y se presenta con el Sprint 2 terminado.
  - *Alcance:* con la velocity del Sprint 1 (34 SP) caben 102 SP y quedaban 113. Se aplica el plan B ya previsto en el backlog: RF13 (Should, 8 SP) y RF20 (Could, 3 SP) salen del compromiso; se recuperan si sobra capacidad.
  - *Coste:* 90 h menos de capacidad → BAC de $13.650.000 CLP (re-baseline).
  - *Riesgos:* R04 (subestimación) sube a alto (16).
- **Alternativas descartadas:** 2 sprints de 3 semanas (se pierden las reviews quincenales que pide el curso); mantener los 20 requerimientos (exigiría 113 SP en 102 SP de capacidad).
- **Decisión:** aprobada por el CCB el 19/10/2026. Se actualizan el Charter, el backlog, la WBS, el cronograma, la RACI, el presupuesto, la matriz de riesgos y el plan de comunicaciones (versión 1.1).

