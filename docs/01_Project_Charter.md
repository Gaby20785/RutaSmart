# Project Charter — RutaSmart (P05)

> Optimizador de rutas de entrega con seguimiento en vivo
> Versión 1.0 · Hito H1 (Kick-off) · Estado: **Borrador para aprobación**

---

## 1. Información general

| Campo | Valor |
|---|---|
| Nombre del proyecto | RutaSmart — Optimizador de Entregas |
| Código | P05 |
| Sector | Logística de última milla |
| Metodología | Híbrida: PMI (gobierno) + Scrum (ejecución) |
| Duración | 11 semanas (S1–S11) |
| Fecha de inicio | 21/09/2026 (S1 · selección del proyecto el 25/09) |
| Fecha de entrega MVP | 06/12/2026 (S11 · H8) |
| Patrocinador (Sponsor) | Profesor/a – Panel evaluador |
| Equipo | 6 personas (Miembro 1 – Miembro 6) |
| Project Manager | Miembro 1 *(propuesta)* |
| Product Owner | Miembro 2 *(propuesta)* |

---

## 2. Propósito y justificación

Las empresas pequeñas y medianas de reparto de última milla suelen planificar las rutas a mano (hojas de cálculo, WhatsApp, conocimiento del conductor). Esto provoca:

- Más kilómetros y combustible de los necesarios.
- Incumplimiento de ventanas horarias y clientes insatisfechos.
- Nula visibilidad en tiempo real para el despachador.
- Ausencia de prueba de entrega ante reclamaciones.

**RutaSmart** es una plataforma web + app para repartidores que **optimiza automáticamente las rutas**, permite **seguir la flota en vivo** y registra **evidencia de entrega** (firma, foto, observaciones), reduciendo costes operativos y mejorando la experiencia del cliente final.

---

## 3. Objetivos del proyecto (SMART)

| # | Objetivo | Métrica / Criterio | Plazo |
|---|---|---|---|
| O1 | Entregar un MVP funcional desplegado en staging | ≥ 16 de 20 requerimientos cerrados (meta: 20) | S11 |
| O2 | Optimizar rutas frente a una asignación manual | ≥ 15 % menos km totales en simulación con datos sintéticos | S8 |
| O3 | Seguimiento en vivo fiable | Latencia de actualización de posición ≤ 5 s | S10 |
| O4 | Calidad del software | Cobertura de tests ≥ 40 % en S6 y ≥ 60 % en S11 | S6 / S11 |
| O5 | Gestión dentro de línea base | SPI ≥ 0,9 y CPI ≥ 0,9 en cada reporte mensual | Mensual |
| O6 | Validación con usuarios | Feedback documentado de ≥ 3 usuarios reales | S11 |

---

## 4. Alcance

### 4.1 Dentro del alcance

- **Panel web (React)** para administrador y despachador:
  - Alta de flota, conductores y vehículos con capacidades.
  - Carga de pedidos (dirección, ventana horaria, peso/volumen).
  - Optimización automática de rutas (VRP básico con capacidad y ventanas horarias).
  - Asignación y reasignación dinámica de rutas.
  - Seguimiento en vivo de la flota sobre mapa.
  - Reportes de KPIs (entregas/día, tiempo promedio, tasa de éxito).
- **App del repartidor (PWA móvil)**: ruta del día, navegación turn-by-turn, check-in por parada, evidencia de entrega, modo offline con sincronización y UI usable con una mano.
- **Notificación al cliente final** con ETA y enlace de seguimiento (SMS/email).
- **Backend (FastAPI + PostgreSQL/PostGIS)** con autenticación por roles (admin, despachador, conductor).
- **Integraciones**: Mapbox (o Google Maps) y proveedor SMS.
- **DevOps**: repositorio Git, pipeline CI/CD, entornos dev / staging / prod.
- **Documentación**: arquitectura, API, algoritmo de optimización y manual de usuario.

### 4.2 Fuera del alcance

- Facturación, cobros o pasarela de pago.
- Integración con ERPs o marketplaces externos.
- Apps nativas publicadas en App Store / Google Play (se usa PWA).
- Optimización avanzada multi-depósito o con tráfico predictivo por IA.
- Soporte multi-idioma y multi-empresa (multi-tenant).

---

## 5. Entregables principales

| Tipo | Entregable |
|---|---|
| Gestión | Project Charter · WBS + Gantt · Product Backlog priorizado · Matriz de riesgos · Plan de comunicaciones · RACI · Presupuesto base (BAC) |
| Seguimiento | Reporte EVM mensual · Retrospectivas por sprint · Hoja de 15 KPIs · Dashboard DORA · Registro de cambios (RFC) |
| Producto | MVP desplegado en staging · Repositorio público · Demo grabada |
| Cierre | Documentación técnica · Feedback de usuarios · Lecciones aprendidas · Acta de cierre |

---

## 6. Hitos y entregas

| Hito | Semana | Fecha | Descripción | Entrega |
|---|---|---|---|---|
| H1 | S1 | 27/09/2026 | Kick-off: Charter y stakeholders aprobados | **Entrega 1** (19/10) |
| H2 | S2 | 04/10/2026 | Baseline aprobada: WBS, Gantt, presupuesto, riesgos, comunicaciones | **Entrega 1** (19/10) |
| H3 | S4 | 18/10/2026 | Demo Sprint 1: setup, autenticación, CI, flota, pedidos y optimización básica | **Entrega 1** (19/10) |
| H4 | S6 | 01/11/2026 | Demo Sprint 2: asignación, app repartidor, evidencia de entrega · tests > 40 % | Entrega 2 (~16/11) |
| H5 | S8 | 15/11/2026 | Demo Sprint 3 + Checkpoint intermedio: replanificación | Entrega 2 (~16/11) |
| H6 | S10 | 29/11/2026 | Demo Sprint 4: hardening, seguridad, offline, notificaciones | Entrega 3 (~07/12) |
| H7 | S11 | 03/12/2026 | Feature freeze: solo corrección de errores | Entrega 3 (~07/12) |
| H8 | S11 | 06/12/2026 | Entrega MVP + defensa + cierre formal | Entrega 3 (~07/12) |

*Fechas de las entregas 2 y 3 estimadas; se ajustarán cuando el profesor las confirme.*

---

## 7. Supuestos y restricciones

**Supuestos**
- El equipo dedica ~15 h/semana por persona durante las 11 semanas.
- Los planes gratuitos o de prueba de Mapbox y del proveedor SMS son suficientes para el MVP.
- Se utilizan datos sintéticos de pedidos y direcciones (no datos reales de clientes).
- Se puede acceder a ≥ 3 usuarios (repartidores/despachadores) para pruebas y feedback.

**Restricciones**
- Plazo fijo: entrega en S11, sin posibilidad de ampliación.
- Stack sugerido: React, FastAPI, PostGIS, Mapbox.
- Mínimo 16 de 20 requerimientos para aprobar el MVP.
- Presupuesto simulado limitado (ver §9).
- Cumplimiento básico de protección de datos (anonimización de datos personales en logs).

---

## 8. Riesgos de alto nivel

| # | Riesgo | Prob. | Impacto | Respuesta inicial |
|---|---|---|---|---|
| R1 | Complejidad del algoritmo VRP supera la capacidad del equipo | Alta | Alto | Usar librería probada (Google OR-Tools) en lugar de implementación propia |
| R2 | Superar cuota gratuita de Mapbox/SMS | Media | Medio | Caché de geocodificación, límites de uso, modo simulado en dev |
| R3 | Modo offline y sincronización más complejos de lo previsto | Media | Alto | Prototipo técnico temprano (spike) en Sprint 2 |
| R4 | No alcanzar latencia ≤ 5 s en seguimiento en vivo | Media | Medio | WebSockets desde el inicio; prueba de carga en Sprint 3 |
| R5 | Baja disponibilidad de miembros del equipo (exámenes, trabajo) | Media | Alto | Buffer del 10 % en cronograma, RACI con suplentes |

*Matriz completa (P×I, responsables, KRIs) en [04_Matriz_Riesgos.md](04_Matriz_Riesgos.md).*

---

## 9. Presupuesto resumido (simulado)

| Concepto | Cálculo | Importe |
|---|---|---|
| Recursos humanos | 6 personas × 15 h/sem × 11 sem × 25 €/h (990 h) | 24.750 € |
| Infraestructura cloud (staging + prod) | 3 meses × 30 € | 90 € |
| APIs externas (Mapbox, SMS) | Estimado | 60 € |
| Herramientas (Jira/Trello, GitHub) | Planes gratuitos | 0 € |
| **Presupuesto base (BAC)** | | **24.900 €** |
| Reserva de contingencia (10 %) | | 2.490 € |
| **Presupuesto total autorizado** | | **27.390 €** |

*Presupuesto simulado. Desglose por paquete de trabajo en [07_Presupuesto_EVM.md](07_Presupuesto_EVM.md).*

---

## 10. Stakeholders principales

| Stakeholder | Rol / Interés | Poder | Interés |
|---|---|---|---|
| Panel evaluador (Sponsor) | Aprueba hitos y evalúa gestión y MVP | Alto | Alto |
| Empresa de última milla (cliente) | Reducir costes y mejorar puntualidad | Alto | Alto |
| Despachador | Planificar, asignar y supervisar rutas | Medio | Alto |
| Repartidor / conductor | Ruta clara, app sencilla y rápida | Bajo | Alto |
| Cliente final | Saber cuándo llega su pedido | Bajo | Medio |
| Equipo del proyecto | Entregar el MVP y aprender | Medio | Alto |
| Proveedores (Mapbox, SMS, cloud) | Servicio contratado | Medio | Bajo |

---

## 11. Equipo y roles

| Miembro | Rol | Responsabilidades principales |
|---|---|---|
| Miembro 1 | Project Manager | Plan de proyecto, cronograma, EVM, riesgos, comunicaciones, control de cambios |
| Miembro 2 | Product Owner + UX/UI | Backlog, priorización, criterios de aceptación, mockups, relación con usuarios |
| Miembro 3 | Scrum Master + Dev Frontend | Ceremonias Scrum, métricas ágiles, panel web React |
| Miembro 4 | Dev Backend | API FastAPI, autenticación, base de datos, tracking en tiempo real |
| Miembro 5 | Dev Backend – Algoritmo y GIS | Motor de optimización VRP, PostGIS, integración Mapbox |
| Miembro 6 | QA / DevOps + Dev Mobile | CI/CD, entornos, tests, métricas DORA, app PWA del repartidor |

*Asignación propuesta, pendiente de confirmar por el equipo. Matriz RACI en [05_RACI.md](05_RACI.md).*

---

## 12. Criterios de éxito y aprobación

El proyecto se considerará exitoso si:

1. El MVP se despliega en staging con **≥ 16 requerimientos** cerrados y la demo se realiza sin fallos críticos.
2. Se entregan los **10 artefactos obligatorios** de gestión.
3. Los índices **SPI y CPI se mantienen ≥ 0,9**.
4. Se obtiene feedback positivo (≥ 3,5/5) de al menos **3 usuarios reales**.

---

## 13. Aprobación

| Rol | Nombre | Firma | Fecha |
|---|---|---|---|
| Sponsor | | | |
| Project Manager | | | |
| Product Owner | | | |
