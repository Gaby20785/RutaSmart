# Product Backlog — RutaSmart (P05)

> Versión 1.1 · Baseline H2, replanificada el 19/10/2026 (RFC-003) · Responsable: Product Owner
> Priorización MoSCoW · Estimación en story points (Fibonacci: 1, 2, 3, 5, 8, 13)

---

## 1. Roles de usuario

| Rol | Descripción |
|---|---|
| **Admin** | Gestiona la flota, los conductores, los vehículos y los usuarios del sistema. |
| **Despachador** | Carga pedidos, genera y asigna rutas, supervisa la operación en vivo. |
| **Conductor** | Ejecuta la ruta asignada desde la app móvil y registra las entregas. |
| **Cliente final** | Recibe el pedido y consulta su estado/ETA. |

---

## 2. Planificación de sprints

| Sprint | Semanas | Objetivo del sprint | SP |
|---|---|---|---|
| Sprint 1 | 05/10 – 18/10 | Base técnica + gestión de flota y pedidos + primera optimización | 34 ✅ |
| Sprint 2 | 20/10 – 02/11 | Ejecución de la ruta: asignación, app del repartidor y evidencia de entrega | 34 |
| Sprint 3 | 03/11 – 16/11 | Control de la operación: seguimiento en vivo, reasignación, KPIs y staging | 34 |
| Sprint 4 | 17/11 – 30/11 | Cliente final, latencia, offline, seguridad y UX (feature freeze 26/11) | 34 |
| **Comprometido** | | **18 requerimientos** | **136** |
| *Si sobra capacidad* | | *RF13 (escalabilidad 200 rutas) y RF20 (documentación del algoritmo)* | *11* |

> **Replanificación del 19/10/2026 (RFC-003):** con el ajuste del calendario (revisión intermedia el 09/11 y cierre el 30/11) quedan 3 sprints de 2 semanas en lugar de 4. Con la velocity del Sprint 1 (34 SP) caben 102 SP y quedaban 113. Se aplicó el plan B previsto: **RF13 y RF20 salen del compromiso** (11 SP). Seguimos en 18 requerimientos, por encima del mínimo de 16.

> **Decisiones de planificación (antes de aprobar la baseline):** la hoja P05 estima hasta 7 sprints, pero el calendario tiene 4, así que se reagruparon los requerimientos. RF15 (autenticación por rol) se priorizó como Must y se adelantó al Sprint 1, porque todas las pantallas dependen del rol del usuario. RF17 (integración con Mapbox) va en el Sprint 2 porque la app del repartidor depende de ella.

---

## 3. Backlog priorizado

### Sprint 1 (05/10 – 18/10) · Demo H3 · ✅ terminado

| ID | Req. | Historia de usuario | MoSCoW | SP |
|---|---|---|---|---|
| EN-01 | — | **Como** equipo, **quiero** el repositorio, la estructura del proyecto (React + FastAPI + PostGIS) y Docker, **para** poder desarrollar en un entorno común. | Must | 3 |
| HU-15 | RF15 | **Como** usuario, **quiero** iniciar sesión y acceder solo a las funciones de mi rol (admin, despachador, conductor), **para** proteger la información. | Should → **Must** | 5 |
| HU-18 | RF18 | **Como** equipo, **quiero** un pipeline CI que compile y ejecute los tests en cada push, **para** detectar errores pronto. *(CD y entornos se completan en Sprint 3)* | Could | 3 |
| HU-01 | RF1 | **Como** admin, **quiero** dar de alta conductores y vehículos con su capacidad (kg / m³), **para** que el sistema sepa qué recursos tengo. | Must | 5 |
| HU-02 | RF2 | **Como** despachador, **quiero** cargar pedidos con dirección, ventana horaria y peso/volumen (formulario o CSV), **para** planificar las entregas del día. | Must | 5 |
| HU-03 | RF3 | **Como** despachador, **quiero** generar automáticamente las rutas óptimas del día, **para** reducir kilómetros y cumplir las ventanas horarias. | Must | 13 |

### Sprint 2 (20/10 – 02/11) · Demo H4

| ID | Req. | Historia de usuario | MoSCoW | SP |
|---|---|---|---|---|
| HU-17 | RF17 | **Como** sistema, **quiero** integrarme con Mapbox (mapas, geocodificación, direcciones) y con un proveedor SMS, **para** ofrecer mapas y notificaciones. | Should | 5 |
| HU-04 | RF4 | **Como** despachador, **quiero** asignar cada ruta a un conductor y que reciba una notificación push, **para** que sepa qué tiene que hacer. | Must | 8 |
| HU-05 | RF5 | **Como** conductor, **quiero** ver mi ruta en un mapa con navegación paso a paso y marcar la llegada a cada parada, **para** seguir el orden óptimo. | Must | 13 |
| HU-06 | RF6 | **Como** conductor, **quiero** registrar firma, foto y observaciones al entregar, **para** tener prueba de la entrega. | Must | 8 |

### Sprint 3 (03/11 – 16/11) · Checkpoint H5 (09/11) · Demo H6

| ID | Req. | Historia de usuario | MoSCoW | SP |
|---|---|---|---|---|
| HU-07 | RF7 | **Como** despachador, **quiero** ver en un mapa la posición en vivo de todos los conductores y el estado de cada parada, **para** supervisar la operación. | Must | 8 |
| HU-08 | RF8 | **Como** despachador, **quiero** reasignar las paradas pendientes de un vehículo averiado a otros conductores, **para** no perder entregas. | Must | 13 |
| HU-09 | RF9 | **Como** despachador, **quiero** un panel con entregas/día, tiempo medio por entrega y tasa de éxito, **para** medir el rendimiento. | Must | 5 |
| HU-19 | RF19 | **Como** equipo, **quiero** tests unitarios y un simulador de rutas con datos sintéticos, **para** validar el algoritmo y evitar regresiones. | Could | 5 |
| HU-18b | RF18 | **Como** equipo, **quiero** despliegue continuo y entornos separados dev / staging / prod, **para** publicar versiones de forma segura. | Could | 3 |

### Sprint 4 (17/11 – 30/11) · Feature freeze H7 (26/11) · Entrega MVP H8

| ID | Req. | Historia de usuario | MoSCoW | SP |
|---|---|---|---|---|
| HU-10 | RF10 | **Como** cliente final, **quiero** recibir un SMS/email con la hora estimada y un enlace de seguimiento, **para** saber cuándo llega mi pedido. | Must | 5 |
| HU-11 | RF11 | **Como** despachador, **quiero** que la posición de los conductores se actualice en ≤ 5 segundos, **para** tomar decisiones con datos actuales. | Must | 8 |
| HU-12 | RF12 | **Como** conductor, **quiero** seguir trabajando sin cobertura y que los datos se sincronicen al recuperarla, **para** no perder entregas registradas. | Must | 13 |
| HU-14 | RF14 | **Como** responsable de datos, **quiero** que los datos personales del cliente final no aparezcan en claro en los logs, **para** cumplir la protección de datos. | Should | 3 |
| HU-16 | RF16 | **Como** conductor, **quiero** una interfaz con botones grandes y usable con una sola mano o con guantes, **para** operar con seguridad. | Should | 5 |

### Fuera del compromiso (solo si sobra capacidad) · RFC-003

| ID | Req. | Historia de usuario | MoSCoW | SP |
|---|---|---|---|---|
| HU-13 | RF13 | **Como** empresa, **quiero** que el sistema soporte 200 rutas simultáneas, **para** poder crecer sin cambiar de herramienta. | Should | 8 |
| HU-20 | RF20 | **Como** equipo, **quiero** documentar el algoritmo de optimización (modelo, restricciones, librería, limitaciones), **para** facilitar su mantenimiento. | Could | 3 |

---

## 4. Criterios de aceptación

### EN-01 · Setup del proyecto
- [ ] Repositorio en GitHub con README y estructura `frontend/`, `backend/`, `docs/`.
- [ ] `docker compose up` levanta frontend, backend y PostgreSQL + PostGIS.
- [ ] Ramas protegidas: `main` solo acepta merges vía pull request con revisión.

### HU-15 · Autenticación por rol
- [ ] **Dado** un usuario registrado, **cuando** introduce credenciales válidas, **entonces** recibe un token JWT y accede a su panel.
- [ ] **Dado** un conductor autenticado, **cuando** intenta acceder a una ruta de admin, **entonces** recibe un error 403.
- [ ] Las contraseñas se guardan con hash (bcrypt).

### HU-18 · Pipeline CI
- [ ] Cada push y pull request ejecuta lint + build + tests en GitHub Actions.
- [ ] Un pull request con tests fallidos no puede fusionarse.

### HU-01 · Alta de flota
- [ ] El admin puede crear, editar, listar y desactivar conductores (nombre, teléfono, licencia).
- [ ] El admin puede crear vehículos con matrícula, capacidad en kg y en m³.
- [ ] No se permiten matrículas duplicadas ni capacidades ≤ 0.

### HU-02 · Carga de pedidos
- [ ] El despachador puede crear un pedido con dirección, ventana horaria (desde–hasta) y peso/volumen.
- [ ] Puede importar pedidos desde un CSV; las filas con errores se informan sin bloquear el resto.
- [ ] La dirección se geocodifica y se guarda como punto geográfico (PostGIS).

### HU-03 · Optimización de rutas (VRP)
- [ ] **Dados** N pedidos y M vehículos, **cuando** pulso "Optimizar", **entonces** obtengo una ruta por vehículo en < 30 s para 100 pedidos.
- [ ] Ninguna ruta supera la capacidad del vehículo.
- [ ] Se respetan las ventanas horarias o se marcan los pedidos que no pueden cumplirse.
- [ ] Las rutas se muestran en el mapa con su orden de paradas y km totales.

### HU-17 · Integración Mapbox + SMS
- [ ] Geocodificación de direcciones y cálculo de trayectos mediante la API de Mapbox.
- [ ] Envío de SMS de prueba mediante el proveedor elegido.
- [ ] Las claves de API se guardan en variables de entorno, nunca en el código.

### HU-04 · Asignación con notificación push
- [ ] El despachador asigna una ruta a un conductor disponible desde el panel.
- [ ] El conductor recibe una notificación push en menos de 10 s.
- [ ] Un conductor no puede tener dos rutas activas el mismo día.

### HU-05 · App del repartidor
- [ ] El conductor ve sus paradas ordenadas y el trayecto en el mapa.
- [ ] Puede abrir la navegación paso a paso hasta la siguiente parada.
- [ ] El botón "He llegado" registra hora y coordenadas del check-in.

### HU-06 · Evidencia de entrega
- [ ] El conductor puede capturar firma en pantalla, foto con la cámara y observaciones.
- [ ] Puede marcar la entrega como "Entregado" o "Fallido" con un motivo.
- [ ] La evidencia queda visible para el despachador en el detalle del pedido.

### HU-07 · Seguimiento en vivo
- [ ] El panel muestra todos los conductores activos en el mapa, actualizándose automáticamente.
- [ ] Cada parada tiene un color según su estado (pendiente, entregada, fallida).
- [ ] Al hacer clic en un conductor se ve su ruta y su progreso.

### HU-08 · Reasignación dinámica
- [ ] El despachador marca un vehículo como "averiado".
- [ ] El sistema recalcula y propone repartir sus paradas pendientes entre los demás vehículos respetando capacidades.
- [ ] Los conductores afectados reciben notificación del cambio.

### HU-09 · Reportes de KPIs
- [ ] El panel muestra entregas/día, tiempo medio por entrega y tasa de éxito (%).
- [ ] Se puede filtrar por rango de fechas y por conductor.
- [ ] Los datos pueden exportarse a CSV.

### HU-19 · Tests + simulador
- [ ] Tests unitarios del algoritmo y de los endpoints principales.
- [ ] Script que genera pedidos sintéticos y compara km optimizados frente a asignación secuencial.
- [ ] Cobertura ≥ 40 % al final del Sprint 3 (meta ≥ 60 % el 30/11).

### HU-18b · CD + entornos
- [ ] Merge a `develop` despliega automáticamente en staging.
- [ ] Merge a `main` despliega en producción tras aprobación manual.
- [ ] Cada entorno tiene su propia base de datos y configuración.

### HU-10 · Notificación al cliente final
- [ ] Al iniciar la ruta, cada cliente recibe un SMS/email con ETA y un enlace.
- [ ] El enlace muestra el estado del pedido y la ETA, sin requerir login.
- [ ] El enlace solo muestra datos de ese pedido (token único no adivinable).

### HU-11 · Latencia ≤ 5 s
- [ ] La posición del conductor se envía al servidor cada ≤ 3 s mediante WebSocket.
- [ ] El panel refleja el cambio en ≤ 5 s (medido en pruebas con 50 conductores simulados).

### HU-12 · Modo offline
- [ ] Sin conexión, el conductor puede ver su ruta y registrar entregas.
- [ ] Los registros se guardan localmente y se sincronizan automáticamente al recuperar la conexión.
- [ ] No se duplican entregas tras la sincronización.

### HU-14 · Anonimización en logs
- [ ] Nombre, teléfono, email y dirección del cliente aparecen enmascarados en los logs.
- [ ] Existe un test automatizado que verifica el enmascarado.

### HU-13 · Escalabilidad 200 rutas
- [ ] Prueba de carga (k6/Locust) con 200 rutas activas simuladas sin errores.
- [ ] Tiempo de respuesta p95 de la API < 500 ms durante la prueba.

### HU-16 · UI para una mano / guantes
- [ ] Botones principales ≥ 48 × 48 px, en la zona inferior de la pantalla.
- [ ] Las acciones de entrega se completan en ≤ 3 toques.
- [ ] Validado con al menos 2 conductores reales.

### HU-20 · Documentación del algoritmo
- [ ] Documento con modelo VRP, restricciones, librería usada, parámetros y limitaciones.
- [ ] Incluye resultados del simulador (HU-19) con datos sintéticos.

---

## 5. Definition of Done (DoD)

Una historia se considera **terminada** cuando:

1. Cumple todos sus criterios de aceptación.
2. El código está revisado y aprobado por al menos otro miembro (code review).
3. Tiene tests automatizados y el pipeline CI está en verde.
4. Está desplegada en el entorno de staging (a partir del Sprint 3).
5. La documentación relevante (README / API) está actualizada.
6. El Product Owner la ha validado en la Sprint Review.

---

## 6. Resumen

| Prioridad | Nº requerimientos | SP |
|---|---|---|
| Must (incluye RF15 adelantado) | 13 | 109 |
| Should | 4 | 21 |
| Could | 3 (RF18 en 2 historias) | 14 |
| Habilitador técnico (EN-01) | — | 3 |
| **Total** | **20** | **147** |

> Para aprobar el MVP hacen falta ≥ 16 requerimientos. Tras RFC-003 hay **18 comprometidos (136 SP)**; RF13 y RF20 quedan fuera del compromiso. Si en el Checkpoint (09/11) la velocity baja, el siguiente candidato a recortar es **RF16** (17 requerimientos, todavía por encima del mínimo).
