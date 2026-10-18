# Presupuesto Base y Control EVM — RutaSmart (P05)

> Versión 1.0 · Hito H2 (Baseline) · Responsable: Miembro 1 (PM)
> **Presupuesto simulado** · Tarifa única: 25 €/h · Moneda: EUR

---

## 1. Supuestos de estimación

- 6 personas × 15 h/semana × 11 semanas = **990 horas**.
- Tarifa simulada homogénea de **25 €/h** para todos los roles.
- Herramientas en planes gratuitos (GitHub, Jira/Trello, Notion).
- Infraestructura cloud y APIs con consumo mínimo (planes de prueba / pago por uso).
- Reserva de contingencia del **10 %** para riesgos identificados (fuera del BAC; requiere aprobación del PM para usarla).

---

## 2. Presupuesto por paquete de trabajo (WBS)

| WBS | Paquete | Horas | Coste (€) | % |
| --- | --- | --- | --- | --- |
| 1 | Gestión del proyecto | 150 | 3.750 | 15,1 % |
| 2 | Análisis y diseño | 80 | 2.000 | 8,0 % |
| 3 | Plataforma y DevOps | 70 | 1.750 | 7,0 % |
| 4 | Backend (FastAPI + VRP) | 250 | 6.250 | 25,1 % |
| 5 | Frontend – Panel web | 140 | 3.500 | 14,1 % |
| 6 | App repartidor (PWA) | 130 | 3.250 | 13,1 % |
| 7 | Integraciones | 30 | 750 | 3,0 % |
| 8 | Calidad y testing | 90 | 2.250 | 9,0 % |
| 9 | Documentación | 50 | 1.250 | 5,0 % |
| | **Subtotal mano de obra** | **990** | **24.750** | 99,4 % |
| — | Infraestructura cloud (3 meses × 30 €) | | 90 | 0,4 % |
| — | APIs externas (Mapbox, SMS) | | 60 | 0,2 % |
| | **Presupuesto base (BAC)** | | **24.900** | 100 % |
| — | Reserva de contingencia (10 %) | | 2.490 | |
| | **Presupuesto total autorizado** | | **27.390** | |

---

## 3. Curva de valor planificado (PV)

Distribución mensual según el cronograma (90 h/semana de equipo + 50 €/mes de costes externos):

| Mes | Semanas | Horas plan. | PV del mes (€) | PV acumulado (€) | % del BAC |
| --- | --- | --- | --- | --- | --- |
| Mes 1 | S1–S4 (21/09 – 18/10) | 360 | 9.050 | 9.050 | 36,3 % |
| Mes 2 | S5–S8 (19/10 – 15/11) | 360 | 9.050 | 18.100 | 72,7 % |
| Mes 3 | S9–S11 (16/11 – 06/12) | 270 | 6.800 | 24.900 | 100 % |

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
