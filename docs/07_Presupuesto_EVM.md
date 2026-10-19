# Presupuesto Base y Control EVM — RutaSmart (P05)

> Versión 1.1 · Baseline H2 + re-baseline del 19/10/2026 (RFC-003) · Responsable: Miembro 1 (PM)
> **Presupuesto simulado** · Tarifa única: $15.000 CLP/h · Moneda: pesos chilenos (CLP)

---

## 1. Supuestos de estimación

- 6 personas × 6 h/semana × 10 semanas = **360 horas** (antes 11 semanas y 396 h; ver §7). Dedicación parcial, compatible con otras asignaturas y trabajo.
- Tarifa simulada homogénea de **$15.000 CLP/h** para todos los roles (referencia: desarrollador junior en Chile).
- Herramientas en planes gratuitos (GitHub, Jira/Trello, Notion).
- Infraestructura cloud y APIs con consumo mínimo (planes de prueba / pago por uso): $30.000 CLP/mes de cloud y $60.000 CLP de APIs en total.
- Reserva de contingencia del **10 %** para riesgos identificados (fuera del BAC; requiere aprobación del PM para usarla).

---

## 2. Presupuesto por paquete de trabajo (WBS) · baseline vigente v1.1

| WBS | Paquete | Horas | Coste (CLP) | % |
| --- | --- | --- | --- | --- |
| 1 | Gestión del proyecto | 56 | $840.000 | 15,1 % |
| 2 | Análisis y diseño | 30 | $450.000 | 8,1 % |
| 3 | Plataforma y DevOps | 26 | $390.000 | 7,0 % |
| 4 | Backend (FastAPI + VRP) | 90 | $1.350.000 | 24,3 % |
| 5 | Frontend – Panel web | 52 | $780.000 | 14,1 % |
| 6 | App repartidor (PWA) | 48 | $720.000 | 13,0 % |
| 7 | Integraciones | 12 | $180.000 | 3,2 % |
| 8 | Calidad y testing | 32 | $480.000 | 8,6 % |
| 9 | Documentación | 14 | $210.000 | 3,8 % |
| | **Subtotal mano de obra** | **360** | **$5.400.000** | 97,3 % |
| — | Infraestructura cloud (3 meses × $30.000) | | $90.000 | 1,6 % |
| — | APIs externas (Mapbox, SMS) | | $60.000 | 1,1 % |
| | **Presupuesto base (BAC)** | | **$5.550.000** | 100 % |
| — | Reserva de contingencia (10 %) | | $555.000 | |
| | **Presupuesto total autorizado** | | **$6.105.000** | |

---

## 3. Curva de valor planificado (PV) · baseline vigente v1.1

Distribución según el cronograma (36 h/semana de equipo + $50.000 CLP/mes de costes externos):

| Mes | Periodo | Horas plan. | PV del mes | PV acumulado | % del BAC |
| --- | --- | --- | --- | --- | --- |
| Mes 1 | 21/09 – 18/10 | 144 | $2.210.000 | $2.210.000 | 39,8 % |
| Mes 2 | 19/10 – 15/11 | 144 | $2.210.000 | $4.420.000 | 79,6 % |
| Mes 3 | 16/11 – 30/11 | 72 | $1.130.000 | $5.550.000 | 100 % |

---

## 4. Cómo se mide el EVM

| Indicador | Fórmula | Interpretación |
| --- | --- | --- |
| **PV** (Planned Value) | Coste planificado del trabajo previsto hasta la fecha | Ver tabla anterior |
| **EV** (Earned Value) | BAC × % de avance real | % de avance = paquetes de gestión terminados + SP completados |
| **AC** (Actual Cost) | Horas reales × $15.000 + gastos reales | Horas registradas por cada miembro |
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

Medido contra la **baseline vigente en esa fecha (v1.0: 11 semanas, 396 h, BAC $6.090.000)**.

| Dato | Valor | Cómo se obtiene |
| --- | --- | --- |
| PV | $2.210.000 | 144 h × $15.000 + $50.000 |
| % avance real | **37 %** | 18 % (gestión S1–S2: 72 h de 396) + 34/147 SP × 82 % |
| EV | **$2.253.300** | $6.090.000 × 0,37 |
| SV = EV − PV | **+$43.300** | Ligeramente adelantados |
| SPI = EV / PV | **1,02** | En plazo |
| Horas reales | **≈ 130 h** | Estimación de cada integrante al cierre del Sprint 1 (≈ 5,4 h/semana por persona frente a 6 planificadas) |
| AC | **$1.950.000** | 130 h × $15.000 + $0 en servicios (planes gratuitos y entorno local) |
| CV = EV − AC | **+$303.300** | Por debajo del presupuesto |
| CPI = EV / AC | **1,16** | Cada $1 gastado produjo $1,16 de valor planificado |
| EAC = BAC / CPI | **$5.270.000** | Coste final previsto si se mantiene la eficiencia |
| ETC = EAC − AC | **$3.320.000** | Coste que falta |
| VAC = BAC − EAC | **+$820.000** | Ahorro final previsto |

**Lectura:** vamos en plazo (SPI 1,02) y con menos horas de las planificadas (CPI 1,16): el equipo dedicó unas 130 h frente a 144, y aun así completó lo previsto. Parte de la explicación es que usar una librería de optimización (OR-Tools) redujo el trabajo del algoritmo.

**Acción correctiva:** las horas del mes 1 se estimaron al cierre del sprint. Desde el Sprint 2 cada miembro registra sus horas a diario (acción de la retrospectiva). Además, se vigila que la menor dedicación no ponga en riesgo los sprints siguientes (R02).

---

## 6. Control de la reserva de contingencia

| Fecha | Riesgo asociado | Importe usado | Saldo | Aprobado por |
| --- | --- | --- | --- | --- |
| 04/10/2026 | — | $0 | $609.000 | M1 |
| 19/10/2026 | Re-baseline RFC-003 | $0 | $555.000 | M1 |

---

## 7. Re-baseline del 19/10/2026 (RFC-003)

Con el ajuste del calendario (revisión intermedia el 09/11 y cierre el 30/11) el proyecto pasa de 11 a 10 semanas.

| Concepto | Baseline original (v1.0) | Baseline vigente (v1.1) | Diferencia |
| --- | --- | --- | --- |
| Duración | 11 semanas (hasta 06/12) | 10 semanas (hasta 30/11) | −1 semana |
| Horas | 396 h | 360 h | −36 h |
| BAC | $6.090.000 | $5.550.000 | −$540.000 |
| Reserva (10 %) | $609.000 | $555.000 | −$54.000 |
| Alcance comprometido | 20 requerimientos · 147 SP | 18 requerimientos · 136 SP | RF13 y RF20 fuera |

- **El reporte del mes 1 (§5) se mantiene contra la baseline original**, que era la vigente en el corte del 18/10 (SPI 1,02).
- **Desde el mes 2 se mide contra la baseline v1.1.** Con ella, el avance acumulado al 18/10 es: gestión (72 h de 360 = 20 %) + 34 de 136 SP × 80 % (20 %) = **40 %**, es decir, EV = $2.220.000 frente a PV = $2.210.000 → SPI ≈ 1,00; y con AC = $1.950.000 → CPI ≈ 1,14.
