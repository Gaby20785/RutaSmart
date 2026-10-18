from datetime import date, time

import pytest

from app.models import Driver, Order, OrderStatus, RoutePlan, Vehicle

PLAN_DATE = date(2026, 10, 19)


@pytest.fixture
def fleet_and_orders(db_session, users):
    driver = db_session.query(Driver).filter_by(license_number="LIC-T1").one()
    db_session.add_all(
        [
            Vehicle(plate="1111AAA", capacity_kg=300, capacity_m3=3, driver_id=driver.id),
            Vehicle(plate="2222BBB", capacity_kg=300, capacity_m3=3),
        ]
    )
    for i in range(10):
        db_session.add(
            Order(
                reference=f"R-{i}",
                customer_name="Cliente",
                address=f"Calle {i}, Madrid",
                lat=40.38 + i * 0.008,
                lng=-3.74 + (i % 4) * 0.02,
                delivery_date=PLAN_DATE,
                window_start=time(9, 0),
                window_end=time(19, 0),
                weight_kg=20,
                volume_m3=0.1,
            )
        )
    db_session.add(
        Order(
            reference="HEAVY",
            customer_name="Cliente",
            address="Calle X, Madrid",
            lat=40.4,
            lng=-3.7,
            delivery_date=PLAN_DATE,
            window_start=time(9, 0),
            window_end=time(19, 0),
            weight_kg=900,
            volume_m3=0.1,
        )
    )
    db_session.commit()


def optimize(client, headers):
    return client.post("/api/routes/optimize", json={"plan_date": str(PLAN_DATE)}, headers=headers)


def test_optimize_creates_plan_and_updates_status(
    client, dispatcher_headers, fleet_and_orders, db_session
):
    response = optimize(client, dispatcher_headers)
    assert response.status_code == 201, response.text
    plan = response.json()
    assert plan["orders_planned"] == 10
    assert plan["total_distance_km"] > 0
    assert [u["order"]["reference"] for u in plan["unassigned"]] == ["HEAVY"]
    for route in plan["routes"]:
        assert route["load_kg"] <= route["vehicle"]["capacity_kg"]
        assert route["stops"][0]["sequence"] == 1

    statuses = {o.reference: o.status for o in db_session.query(Order)}
    assert statuses["HEAVY"] == OrderStatus.pending
    assert statuses["R-0"] == OrderStatus.planned


def test_get_plan_by_date(client, dispatcher_headers, fleet_and_orders):
    plan_id = optimize(client, dispatcher_headers).json()["id"]
    response = client.get(f"/api/routes/plans?plan_date={PLAN_DATE}", headers=dispatcher_headers)
    assert response.json()["id"] == plan_id


def test_reoptimizing_replaces_previous_plan(
    client, dispatcher_headers, fleet_and_orders, db_session
):
    optimize(client, dispatcher_headers)
    second = optimize(client, dispatcher_headers).json()
    assert db_session.query(RoutePlan).filter_by(plan_date=PLAN_DATE).count() == 1
    current = client.get(f"/api/routes/plans?plan_date={PLAN_DATE}", headers=dispatcher_headers)
    assert current.json()["id"] == second["id"]
    assert current.json()["orders_planned"] == 10


def test_optimize_without_orders_returns_400(client, dispatcher_headers, users):
    response = client.post(
        "/api/routes/optimize", json={"plan_date": "2030-01-01"}, headers=dispatcher_headers
    )
    assert response.status_code == 400


def test_plan_not_found(client, dispatcher_headers, users):
    response = client.get("/api/routes/plans?plan_date=2030-01-01", headers=dispatcher_headers)
    assert response.status_code == 404


def test_driver_cannot_optimize(client, driver_headers, fleet_and_orders):
    assert optimize(client, driver_headers).status_code == 403


def test_driver_sees_only_own_routes(client, dispatcher_headers, driver_headers, fleet_and_orders):
    optimize(client, dispatcher_headers)
    response = client.get(f"/api/routes/mine?plan_date={PLAN_DATE}", headers=driver_headers)
    assert response.status_code == 200
    for route in response.json():
        assert route["vehicle"]["plate"] == "1111AAA"
