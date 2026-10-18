import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base, get_db, make_engine
from app.main import app
from app.models import Driver, Role, User
from app.security import hash_password

PASSWORDS = {Role.admin: "Admin1234", Role.dispatcher: "Despacho1234", Role.driver: "Conductor1234"}


@pytest.fixture(autouse=True)
def _test_settings(monkeypatch):
    monkeypatch.setattr(settings, "geocoder", "none")
    monkeypatch.setattr(settings, "optimizer_time_limit_s", 1)
    monkeypatch.setattr(settings, "bcrypt_rounds", 4)


@pytest.fixture
def db_session():
    engine = make_engine("sqlite://")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = session_factory()
    app.dependency_overrides[get_db] = lambda: session
    yield session
    session.close()
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def client(db_session):
    return TestClient(app)


@pytest.fixture
def users(db_session):
    created = {}
    for role in Role:
        user = User(
            email=f"{role.value}@test.dev",
            full_name=f"Usuario {role.value}",
            hashed_password=hash_password(PASSWORDS[role]),
            role=role,
        )
        db_session.add(user)
        created[role] = user
    db_session.flush()
    db_session.add(
        Driver(
            full_name="Conductor Test",
            phone="600000000",
            license_number="LIC-T1",
            user_id=created[Role.driver].id,
        )
    )
    db_session.commit()
    return created


def _token(client: TestClient, role: Role) -> dict[str, str]:
    response = client.post(
        "/api/auth/login", data={"username": f"{role.value}@test.dev", "password": PASSWORDS[role]}
    )
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def admin_headers(client, users):
    return _token(client, Role.admin)


@pytest.fixture
def dispatcher_headers(client, users):
    return _token(client, Role.dispatcher)


@pytest.fixture
def driver_headers(client, users):
    return _token(client, Role.driver)
