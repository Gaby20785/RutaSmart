# Presupuesto Base y Control EVM — RutaSmart (P05)

> Versión 1.1 · Baseline H2 + re-baseline del 19/10/2026 (RFC-003) · Responsable: Miembro 1 (PM)
> **Presupuesto simulado** · Tarifa única: $15.000 CLP/h · Moneda: pesos chilenos (CLP)

---

## 1. Supuestos de estimación

- 6 personas × 15 h/semana × 10 semanas = **900 horas** (antes 11 semanas y 990 h; ver §7).
- Tarifa simulada homogénea de **$15.000 CLP/h** para todos los roles (referencia: desarrollador junior en Chile).
- Herramientas en planes gratuitos (GitHub, Jira/Trello, Notion).
- Infraestructura cloud y APIs con consumo mínimo (planes de prueba / pago por uso): $30.000 CLP/mes de cloud y $60.000 CLP de APIs en total.
- Reserva de contingencia del **10 %** para riesgos identificados (fuera del BAC; requiere aprobación del PM para usarla).

---

## 2. Presupuesto por paquete de trabajo (WBS) · baseline vigente v1.1

| WBS | Paquete | Horas | Coste (CLP) | % |
| --- | --- | --- | --- | --- |
| 1 | Gestión del proyecto | 140 | $2.100.000 | 15,4 % |
| 2 | Análisis y diseño | 75 | $1.125.000 | 8,2 % |
| 3 | Plataforma y DevOps | 65 | $975.000 | 7,1 % |
| 4 | Backend (FastAPI + VRP) | 225 | $3.375.000 | 24,7 % |
| 5 | Frontend – Panel web | 130 | $1.950.000 | 14,3 % |
| 6 | App repartidor (PWA) | 120 | $1.800.000 | 13,2 % |
| 7 | Integraciones | 30 | $450.000 | 3,3 % |
| 8 | Calidad y testing | 80 | $1.200.000 | 8,8 % |
| 9 | Documentación | 35 | $525.000 | 3,8 % |
| | **Subtotal mano de obra** | **900** | **$13.500.000** | 98,9 % |
| — | Infraestructura cloud (3 meses × $30.000) | | $90.000 | 0,7 % |
| — | APIs externas (Mapbox, SMS) | | $60.000 | 0,4 % |
| | **Presupuesto base (BAC)** | | **$13.650.000** | 100 % |
| — | Reserva de contingencia (10 %) | | $1.365.000 | |
| | **Presupuesto total autorizado** | | **$15.015.000** | |

---

## 3. Curva de valor planificado (PV) · baseline vigente v1.1

Distribución según el cronograma (90 h/semana de equipo + $50.000 CLP/mes de costes externos):

| Mes | Periodo | Horas plan. | PV del mes | PV acumulado | % del BAC |
| --- | --- | --- | --- | --- | --- |
| Mes 1 | 21/09 – 18/10 | 360 | $5.450.000 | $5.450.000 | 39,9 % |
| Mes 2 | 19/10 – 15/11 | 360 | $5.450.000 | $10.900.000 | 79,9 % |
| Mes 3 | 16/11 – 30/11 | 180 | $2.750.000 | $13.650.000 | 100 % |

---

## 4. Cómo se mide el EVM

| Indicador | Fórmula | Interpretación |
| --- | --- | --- |
| **PV** (Planned Value) | Coste planificado del trabajo previsto hasta la fecha | Ver tabla anterior |
| **EV** (Earned Value) | BAC × % de avance real | % de avance = paquetes de gestión terminados + SP completados |
| **AC** (Actual Cost) | Horas reales registradas × $15.000 + gastos reales | Horas imputadas por cada miembro en el tablero |
| **SV** | EV − PV | > 0 adelantados · < 0 retrasados |
| **CV** | EV − AC | > 0 por debajo del presupuesto · < 0 sobrecoste |
| **SPI** | EV / PV | ≥ 1 en plazo · objetivo ≥ 0,9 |
| **CPI** | EV / AC | ≥ 1 eficiente · objetivo ≥ 0,9 |
| **EAC** | BAC / CPI | Coste final previsto |
| **ETC** | EAC − AC | Coste que falta |
| **VAC** | BAC − EAC | Desviación final prevista |

> **Medición del avance:** para las fases de gestión (S1–S2) se usa la regla 0/100 por entregable (Charter, WBS, riesgos… terminado = 100 %). Desde el Sprint 1 se usan los story points completados según la Definition of Done.

---

## 5. Reporte EVM — Mes 1 (corte 18/10/2026)

Medido contra la **baseline vigente en esa fecha (v1.0: 11 semanas, 990 h, BAC $15.000.000)**.

| Dato | Valor | Cómo se obtiene |
| --- | --- | --- |
| PV | $5.450.000 | 360 h × $15.000 + $50.000 |
| % avance real | **37 %** | 18 % (gestión S1–S2: 180 h de 990) + 34/147 SP × 82 % |
| EV | **$5.550.000** | $15.000.000 × 0,37 |
| SV = EV − PV | **+$100.000** | Ligeramente adelantados |
| SPI = EV / PV | **1,02** | En plazo |
| Horas reales | **320 h** | Estimación de cada integrante al cierre del Sprint 1 (≈ 13 h/semana por persona frente a 15 planificadas) |
| AC | **$4.800.000** | 320 h × $15.000 + $0 en servicios (todo en planes gratuitos y entorno local) |
| CV = EV − AC | **+$750.000** | Por debajo del presupuesto |
| CPI = EV / AC | **1,16** | Cada $1 gastado produjo $1,16 de valor planificado |
| EAC = BAC / CPI | **$12.970.000** | Coste final previsto si se mantiene la eficiencia |
| ETC = EAC − AC | **$8.170.000** | Coste que falta |
| VAC = BAC − EAC | **+$2.030.000** | Ahorro final previsto |

**Lectura:** vamos en plazo (SPI 1,02) y con menos horas de las planificadas (CPI 1,16): el equipo dedicó unas 320 h frente a 360, y aun así completó lo previsto. Parte de la explicación es que usar una librería de optimización (OR-Tools) redujo el trabajo del algoritmo.

**Acción correctiva:** las horas del mes 1 se estimaron al cierre del sprint. Desde el Sprint 2 cada miembro registra sus horas a diario en el tablero (acción de la retrospectiva). Además, se vigila que la menor dedicación no ponga en riesgo los sprints siguientes (R02).

---

## 6. Control de la reserva de contingencia

| Fecha | Riesgo asociado | Importe usado | Saldo | Aprobado por |
| --- | --- | --- | --- | --- |
| 04/10/2026 | — | $0 | $1.500.000 | M1 |
| 19/10/2026 | Re-baseline RFC-003 | $0 | $1.365.000 | M1 |

---

## 7. Re-baseline del 19/10/2026 (RFC-003)

Con el ajuste del calendario (revisión intermedia el 09/11 y cierre el 30/11) el proyecto pasa de 11 a 10 semanas.

| Concepto | Baseline original (v1.0) | Baseline vigente (v1.1) | Diferencia |
| --- | --- | --- | --- |
| Duración | 11 semanas (hasta 06/12) | 10 semanas (hasta 30/11) | −1 semana |
| Horas | 990 h | 900 h | −90 h |
| BAC | $15.000.000 | $13.650.000 | −$1.350.000 |
| Reserva (10 %) | $1.500.000 | $1.365.000 | −$135.000 |
| Alcance comprometido | 20 requerimientos · 147 SP | 18 requerimientos · 136 SP | RF13 y RF20 fuera |

- **El reporte del mes 1 (§5) se mantiene contra la baseline original**, que era la vigente en el corte del 18/10 (SPI 1,02).
- **Desde el mes 2 se mide contra la baseline v1.1.** Con ella, el avance acumulado al 18/10 es: gestión (180 h de 900 = 20 %) + 34 de 136 SP × 80 % (20 %) = **40 %**, es decir, EV = $5.460.000 frente a PV = $5.450.000 → SPI ≈ 1,00; y con AC = $4.800.000 → CPI ≈ 1,14.
