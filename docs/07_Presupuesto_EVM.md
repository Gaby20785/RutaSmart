# Presupuesto Base y Control EVM — RutaSmart (P05)

> Versión 1.1 · Baseline H2 + re-baseline del 19/10/2026 (RFC-005) · Responsable: Miembro 1 (PM)
> **Presupuesto simulado** · Tarifa única: 25 €/h · Moneda: EUR

---

## 1. Supuestos de estimación

- 6 personas × 15 h/semana × 10 semanas = **900 horas** (antes 11 semanas y 990 h; ver §7).
- Tarifa simulada homogénea de **25 €/h** para todos los roles.
- Herramientas en planes gratuitos (GitHub, Jira/Trello, Notion).
- Infraestructura cloud y APIs con consumo mínimo (planes de prueba / pago por uso).
- Reserva de contingencia del **10 %** para riesgos identificados (fuera del BAC; requiere aprobación del PM para usarla).

---

## 2. Presupuesto por paquete de trabajo (WBS) · baseline vigente v1.1

| WBS | Paquete | Horas | Coste (€) | % |
| --- | --- | --- | --- | --- |
| 1 | Gestión del proyecto | 140 | 3.500 | 15,5 % |
| 2 | Análisis y diseño | 75 | 1.875 | 8,3 % |
| 3 | Plataforma y DevOps | 65 | 1.625 | 7,2 % |
| 4 | Backend (FastAPI + VRP) | 225 | 5.625 | 24,8 % |
| 5 | Frontend – Panel web | 130 | 3.250 | 14,3 % |
| 6 | App repartidor (PWA) | 120 | 3.000 | 13,2 % |
| 7 | Integraciones | 30 | 750 | 3,3 % |
| 8 | Calidad y testing | 80 | 2.000 | 8,8 % |
| 9 | Documentación | 35 | 875 | 3,9 % |
| | **Subtotal mano de obra** | **900** | **22.500** | 99,3 % |
| — | Infraestructura cloud (3 meses × 30 €) | | 90 | 0,4 % |
| — | APIs externas (Mapbox, SMS) | | 60 | 0,3 % |
| | **Presupuesto base (BAC)** | | **22.650** | 100 % |
| — | Reserva de contingencia (10 %) | | 2.265 | |
| | **Presupuesto total autorizado** | | **24.915** | |

---

## 3. Curva de valor planificado (PV) · baseline vigente v1.1

Distribución según el cronograma (90 h/semana de equipo + 50 €/mes de costes externos):

| Mes | Periodo | Horas plan. | PV del mes (€) | PV acumulado (€) | % del BAC |
| --- | --- | --- | --- | --- | --- |
| Mes 1 | 21/09 – 18/10 | 360 | 9.050 | 9.050 | 40,0 % |
| Mes 2 | 19/10 – 15/11 | 360 | 9.050 | 18.100 | 79,9 % |
| Mes 3 | 16/11 – 30/11 | 180 | 4.550 | 22.650 | 100 % |

---

## 4. Cómo se mide el EVM

| Indicador | Fórmula | Interpretación |
| --- | --- | --- |
| **PV** (Planned Value) | Coste planificado del trabajo previsto hasta la fecha | Ver tabla anterior |
| **EV** (Earned Value) | BAC × % de avance real | % de avance = SP completados / 147 SP *(o paquetes WBS terminados)* |
| **AC** (Actual Cost) | Horas reales registradas × 25 € + gastos reales | Horas imputadas por cada miembro en el tablero |
| **SV** | EV − PV | > 0 adelantados · < 0 retrasados |
| **CV** | EV − AC | > 0 por debajo del presupuesto · < 0 sobrecoste |
| **SPI** | EV / PV | ≥ 1 en plazo · objetivo ≥ 0,9 |
| **CPI** | EV / AC | ≥ 1 eficiente · objetivo ≥ 0,9 |
| **EAC** | BAC / CPI | Coste final previsto |
| **ETC** | EAC − AC | Coste que falta |
| **VAC** | BAC − EAC | Desviación final prevista |

> **Medición del avance:** para las fases de gestión (S1–S2) se usa la regla 0/100 por entregable (Charter, WBS, riesgos… terminado = 100 %). Desde Sprint 1 se usan los story points completados según la Definition of Done.

---

## 5. Reporte EVM — Mes 1 (corte 18/10/2026)

> ⚠️ **Rellenar con datos reales** del equipo: horas registradas y story points terminados en el Sprint 1.

| Dato | Valor | Cómo obtenerlo |
| --- | --- | --- |
| PV | 9.050 € | De la curva de PV |
| % avance real | **37 %** | 18 % (gestión S1–S2 completa) + 34/147 SP × 82 % |
| EV | **9.213 €** | 24.900 × 0,37 |
| SPI | **1,02** | EV / PV → en plazo |
| Horas reales | `[___] h` | Suma de horas imputadas por M1–M6 |
| AC | `[horas × 25 + gastos]` | |
| SV = EV − PV | **+163 €** | |
| CV = EV − AC | | Requiere AC |
| CPI = EV / AC | | Requiere AC |
| EAC = BAC / CPI | | |

**Ejemplo de cálculo de % de avance a fin del Mes 1:**
Si la gestión (S1–S2) representa el 18 % del proyecto (180 h de 990) y en el Sprint 1 se completaron X SP de 147, que valen el 82 % restante:
`% avance = 18 % + (X / 147) × 82 %`
→ con X = 34 SP (sprint completo): 18 % + 19 % = **37 %** → EV = 9.213 € → SPI ≈ 1,02.

**Acciones correctivas** (si SPI o CPI < 0,9): `[describir]`

---

## 6. Control de la reserva de contingencia

| Fecha | Riesgo asociado | Importe usado | Saldo | Aprobado por |
| --- | --- | --- | --- | --- |
| 04/10/2026 | — | 0 € | 2.490 € | M1 |

---

## 7. Re-baseline del 19/10/2026 (RFC-005)

El Sponsor fijó las entregas el 09/11 y el 30/11: el proyecto pasa de 11 a 10 semanas.

| Concepto | Baseline original (v1.0) | Baseline vigente (v1.1) | Diferencia |
| --- | --- | --- | --- |
| Duración | 11 semanas (hasta 06/12) | 10 semanas (hasta 30/11) | −1 semana |
| Horas | 990 h | 900 h | −90 h |
| BAC | 24.900 € | 22.650 € | −2.250 € |
| Reserva (10 %) | 2.490 € | 2.265 € | −225 € |
| Alcance comprometido | 20 requerimientos · 147 SP | 18 requerimientos · 136 SP | RF13 y RF20 fuera |

- **El reporte del mes 1 (§5) se mantiene contra la baseline original**, que era la vigente en el corte del 18/10 (SPI 1,02).
- **Desde el mes 2 se mide contra la baseline v1.1.** Con ella, el avance acumulado al 18/10 es: gestión (180 h de 900 = 20 %) + 34 de 136 SP × 80 % (20 %) = **40 %**, es decir, EV = 9.060 € frente a PV = 9.050 € → SPI ≈ 1,00.

