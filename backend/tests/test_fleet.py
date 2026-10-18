def create_driver(client, headers, **overrides):
    payload = {"full_name": "Laura Gil", "phone": "611222333", "license_number": "LIC-200"}
    payload.update(overrides)
    return client.post("/api/drivers", json=payload, headers=headers)


def test_create_and_list_drivers(client, admin_headers, dispatcher_headers):
    assert create_driver(client, admin_headers).status_code == 201
    names = [d["full_name"] for d in client.get("/api/drivers", headers=dispatcher_headers).json()]
    assert "Laura Gil" in names


def test_duplicate_license_rejected(client, admin_headers):
    create_driver(client, admin_headers)
    assert create_driver(client, admin_headers, full_name="Otra").status_code == 409


def test_driver_with_account_can_login(client, admin_headers):
    response = create_driver(client, admin_headers, email="laura@test.dev", password="Conductor99")
    assert response.status_code == 201
    assert response.json()["user_id"] is not None
    login = client.post(
        "/api/auth/login", data={"username": "laura@test.dev", "password": "Conductor99"}
    )
    assert login.json()["user"]["role"] == "driver"


def test_driver_account_requires_email_and_password(client, admin_headers):
    assert create_driver(client, admin_headers, email="solo@test.dev").status_code == 422


def test_dispatcher_cannot_create_driver(client, dispatcher_headers):
    assert create_driver(client, dispatcher_headers).status_code == 403


def test_deactivated_driver_hidden_from_list(client, admin_headers):
    driver_id = create_driver(client, admin_headers).json()["id"]
    assert client.delete(f"/api/drivers/{driver_id}", headers=admin_headers).status_code == 204
    ids = [d["id"] for d in client.get("/api/drivers", headers=admin_headers).json()]
    assert driver_id not in ids
    all_ids = [
        d["id"]
        for d in client.get("/api/drivers?include_inactive=true", headers=admin_headers).json()
    ]
    assert driver_id in all_ids


def test_create_vehicle_normalizes_plate_and_assigns_driver(client, admin_headers):
    driver_id = create_driver(client, admin_headers).json()["id"]
    response = client.post(
        "/api/vehicles",
        json={
            "plate": "1234-abc",
            "model": "Kangoo",
            "capacity_kg": 600,
            "capacity_m3": 4,
            "driver_id": driver_id,
        },
        headers=admin_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["plate"] == "1234ABC"
    assert body["driver"]["full_name"] == "Laura Gil"


def test_vehicle_capacity_must_be_positive(client, admin_headers):
    response = client.post(
        "/api/vehicles",
        json={"plate": "1111BBB", "capacity_kg": 0, "capacity_m3": 4},
        headers=admin_headers,
    )
    assert response.status_code == 422


def test_duplicate_plate_rejected(client, admin_headers):
    payload = {"plate": "2222CCC", "capacity_kg": 500, "capacity_m3": 3}
    assert client.post("/api/vehicles", json=payload, headers=admin_headers).status_code == 201
    assert client.post("/api/vehicles", json=payload, headers=admin_headers).status_code == 409


def test_vehicle_with_unknown_driver_rejected(client, admin_headers):
    response = client.post(
        "/api/vehicles",
        json={"plate": "3333DDD", "capacity_kg": 500, "capacity_m3": 3, "driver_id": 999},
        headers=admin_headers,
    )
    assert response.status_code == 422


def test_update_vehicle(client, admin_headers):
    vehicle_id = client.post(
        "/api/vehicles",
        json={"plate": "4444EEE", "capacity_kg": 500, "capacity_m3": 3},
        headers=admin_headers,
    ).json()["id"]
    response = client.put(
        f"/api/vehicles/{vehicle_id}", json={"capacity_kg": 750}, headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["capacity_kg"] == 750
