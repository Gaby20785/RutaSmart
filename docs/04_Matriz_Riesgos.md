# Matriz de Riesgos — RutaSmart (P05)

> Versión 1.0 · Hito H2 (Baseline) · Responsable: Miembro 1 (PM)
> Revisión: **quincenal**, al final de cada sprint (y siempre que se active un disparador)

---

## 1. Escalas

| Valor | Probabilidad | Impacto (alcance / tiempo / coste / calidad) |
| --- | --- | --- |
| 1 | Muy baja (< 10 %) | Insignificante: sin efecto visible |
| 2 | Baja (10–30 %) | Menor: retraso < 2 días o tarea secundaria afectada |
| 3 | Media (30–50 %) | Moderado: retraso de 2–5 días o un requerimiento Should afectado |
| 4 | Alta (50–70 %) | Grave: retraso > 1 semana o un requerimiento Must afectado |
| 5 | Muy alta (> 70 %) | Crítico: pone en riesgo el MVP (< 16 requerimientos) o un hito |

**Exposición = Probabilidad × Impacto** → 🟢 Baja (1–6) · 🟡 Media (8–12) · 🔴 Alta (15–25)

---

## 2. Registro de riesgos

| ID | Categoría | Riesgo (causa → efecto) | P | I | P×I | Estrategia | Plan de respuesta | Responsable | Disparador / KRI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R01 | Técnico | El algoritmo VRP con capacidades y ventanas horarias es más complejo de lo previsto → retraso del Sprint 1 y de la ruta crítica | 4 | 5 | 🔴 20 | Mitigar | Usar Google OR-Tools en lugar de implementación propia; empezar con VRP de capacidad y añadir ventanas horarias después; spike técnico en S3 | M5 | Tiempo de cálculo > 30 s para 100 pedidos o HU-03 sin terminar al día 7 del sprint |
| R02 | Recursos | Baja disponibilidad de miembros por exámenes, trabajo u otras asignaturas → menor velocity | 4 | 4 | 🔴 16 | Mitigar | Buffer del 10 % en capacidad; parejas de backup por área (RACI); calendario compartido de ausencias | M1 | Velocity < 80 % de la planificada en un sprint |
| R03 | Técnico | El modo offline y la sincronización generan conflictos o duplicados → RF12 incompleto | 3 | 5 | 🔴 15 | Mitigar | Prototipo con Service Worker + IndexedDB en Sprint 2; IDs generados en cliente para evitar duplicados | M6 | Prototipo no funcional al final de S6 |
| R04 | Planificación | Subestimación del esfuerzo de las historias (equipo sin histórico de velocity) → no se cierran los Must | 4 | 3 | 🟡 12 | Mitigar | Recalibrar estimaciones tras Sprint 1; priorizar Must; lista de recorte acordada (RF13, RF16, RF20) | M2 | SP completados < 75 % de los comprometidos |
| R05 | Técnico | La actualización de posición supera los 5 s con muchos conductores → incumplimiento de RF11 | 3 | 4 | 🟡 12 | Mitigar | WebSockets desde el primer momento; prueba de carga con conductores simulados en Sprint 3 | M4 | Latencia p95 > 5 s en pruebas |
| R06 | Externo / coste | Superar la cuota gratuita de Mapbox o del proveedor SMS → coste extra o servicio bloqueado | 3 | 3 | 🟡 9 | Mitigar | Caché de geocodificación; modo "mock" en dev y tests; alertas de uso; límite de SMS en staging | M5 | Uso > 70 % de la cuota mensual |
| R07 | Alcance | Scope creep: añadir funcionalidades no previstas (p. ej. multi-depósito, IA) → retrasos | 3 | 3 | 🟡 9 | Evitar | Todo cambio pasa por RFC y CCB; el PO protege el sprint en curso | M2 | Nº de RFC > 3 por sprint o tareas no planificadas en el tablero |
| R08 | Equipo | Conflictos o mala comunicación entre miembros → bloqueos y retrabajo | 2 | 4 | 🟡 8 | Mitigar | Acuerdos de equipo, dailies, retrospectivas; escalado al PM y luego al Sponsor | M3 | Satisfacción del equipo < 3/5 o bloqueos > 2 días |
| R09 | Calidad | Cobertura de tests insuficiente → defectos en la demo | 3 | 3 | 🟡 9 | Mitigar | Tests en la Definition of Done; el CI bloquea merges con tests fallidos; medir cobertura en cada PR | M6 | Cobertura < 40 % en S6 |
| R10 | Usuarios | No conseguir 3 personas ajenas al equipo para la prueba de uso → requisito de evaluación incumplido | 1 | 4 | 🟢 4 | Mitigar | Pedirlo a compañeros de otros grupos o familiares; guion de tareas de 20 min y encuesta breve | M2 | Menos de 3 personas confirmadas el 16/11 |
| R11 | Técnico | Fallo en el despliegue o caída de staging el día de la demo → demo fallida | 2 | 5 | 🟡 10 | Mitigar | Demo grabada de respaldo; feature freeze en H7; despliegue final 48 h antes | M6 | Change failure rate > 20 % |
| R12 | Legal / seguridad | Exposición de datos personales del cliente (direcciones, teléfonos) en logs o enlaces → incumplimiento RGPD | 2 | 4 | 🟡 8 | Mitigar | Datos sintéticos en dev; anonimización en logs (RF14); tokens no adivinables en enlaces de tracking | M4 | Datos personales detectados en logs en revisión |
| R13 | Técnico | Cambios o limitaciones en APIs externas (notificaciones push en iOS para PWA) → push no funciona en algunos móviles | 3 | 2 | 🟢 6 | Aceptar | Alternativa: notificación por SMS/email y aviso dentro de la app | M6 | Push no recibido en pruebas con iOS |
| R14 | Gestión | Documentación de gestión desactualizada respecto al avance real → baja nota en rúbrica | 2 | 3 | 🟢 6 | Mitigar | Actualizar artefactos en cada review; checklist de entrega por hito | M1 | Artefacto con fecha > 2 semanas |

---

## 3. Mapa de calor (situación actual, 19/10/2026)

| Probabilidad ↓ / Impacto → | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| **5** | | | | | |
| **4** | | | | R02, R04 | |
| **3** | | R13 | R06, R07, R09 | R05 | R03 |
| **2** | | | R14, R15 | R08, R12 | R01, R11 |
| **1** | | | | R10 | |

**Riesgos prioritarios (rojo):** R02 (disponibilidad del equipo), R04 (subestimación, sube tras RFC-005) y R03 (modo offline). En la baseline (04/10) eran R01, R02 y R03; R01 bajó tras el Sprint 1.

---

## 4. Planes de contingencia (riesgos altos)

| Riesgo | Si se materializa… |
| --- | --- |
| R01 | Usar heurística simple (vecino más cercano + 2-opt) que respete capacidad; ventanas horarias pasan a Sprint 3 vía RFC. |
| R02 | Redistribuir historias según RACI de backup; mover Should/Could del sprint afectado; usar reserva de contingencia. |
| R03 | Reducir alcance offline a "solo lectura de ruta + cola de entregas" y sincronizar manualmente con un botón. |

---

## 5. Seguimiento

| Fecha | Riesgos activos (alto impacto) | Nuevos | Cerrados | Comentario |
| --- | --- | --- | --- | --- |
| 04/10/2026 (H2) | 3 | 14 | 0 | Baseline inicial |
| 18/10/2026 (H3) | 2 | 1 (R15) | 0 | **R01 baja a 🟡 (P 2 × I 5 = 10):** el VRP con OR-Tools funciona (40 pedidos en 3 s, todos los tests en verde). R02 y R03 siguen altos. Nuevo **R15**. |

### Riesgos nuevos tras el Sprint 1

| ID | Categoría | Riesgo | P | I | P×I | Estrategia | Plan de respuesta | Responsable | Disparador |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R15 | Técnico | Diferencias de comportamiento entre SQLite (desarrollo) y PostgreSQL (staging) → errores que solo aparecen al desplegar | 2 | 3 | 🟢 6 | Mitigar | Probar con `docker compose` (PostgreSQL + PostGIS) antes de cada demo; añadir job de tests con PostgreSQL en CI (Sprint 3) | M6 | Fallo en staging no reproducible en local |

**Revisión del 19/10/2026 (RFC-005):** el Sponsor adelanta las entregas (09/11 y 30/11) y el proyecto pasa de 11 a 10 semanas. **R04 (subestimación) sube a 🔴 (P 4 × I 4 = 16)** porque queda menos margen; se mitiga sacando RF13 y RF20 del compromiso (plan B) y dejando RF16 como siguiente recorte. R02 se mantiene en 🔴.

**Incidencia detectada en el Sprint 1:** el healthcheck de PostgreSQL en Docker daba el servicio por listo antes de tiempo y el backend no arrancaba. Se corrigió y dio origen a R15.
