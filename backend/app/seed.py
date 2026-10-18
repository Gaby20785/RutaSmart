"""Carga datos de demostración (sintéticos).

Uso:
    python -m app.seed                    # pedidos para hoy
    python -m app.seed --date 2026-10-19  # pedidos para una fecha
    python -m app.seed --reset            # borra la base de datos antes de cargar
    python -m app.seed --csv sample_data/pedidos_ejemplo.csv --date 2026-10-20
                                          # solo genera un CSV de ejemplo para importar
"""

import argparse
import csv
import random
from datetime import date, time
from pathlib import Path

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Driver, Order, Role, User, Vehicle
from app.security import hash_password

# Centro aproximado de distritos de Madrid. Las direcciones son ficticias.
DISTRICTS = [
    ("Centro", 40.4155, -3.7074),
    ("Arganzuela", 40.3980, -3.6990),
    ("Retiro", 40.4110, -3.6760),
    ("Salamanca", 40.4300, -3.6770),
    ("Chamartín", 40.4580, -3.6770),
    ("Tetuán", 40.4600, -3.6980),
    ("Chamberí", 40.4340, -3.7040),
    ("Moncloa", 40.4350, -3.7290),
    ("Latina", 40.4030, -3.7360),
    ("Carabanchel", 40.3830, -3.7280),
    ("Usera", 40.3830, -3.7070),
    ("Puente de Vallecas", 40.3920, -3.6680),
    ("Moratalaz", 40.4070, -3.6440),
    ("Ciudad Lineal", 40.4380, -3.6560),
    ("Villaverde", 40.3460, -3.7000),
]
STREETS = [
    "Calle del Olivo",
    "Calle de la Estación",
    "Avenida del Parque",
    "Calle Real",
    "Calle de los Almendros",
    "Paseo de la Ribera",
    "Calle del Sol",
    "Calle Nueva",
    "Calle de la Fuente",
    "Avenida de la Constitución",
    "Calle del Pinar",
    "Calle Mayor",
]
FIRST_NAMES = [
    "Lucía",
    "Hugo",
    "Martina",
    "Mateo",
    "Sofía",
    "Leo",
    "Paula",
    "Daniel",
    "Valeria",
    "Pablo",
    "Julia",
    "Álvaro",
    "Carmen",
    "Diego",
    "Elena",
    "Adrián",
]
LAST_NAMES = [
    "García",
    "Martínez",
    "López",
    "Sánchez",
    "Pérez",
    "Gómez",
    "Fernández",
    "Ruiz",
    "Díaz",
    "Moreno",
    "Álvarez",
    "Romero",
    "Navarro",
    "Torres",
]
WINDOWS = [
    (time(9, 0), time(13, 0)),
    (time(9, 0), time(19, 0)),
    (time(10, 0), time(12, 0)),
    (time(12, 0), time(16, 0)),
    (time(15, 0), time(19, 0)),
    (time(16, 0), time(18, 0)),
]

USERS = [
    ("admin@rutasmart.dev", "Administración RutaSmart", "Admin1234", Role.admin),
    ("despacho@rutasmart.dev", "Despacho Central", "Despacho1234", Role.dispatcher),
]
DRIVERS = [
    ("Carlos Ortega", "600111222", "LIC-1001", "conductor1@rutasmart.dev"),
    ("Ana Beltrán", "600333444", "LIC-1002", "conductor2@rutasmart.dev"),
    ("Javier Molina", "600555666", "LIC-1003", None),
    ("Marta Vidal", "600777888", "LIC-1004", None),
]
# Se asignan en orden a DRIVERS: los conductores con cuenta llevan los vehículos grandes,
# que el optimizador siempre utiliza, para que la vista del conductor tenga datos en la demo.
VEHICLES = [
    ("3456GFD", "Mercedes Sprinter", 1300, 10.5),
    ("5678KJH", "Ford Transit Custom", 1000, 6.0),
    ("9012HGF", "Citroën Berlingo", 700, 4.4),
    ("1234LMN", "Renault Kangoo E-Tech", 650, 3.9),
]
DRIVER_PASSWORD = "Conductor1234"


def synthetic_orders(delivery_date: date, count: int, seed: int, prefix: str) -> list[dict]:
    rng = random.Random(seed)
    orders = []
    for i in range(1, count + 1):
        district, lat, lng = rng.choice(DISTRICTS)
        start, end = rng.choice(WINDOWS)
        orders.append(
            {
                "reference": f"{prefix}-{delivery_date:%m%d}-{i:03d}",
                "customer_name": f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}",
                "customer_phone": f"6{rng.randint(10_000_000, 99_999_999)}",
                "address": f"{rng.choice(STREETS)} {rng.randint(1, 180)}, {district}, Madrid",
                "lat": round(lat + rng.uniform(-0.009, 0.009), 6),
                "lng": round(lng + rng.uniform(-0.011, 0.011), 6),
                "delivery_date": delivery_date,
                "window_start": start,
                "window_end": end,
                "weight_kg": round(rng.uniform(1, 45), 1),
                "volume_m3": round(rng.uniform(0.01, 0.35), 3),
                "service_minutes": rng.choice([3, 5, 5, 8]),
            }
        )
    return orders


def write_csv(path: Path, delivery_date: date, count: int = 25) -> None:
    rows = synthetic_orders(delivery_date, count, seed=99, prefix="CSV")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row["window_start"] = row["window_start"].strftime("%H:%M")
            row["window_end"] = row["window_end"].strftime("%H:%M")
            writer.writerow(row)
    print(f"CSV de ejemplo generado: {path} ({count} pedidos para {delivery_date})")


def seed(delivery_date: date, order_count: int, reset: bool) -> None:
    if reset:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with SessionLocal() as db:
        for email, name, password, role in USERS:
            if db.scalar(select(User).where(User.email == email)) is None:
                db.add(
                    User(
                        email=email,
                        full_name=name,
                        hashed_password=hash_password(password),
                        role=role,
                    )
                )

        drivers = []
        for name, phone, license_number, email in DRIVERS:
            driver = db.scalar(select(Driver).where(Driver.license_number == license_number))
            if driver is None:
                driver = Driver(full_name=name, phone=phone, license_number=license_number)
                if email:
                    driver.user = User(
                        email=email,
                        full_name=name,
                        role=Role.driver,
                        hashed_password=hash_password(DRIVER_PASSWORD),
                    )
                db.add(driver)
            drivers.append(driver)
        db.flush()

        for (plate, model, kg, m3), driver in zip(VEHICLES, drivers, strict=True):
            if db.scalar(select(Vehicle).where(Vehicle.plate == plate)) is None:
                db.add(
                    Vehicle(
                        plate=plate,
                        model=model,
                        capacity_kg=kg,
                        capacity_m3=m3,
                        driver_id=driver.id,
                    )
                )

        existing = set(db.scalars(select(Order.reference)).all())
        new_orders = [
            Order(**o)
            for o in synthetic_orders(delivery_date, order_count, seed=42, prefix="PED")
            if o["reference"] not in existing
        ]
        db.add_all(new_orders)
        db.commit()

    print(
        f"Datos de demo cargados: {len(USERS)} usuarios, {len(DRIVERS)} conductores, "
        f"{len(VEHICLES)} vehículos, {len(new_orders)} pedidos nuevos para {delivery_date}"
    )
    print(
        "Usuarios: admin@rutasmart.dev / Admin1234 · despacho@rutasmart.dev / Despacho1234 · "
        f"conductor1@rutasmart.dev / {DRIVER_PASSWORD}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga datos de demostración de RutaSmart")
    parser.add_argument("--date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--orders", type=int, default=40)
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--csv", type=Path, help="Solo genera un CSV de pedidos de ejemplo")
    args = parser.parse_args()
    if args.csv:
        write_csv(args.csv, args.date)
    else:
        seed(args.date, args.orders, args.reset)


if __name__ == "__main__":
    main()
