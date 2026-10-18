def test_health(client):
    assert client.get("/api/health").json()["status"] == "ok"


def test_login_ok_returns_token_and_user(client, users):
    response = client.post(
        "/api/auth/login", data={"username": "ADMIN@test.dev", "password": "Admin1234"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["user"]["role"] == "admin"


def test_login_wrong_password(client, users):
    response = client.post(
        "/api/auth/login", data={"username": "admin@test.dev", "password": "incorrecta"}
    )
    assert response.status_code == 401


def test_me_requires_token(client):
    assert client.get("/api/auth/me").status_code == 401


def test_invalid_token_rejected(client):
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer no-es-un-jwt"})
    assert response.status_code == 401


def test_me_returns_current_user(client, dispatcher_headers):
    response = client.get("/api/auth/me", headers=dispatcher_headers)
    assert response.json()["email"] == "dispatcher@test.dev"


def test_password_is_hashed(db_session, users):
    from app.models import Role

    assert users[Role.admin].hashed_password.startswith("$2")


def test_driver_cannot_access_admin_endpoints(client, driver_headers):
    response = client.post(
        "/api/vehicles",
        json={"plate": "0000AAA", "capacity_kg": 100, "capacity_m3": 1},
        headers=driver_headers,
    )
    assert response.status_code == 403
    assert client.get("/api/orders", headers=driver_headers).status_code == 403


def test_admin_creates_user_and_rejects_duplicate(client, admin_headers):
    payload = {
        "email": "nuevo@test.dev",
        "full_name": "Nuevo Despachador",
        "password": "Password123",
        "role": "dispatcher",
    }
    assert client.post("/api/users", json=payload, headers=admin_headers).status_code == 201
    assert client.post("/api/users", json=payload, headers=admin_headers).status_code == 409


def test_dispatcher_cannot_create_users(client, dispatcher_headers):
    payload = {"email": "x@test.dev", "full_name": "X", "password": "Password123", "role": "admin"}
    assert client.post("/api/users", json=payload, headers=dispatcher_headers).status_code == 403
