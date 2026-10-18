"""Tests unitarios del motor de optimización con datos sintéticos (RF3, RF19)."""

import random

from app.services.optimizer import (
    REASON_CAPACITY,
    REASON_WINDOW,
    Location,
    OrderInput,
    VehicleInput,
    baseline_distance_km,
    optimize_routes,
)

DEPOT = Location(40.3720, -3.6950)


def synthetic_orders(n: int, seed: int = 1, window=(9 * 60, 19 * 60), kg=(1, 30)):
    rng = random.Random(seed)
    return [
        OrderInput(
            id=i,
            lat=40.38 + rng.uniform(0, 0.09),
            lng=-3.75 + rng.uniform(0, 0.12),
            weight_kg=round(rng.uniform(*kg), 1),
            volume_m3=0.1,
            window_start=window[0],
            window_end=window[1],
        )
        for i in range(1, n + 1)
    ]


def test_all_orders_served_when_capacity_is_enough():
    orders = synthetic_orders(20)
    vehicles = [VehicleInput(1, 1000, 10), VehicleInput(2, 1000, 10)]
    result = optimize_routes(DEPOT, vehicles, orders, time_limit_s=1)
    served = sorted(s.order_id for r in result.routes for s in r.stops)
    assert served == [o.id for o in orders]
    assert result.unassigned == {}


def test_vehicle_capacity_is_respected():
    orders = synthetic_orders(12, kg=(40, 50))
    vehicles = [VehicleInput(1, 200, 10), VehicleInput(2, 200, 10), VehicleInput(3, 200, 10)]
    result = optimize_routes(DEPOT, vehicles, orders, time_limit_s=1)
    weights = {o.id: o.weight_kg for o in orders}
    for route in result.routes:
        assert sum(weights[s.order_id] for s in route.stops) <= 200
    assert len(result.routes) == 3


def test_time_windows_are_respected():
    rng = random.Random(7)
    orders = [
        OrderInput(
            i,
            40.38 + rng.uniform(0, 0.08),
            -3.74 + rng.uniform(0, 0.1),
            5,
            0.05,
            *(rng.choice([(9 * 60, 11 * 60), (12 * 60, 14 * 60), (16 * 60, 18 * 60)])),
        )
        for i in range(1, 16)
    ]
    result = optimize_routes(
        DEPOT, [VehicleInput(1, 500, 5), VehicleInput(2, 500, 5)], orders, time_limit_s=1
    )
    windows = {o.id: (o.window_start, o.window_end) for o in orders}
    for route in result.routes:
        previous = route.start_minute
        for stop in route.stops:
            start, end = windows[stop.order_id]
            assert start <= stop.arrival_minute <= end
            assert stop.arrival_minute >= previous
            previous = stop.arrival_minute


def test_order_heavier_than_any_vehicle_is_unassigned():
    orders = synthetic_orders(3) + [OrderInput(99, 40.4, -3.7, 5000, 0.1, 540, 1140)]
    result = optimize_routes(DEPOT, [VehicleInput(1, 800, 5)], orders, time_limit_s=1)
    assert result.unassigned == {99: REASON_CAPACITY}


def test_window_outside_shift_is_unassigned():
    orders = [OrderInput(1, 40.4, -3.7, 5, 0.1, 21 * 60, 22 * 60)]
    result = optimize_routes(DEPOT, [VehicleInput(1, 800, 5)], orders, time_limit_s=1)
    assert result.unassigned == {1: REASON_WINDOW}
    assert result.routes == []


def test_no_vehicles_leaves_everything_unassigned():
    result = optimize_routes(DEPOT, [], synthetic_orders(3), time_limit_s=1)
    assert set(result.unassigned) == {1, 2, 3}


def test_optimization_beats_sequential_baseline_by_15_percent():
    """Objetivo O2 del Project Charter: ≥ 15 % menos km que la asignación manual."""
    orders = synthetic_orders(40, seed=3)
    vehicles = [VehicleInput(i, 400, 5) for i in range(1, 5)]
    result = optimize_routes(DEPOT, vehicles, orders, time_limit_s=2)
    assert result.unassigned == {}
    assert result.baseline_distance_km == baseline_distance_km(DEPOT, vehicles, orders)
    assert result.savings_pct >= 15


def test_balancing_shortens_the_longest_route():
    orders = synthetic_orders(30, seed=5)
    vehicles = [VehicleInput(i, 1000, 10) for i in range(1, 4)]
    plain = optimize_routes(DEPOT, vehicles, orders, time_limit_s=1)
    balanced = optimize_routes(DEPOT, vehicles, orders, time_limit_s=1, balance_coefficient=10)
    longest = lambda result: max(r.distance_km for r in result.routes)  # noqa: E731
    assert len(balanced.routes) >= len(plain.routes)
    assert longest(balanced) <= longest(plain)
    assert balanced.unassigned == {}


def test_route_distance_and_load_are_reported():
    orders = synthetic_orders(5)
    result = optimize_routes(DEPOT, [VehicleInput(1, 500, 5)], orders, time_limit_s=1)
    route = result.routes[0]
    assert route.distance_km > 0
    assert route.load_kg == round(sum(o.weight_kg for o in orders), 2)
    assert route.end_minute > route.start_minute
    assert [s.sequence for s in route.stops] == [1, 2, 3, 4, 5]
