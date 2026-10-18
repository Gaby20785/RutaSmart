"""Optimización de rutas (CVRPTW) con Google OR-Tools.

Modelo:
- Un único depósito del que salen y al que vuelven todos los vehículos.
- Capacidad en peso (kg) y en volumen (m³) por vehículo.
- Ventanas horarias por pedido y turno de reparto por vehículo.
- Distancias: haversine × factor de carretera (en el Sprint 2 se sustituye por la
  matriz de distancias de Mapbox, RF17).
- Objetivo: minimizar la distancia total. Si un pedido no cabe, se deja sin asignar
  (penalización por pedido) en lugar de hacer el problema irresoluble.

Ver docs/algoritmo_optimizacion.md para el detalle.
"""

from dataclasses import dataclass, field

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from app.services.geo import haversine_km

# Penalización por dejar un pedido sin servir (en metros). Muy superior a cualquier
# ruta real, para que el solver solo descarte pedidos cuando sea imprescindible.
DROP_PENALTY = 10_000_000
MAX_WAIT_MIN = 240

REASON_CAPACITY = "Supera la capacidad de todos los vehículos"
REASON_WINDOW = "Ventana horaria fuera del turno de reparto"
REASON_NO_ROOM = "Sin capacidad o tiempo disponible en la flota"


@dataclass(frozen=True)
class Location:
    lat: float
    lng: float


@dataclass(frozen=True)
class VehicleInput:
    id: int
    capacity_kg: float
    capacity_m3: float


@dataclass(frozen=True)
class OrderInput:
    id: int
    lat: float
    lng: float
    weight_kg: float
    volume_m3: float
    window_start: int  # minutos desde medianoche
    window_end: int
    service_minutes: int = 5


@dataclass
class StopResult:
    order_id: int
    sequence: int
    arrival_minute: int


@dataclass
class RouteResult:
    vehicle_id: int
    stops: list[StopResult]
    distance_km: float
    start_minute: int
    end_minute: int
    load_kg: float
    load_m3: float


@dataclass
class OptimizationResult:
    routes: list[RouteResult] = field(default_factory=list)
    unassigned: dict[int, str] = field(default_factory=dict)  # order_id -> motivo
    total_distance_km: float = 0.0
    baseline_distance_km: float = 0.0

    @property
    def savings_pct(self) -> float:
        if self.baseline_distance_km <= 0:
            return 0.0
        return round((1 - self.total_distance_km / self.baseline_distance_km) * 100, 1)


def _distance_matrix_m(points: list[Location], road_factor: float) -> list[list[int]]:
    return [
        [round(haversine_km(a.lat, a.lng, b.lat, b.lng) * road_factor * 1000) for b in points]
        for a in points
    ]


def baseline_distance_km(
    depot: Location,
    vehicles: list[VehicleInput],
    orders: list[OrderInput],
    road_factor: float = 1.3,
) -> float:
    """Distancia de referencia sin optimizar: pedidos en orden de alta, llenando
    vehículos uno tras otro hasta su capacidad (cómo se haría a mano)."""
    if not orders or not vehicles:
        return 0.0
    points = [depot] + [Location(o.lat, o.lng) for o in orders]
    dist = _distance_matrix_m(points, road_factor)

    total_m = 0
    v_idx, kg, m3, current = 0, 0.0, 0.0, 0
    for node, order in enumerate(orders, start=1):
        vehicle = vehicles[v_idx % len(vehicles)]
        if current != 0 and (
            kg + order.weight_kg > vehicle.capacity_kg or m3 + order.volume_m3 > vehicle.capacity_m3
        ):
            total_m += dist[current][0]  # vuelta al almacén y siguiente vehículo
            v_idx, kg, m3, current = v_idx + 1, 0.0, 0.0, 0
        total_m += dist[current][node]
        kg, m3, current = kg + order.weight_kg, m3 + order.volume_m3, node
    total_m += dist[current][0]
    return round(total_m / 1000, 2)


def optimize_routes(
    depot: Location,
    vehicles: list[VehicleInput],
    orders: list[OrderInput],
    *,
    shift_start: int = 8 * 60,
    shift_end: int = 20 * 60,
    speed_kmh: float = 30.0,
    road_factor: float = 1.3,
    time_limit_s: int = 3,
    balance_coefficient: int = 0,
) -> OptimizationResult:
    result = OptimizationResult()
    if not vehicles:
        result.unassigned = {o.id: REASON_NO_ROOM for o in orders}
        return result

    # 1) Descartar de antemano los pedidos imposibles, con un motivo claro
    max_kg = max(v.capacity_kg for v in vehicles)
    max_m3 = max(v.capacity_m3 for v in vehicles)
    feasible: list[OrderInput] = []
    for o in orders:
        if o.weight_kg > max_kg or o.volume_m3 > max_m3:
            result.unassigned[o.id] = REASON_CAPACITY
        elif max(o.window_start, shift_start) >= min(o.window_end, shift_end):
            result.unassigned[o.id] = REASON_WINDOW
        else:
            feasible.append(o)
    if not feasible:
        return result

    # 2) Modelo de OR-Tools. Nodo 0 = almacén; nodo i = feasible[i-1]
    points = [depot] + [Location(o.lat, o.lng) for o in feasible]
    dist_m = _distance_matrix_m(points, road_factor)
    meters_per_min = speed_kmh * 1000 / 60
    travel_min = [[round(d / meters_per_min) for d in row] for row in dist_m]
    service = [0] + [o.service_minutes for o in feasible]
    kg_demand = [0] + [round(o.weight_kg * 10) for o in feasible]  # décimas de kg
    m3_demand = [0] + [round(o.volume_m3 * 1000) for o in feasible]  # litros

    manager = pywrapcp.RoutingIndexManager(len(points), len(vehicles), 0)
    routing = pywrapcp.RoutingModel(manager)

    def node(index: int) -> int:
        return manager.IndexToNode(index)

    distance_cb = routing.RegisterTransitCallback(lambda i, j: dist_m[node(i)][node(j)])
    routing.SetArcCostEvaluatorOfAllVehicles(distance_cb)
    if balance_coefficient > 0:
        # Penaliza la ruta más larga para repartir el trabajo entre los conductores
        routing.AddDimension(distance_cb, 0, 10_000_000, True, "Distance")
        routing.GetDimensionOrDie("Distance").SetGlobalSpanCostCoefficient(balance_coefficient)

    weight_cb = routing.RegisterUnaryTransitCallback(lambda i: kg_demand[node(i)])
    routing.AddDimensionWithVehicleCapacity(
        weight_cb, 0, [round(v.capacity_kg * 10) for v in vehicles], True, "Weight"
    )
    volume_cb = routing.RegisterUnaryTransitCallback(lambda i: m3_demand[node(i)])
    routing.AddDimensionWithVehicleCapacity(
        volume_cb, 0, [round(v.capacity_m3 * 1000) for v in vehicles], True, "Volume"
    )

    time_cb = routing.RegisterTransitCallback(
        lambda i, j: service[node(i)] + travel_min[node(i)][node(j)]
    )
    routing.AddDimension(time_cb, MAX_WAIT_MIN, shift_end, False, "Time")
    time_dim = routing.GetDimensionOrDie("Time")

    for n, o in enumerate(feasible, start=1):
        index = manager.NodeToIndex(n)
        time_dim.CumulVar(index).SetRange(
            max(o.window_start, shift_start), min(o.window_end, shift_end)
        )
        routing.AddDisjunction([index], DROP_PENALTY)

    for v in range(len(vehicles)):
        start, end = routing.Start(v), routing.End(v)
        time_dim.CumulVar(start).SetRange(shift_start, shift_end)
        time_dim.CumulVar(end).SetRange(shift_start, shift_end)
        # Prioridad 1: terminar lo antes posible. Prioridad 2: con ese final, salir lo
        # más tarde posible para no esperar en la primera parada.
        routing.AddVariableMinimizedByFinalizer(time_dim.CumulVar(end))
        routing.AddVariableMaximizedByFinalizer(time_dim.CumulVar(start))

    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    params.time_limit.FromSeconds(time_limit_s)

    solution = routing.SolveWithParameters(params)
    if solution is None:
        result.unassigned.update({o.id: REASON_NO_ROOM for o in feasible})
        return result

    # 3) Extraer las rutas
    served: list[OrderInput] = []
    for v, vehicle in enumerate(vehicles):
        index = routing.Start(v)
        start_minute = solution.Min(time_dim.CumulVar(index))
        stops: list[StopResult] = []
        distance = 0
        kg = m3 = 0.0
        while not routing.IsEnd(index):
            next_index = solution.Value(routing.NextVar(index))
            distance += dist_m[node(index)][node(next_index)]
            index = next_index
            if not routing.IsEnd(index):
                order = feasible[node(index) - 1]
                stops.append(
                    StopResult(order.id, len(stops) + 1, solution.Min(time_dim.CumulVar(index)))
                )
                kg += order.weight_kg
                m3 += order.volume_m3
                served.append(order)
        if not stops:
            continue
        result.routes.append(
            RouteResult(
                vehicle_id=vehicle.id,
                stops=stops,
                distance_km=round(distance / 1000, 2),
                start_minute=start_minute,
                end_minute=solution.Min(time_dim.CumulVar(index)),
                load_kg=round(kg, 2),
                load_m3=round(m3, 3),
            )
        )

    served_ids = {o.id for o in served}
    for o in feasible:
        if o.id not in served_ids:
            result.unassigned[o.id] = REASON_NO_ROOM

    result.total_distance_km = round(sum(r.distance_km for r in result.routes), 2)
    # La referencia se calcula sobre los mismos pedidos servidos, en orden de alta
    served.sort(key=lambda o: o.id)
    result.baseline_distance_km = baseline_distance_km(depot, vehicles, served, road_factor)
    return result
