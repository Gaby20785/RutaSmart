from app.services.geo import GeocodingError


def order_payload(**overrides):
    payload = {
        "reference": "PED-001",
        "customer_name": "Cliente Uno",
        "address": "Calle Mayor 1, Madrid",
        "lat": 40.4168,
        "lng": -3.7038,
        "delivery_date": "2026-10-19",
        "window_start": "09:00",
        "window_end": "13:00",
        "weight_kg": 12.5,
        "volume_m3": 0.1,
    }
    payload.update(overrides)
    return payload


def test_create_order_with_coordinates(client, dispatcher_headers):
    response = client.post("/api/orders", json=order_payload(), headers=dispatcher_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    assert body["service_minutes"] == 5


def test_invalid_time_window_rejected(client, dispatcher_headers):
    response = client.post(
        "/api/orders",
        json=order_payload(window_start="14:00", window_end="10:00"),
        headers=dispatcher_headers,
    )
    assert response.status_code == 422


def test_negative_weight_rejected(client, dispatcher_headers):
    response = client.post(
        "/api/orders", json=order_payload(weight_kg=-1), headers=dispatcher_headers
    )
    assert response.status_code == 422


def test_duplicate_reference_rejected(client, dispatcher_headers):
    client.post("/api/orders", json=order_payload(), headers=dispatcher_headers)
    response = client.post("/api/orders", json=order_payload(), headers=dispatcher_headers)
    assert response.status_code == 409


def test_order_without_coordinates_is_geocoded(client, dispatcher_headers, monkeypatch):
    monkeypatch.setattr("app.routers.orders.geocode", lambda address: (40.5, -3.6))
    response = client.post(
        "/api/orders", json=order_payload(lat=None, lng=None), headers=dispatcher_headers
    )
    assert response.status_code == 201
    assert (response.json()["lat"], response.json()["lng"]) == (40.5, -3.6)


def test_geocoding_failure_returns_422(client, dispatcher_headers, monkeypatch):
    def fail(address):
        raise GeocodingError("Dirección no encontrada")

    monkeypatch.setattr("app.routers.orders.geocode", fail)
    response = client.post(
        "/api/orders", json=order_payload(lat=None, lng=None), headers=dispatcher_headers
    )
    assert response.status_code == 422
    assert "no encontrada" in response.json()["detail"]


def test_list_orders_filtered_by_date(client, dispatcher_headers):
    client.post("/api/orders", json=order_payload(), headers=dispatcher_headers)
    client.post(
        "/api/orders",
        json=order_payload(reference="PED-002", delivery_date="2026-10-20"),
        headers=dispatcher_headers,
    )
    response = client.get("/api/orders?delivery_date=2026-10-19", headers=dispatcher_headers)
    assert [o["reference"] for o in response.json()] == ["PED-001"]


def test_delete_pending_order(client, dispatcher_headers):
    order_id = client.post("/api/orders", json=order_payload(), headers=dispatcher_headers).json()[
        "id"
    ]
    assert client.delete(f"/api/orders/{order_id}", headers=dispatcher_headers).status_code == 204


def test_import_csv_reports_errors_without_blocking(client, dispatcher_headers):
    csv_content = (
        "reference;customer_name;address;lat;lng;delivery_date;window_start;window_end;"
        "weight_kg;volume_m3\n"
        "C-1;Ana Ruiz;Calle Sol 3, Madrid;40,41;-3,70;2026-10-19;09:00;12:00;10,5;0,2\n"
        "C-2;Luis Paz;Calle Luna 5, Madrid;40.42;-3.71;2026-10-19;15:00;11:00;8;0.1\n"
        "C-3;Eva Rey;Calle Mar 7, Madrid;40.43;-3.69;2026-10-19;10:00;14:00;5;0.05\n"
        "C-1;Repetido;Calle Sol 3, Madrid;40.41;-3.70;2026-10-19;09:00;12:00;3;0.1\n"
        "C-5;Sin coords;Calle Río 9, Madrid;;;2026-10-19;09:00;12:00;3;0.1\n"
    )
    response = client.post(
        "/api/orders/import",
        files={"file": ("pedidos.csv", csv_content.encode("utf-8"), "text/csv")},
        headers=dispatcher_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["created"] == 2
    errors = {e["row"]: e["error"] for e in body["errors"]}
    assert set(errors) == {3, 5, 6}
    assert "posterior" in errors[3]
    assert "duplicada" in errors[5]
    assert "desactivada" in errors[6]  # geocoder desactivado en tests


def test_import_csv_missing_columns(client, dispatcher_headers):
    response = client.post(
        "/api/orders/import",
        files={"file": ("p.csv", b"reference,address\nX,Calle 1", "text/csv")},
        headers=dispatcher_headers,
    )
    assert response.status_code == 422
    assert "Faltan columnas" in response.json()["detail"]
