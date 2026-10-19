# Plan de Comunicaciones y Stakeholders — RutaSmart (P05)

> Versión 1.0 · Hito H2 (Baseline) · Responsable: Miembro 1 (PM)

---

## 1. Registro de stakeholders

| ID | Stakeholder | Rol en el proyecto | Expectativas | Poder | Interés | Estrategia |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | Profesor/a – Panel evaluador | Sponsor: aprueba hitos y evalúa | Gestión rigurosa, MVP funcional, evidencias | Alto | Alto | **Gestionar de cerca** |
| S2 | Empresa de última milla (cliente simulado) | Usuario de negocio | Reducir km y costes, cumplir horarios | Alto | Alto | **Gestionar de cerca** |
| S3 | Despachador | Usuario principal del panel web | Planificar y supervisar rutas fácilmente | Medio | Alto | **Mantener informado** |
| S4 | Repartidor / conductor | Usuario de la app móvil | App rápida, sencilla, que funcione sin cobertura | Bajo | Alto | **Mantener informado** |
| S5 | Cliente final | Receptor de pedidos | Saber cuándo llega su pedido | Bajo | Medio | **Monitorear** |
| S6 | Equipo del proyecto (M1–M6) | Ejecuta el proyecto | Buen reparto, aprendizaje, buena nota | Medio | Alto | **Gestionar de cerca** |
| S7 | Proveedores (Mapbox, SMS, cloud) | Servicios externos | Uso dentro de las condiciones del servicio | Medio | Bajo | **Mantener satisfecho** |

### Matriz poder / interés

| | **Interés bajo** | **Interés alto** |
| --- | --- | --- |
| **Poder alto** | Mantener satisfecho: S7 | Gestionar de cerca: S1, S2, S6 |
| **Poder bajo** | Monitorear: S5 | Mantener informado: S3, S4 |

---

## 2. Matriz de comunicaciones

| Qué se comunica | Para quién | Frecuencia | Canal / formato | Responsable |
| --- | --- | --- | --- | --- |
| Kick-off y Project Charter | Sponsor, equipo | Una vez (S1) | Reunión + documento | M1 |
| Aprobación de la baseline | Sponsor | Una vez (S2) | Presentación + documentos | M1 |
| Daily Scrum | Equipo | L-X-V (resto asíncrona) | Videollamada 15 min / mensaje en canal | M3 |
| Estado del sprint | Equipo | Continuo | Tablero Jira/Trello | M3 |
| Sprint Review (demo) | Sponsor, equipo, usuarios invitados | Quincenal | Demo en vivo + acta | M2 |
| Retrospectiva | Equipo | Quincenal | Reunión + acta en wiki | M3 |
| Reporte de avance (estado, hitos, riesgos) | Sponsor | Quincenal | Informe de 1 página en wiki | M1 |
| Reporte EVM + 15 KPIs | Sponsor | Mensual (18/10, 15/11, 30/11) | Hoja "Métricas Seguimiento" + informe | M1 |
| Solicitudes de cambio (RFC) y decisiones CCB | Equipo, Sponsor | Cuando ocurran | Formulario RFC + registro de cambios | M2 |
| Alertas de riesgo o bloqueo crítico | PM → Sponsor | Inmediata (< 24 h) | Mensaje directo + reunión si hace falta | M1 |
| Prueba de uso guiada + encuesta | 3 personas ajenas al equipo | 26–29/11 | Entrevista / prueba guiada 20 min + formulario | M2 |
| Entregas formales (1, 2, 3) | Sponsor / panel | 19/10 · 09/11 · 30/11 | Presentación + documentación | M1 |
| Defensa final y lecciones aprendidas | Panel evaluador | 30/11 | Presentación + demo + documento | M1 |

---

## 3. Herramientas

| Herramienta | Uso |
| --- | --- |
| WhatsApp / Discord | Comunicación diaria del equipo y avisos rápidos |
| Google Meet / Teams | Ceremonias y reuniones con el Sponsor |
| Jira o Trello | Product Backlog, sprints, tablero Kanban, burndown |
| GitHub | Código, pull requests, issues, GitHub Actions (CI/CD) |
| Notion / Confluence (wiki) | Documentación, actas, reportes, evidencias para la rúbrica |
| Google Drive | Presentaciones y hojas de métricas |

---

## 4. Escalado de incidencias

| Nivel | Cuándo | Quién resuelve | Plazo |
| --- | --- | --- | --- |
| 1 | Bloqueo técnico o duda de una tarea | Miembros implicados / SM | < 24 h |
| 2 | Bloqueo que afecta al objetivo del sprint o conflicto en el equipo | PM + PO | < 48 h |
| 3 | Riesgo de incumplir un hito, cambio que afecta a la baseline | PM → Sponsor | Siguiente reunión o < 72 h |

---

## 5. Reglas de las reuniones

- Toda reunión tiene agenda previa y acta con decisiones y responsables.
- Las actas se publican en la wiki en menos de 24 h.
- Las decisiones que cambian alcance, tiempo o coste se registran como RFC.
