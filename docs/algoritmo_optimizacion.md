# Algoritmo de optimización de rutas — RutaSmart

> Versión inicial (Sprint 1). Se completará en el Sprint 5 (RF20).
> Código: [backend/app/services/optimizer.py](../backend/app/services/optimizer.py)

## 1. Problema

RutaSmart resuelve un **CVRPTW** (*Capacitated Vehicle Routing Problem with Time Windows*): dado un almacén, una flota de vehículos y un conjunto de pedidos, decidir **qué vehículo entrega cada pedido y en qué orden**, minimizando los kilómetros recorridos.

| Elemento | Modelado |
| --- | --- |
| Almacén | Un único punto de salida y llegada (configurable) |
| Vehículos | Capacidad en peso (kg) y volumen (m³) |
| Pedidos | Ubicación, peso, volumen, ventana horaria y tiempo de servicio |
| Turno | 08:00–20:00 (configurable) |
| Distancia | Haversine × factor de carretera 1,3 |
| Tiempo de viaje | Distancia / velocidad media (30 km/h en ciudad) |

## 2. Restricciones

1. **Capacidad:** la suma de peso y la de volumen de cada ruta no superan las del vehículo.
2. **Ventanas horarias:** la llegada a cada parada está dentro de su ventana; si se llega antes, se espera (máx. 4 h).
3. **Turno:** cada ruta sale y vuelve al almacén dentro del turno.
4. **Pedidos no servibles:** se descartan con un motivo en lugar de hacer el problema irresoluble.
   - Antes de optimizar: peso/volumen mayor que el de cualquier vehículo, o ventana fuera del turno.
   - Durante la optimización: cada pedido tiene una penalización muy alta si no se sirve (*disjunction*), así que solo se descarta cuando no hay forma de encajarlo.

## 3. Función objetivo

```text
minimizar   Σ distancia de todas las rutas
          + 2 × distancia de la ruta más larga        (solo si "equilibrar carga" está activo)
          + 10.000 km × nº de pedidos sin servir
```

El término de equilibrio reparte el trabajo entre conductores a costa de algunos km. En los datos de demo (40 pedidos, 4 vehículos):

| Modo | Km totales | Vehículos | Paradas por vehículo |
| --- | --- | --- | --- |
| Mínimos km | 88,0 | 3 | 4 / 11 / 25 |
| Equilibrado (por defecto) | 102,3 | 4 | 4 / 10 / 12 / 14 |

## 4. Método de resolución

Se usa **Google OR-Tools** (`pywrapcp` Routing Solver):

1. **Solución inicial:** `PATH_CHEAPEST_ARC` (desde cada nodo, ir al más cercano no visitado).
2. **Mejora:** búsqueda local con la metaheurística **Guided Local Search**, con límite de tiempo (3 s por defecto).
3. **Horarios:** tras optimizar, cada ruta se ajusta para terminar lo antes posible y, con ese final, salir lo más tarde posible (sin esperas innecesarias en la primera parada).

Se descartó una implementación propia del algoritmo por el riesgo **R01** de la matriz de riesgos (complejidad del VRP).

## 5. Indicador de ahorro

Para el objetivo **O2** del Project Charter (≥ 15 % menos km que la planificación manual), se compara con una **referencia sin optimizar**: los mismos pedidos en orden de alta, llenando cada vehículo hasta su capacidad. Es lo que haría un despachador sin herramienta.

El test `test_optimization_beats_sequential_baseline_by_15_percent` comprueba este objetivo con datos sintéticos.

## 6. Limitaciones y evolución

| Limitación actual | Mejora prevista | Sprint |
| --- | --- | --- |
| Distancias en línea recta × 1,3 | Matriz de distancias y tiempos reales de Mapbox | 2 (RF17) |
| Velocidad media constante | Tiempos por franja horaria (tráfico) | Fuera del MVP |
| Un solo almacén | Multi-depósito | Fuera del MVP |
| Plan estático | Reasignación dinámica ante averías | 3 (RF8) |
