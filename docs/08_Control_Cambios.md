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
| RFC-001 | 08/10/2026 | Mostrar las rutas en un mapa de OpenStreetMap desde el Sprint 1, sin esperar a la integración con Mapbox (Sprint 2) | M5 (Dev) | Sin cambio en los requerimientos | Sin impacto | $0 | ✅ Aprobada |
| RFC-002 | 15/10/2026 | Añadir al optimizador la opción «Equilibrar carga entre conductores» (activada por defecto) | M5 (Dev) | Mejora de RF3, sin historias nuevas | +1 SP absorbido en el Sprint 1 | $0 | ✅ Aprobada |
| RFC-003 | 19/10/2026 | Ajuste del calendario: el proyecto cierra el 30/11 (10 semanas en lugar de 11), con revisión intermedia el 09/11 | M1 (PM) | RF13 y RF20 salen del compromiso: 18 requerimientos, 136 SP | De 11 a 10 semanas; 3 sprints de 2 semanas | BAC de $15.000.000 a $13.650.000 | ✅ Aprobada |

> Las decisiones tomadas durante la planificación, antes de aprobar la baseline (H2), no se registran como RFC: el control de cambios aplica a la baseline aprobada.

### Detalle RFC-001 · Mapa con OpenStreetMap en el Sprint 1

- **Motivo:** el despachador necesita ver las rutas en un mapa para validar el resultado de la optimización, pero la integración con Mapbox (RF17) está planificada para el Sprint 2.
- **Solución:** usar los mapas gratuitos de OpenStreetMap (librería Leaflet) para dibujar las rutas desde el Sprint 1. Mapbox se incorpora en el Sprint 2 para el trazado por calles y la geocodificación.
- **Impacto:** ninguno en alcance, tiempo ni coste (no requiere cuenta ni clave de API).
- **Decisión:** aprobada por el CCB.

### Detalle RFC-002 · Equilibrar carga entre conductores

- **Motivo:** en las pruebas, el optimizador en modo «mínimos km» usaba 3 de los 4 vehículos: un conductor hacía 25 paradas y otro ninguno. Un despachador real necesita repartir la jornada.
- **Solución:** penalizar la ruta más larga en la función objetivo. Con los datos de demo: 88 km con 3 vehículos frente a 102 km con 4 vehículos equilibrados (10–14 paradas cada uno). El ahorro frente a la planificación manual sigue en torno al 60 %.
- **Decisión:** se deja como opción para que el despachador elija entre menos km y reparto equilibrado.

### Detalle RFC-003 · Ajuste del calendario

- **Origen:** al confirmar las fechas de entrega del proyecto (revisión intermedia el 09/11 y cierre el 30/11), el calendario de referencia de 11 semanas se reduce a 10.
- **Análisis de impacto:**
  - *Tiempo:* quedan 6 semanas (20/10 – 30/11) en lugar de 7. Se organizan 3 sprints de 2 semanas para mantener las Sprint Reviews quincenales; la revisión del 09/11 cae a mitad del Sprint 3 y se presenta con el Sprint 2 terminado.
  - *Alcance:* con la velocity del Sprint 1 (34 SP) caben 102 SP y quedaban 113. Se aplica el plan B ya previsto en el backlog: RF13 (Should, 8 SP) y RF20 (Could, 3 SP) salen del compromiso; se recuperan si sobra capacidad.
  - *Coste:* 90 h menos de capacidad → BAC de $13.650.000 (re-baseline).
  - *Riesgos:* R04 (subestimación) sube a alto (16).
- **Alternativas descartadas:** 2 sprints de 3 semanas (se pierden las reviews quincenales); mantener los 20 requerimientos (exigiría 113 SP con 102 SP de capacidad).
- **Decisión:** aprobada por el CCB el 19/10/2026. Se actualizan el Charter, el backlog, la WBS, el cronograma, la RACI, el presupuesto, la matriz de riesgos y el plan de comunicaciones (versión 1.1).
