import enum
from datetime import date, datetime, time

from sqlalchemy import (
    JSON,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Time,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Role(enum.StrEnum):
    admin = "admin"
    dispatcher = "dispatcher"
    driver = "driver"


class OrderStatus(enum.StrEnum):
    pending = "pending"
    planned = "planned"
    delivered = "delivered"
    failed = "failed"


def _enum(cls: type[enum.Enum]) -> Enum:
    return Enum(cls, native_enum=False, length=20, values_callable=lambda e: [m.value for m in e])


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(_enum(Role))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(30))
    license_number: Mapped[str] = mapped_column(String(30), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped[User | None] = relationship()


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    plate: Mapped[str] = mapped_column(String(15), unique=True)
    model: Mapped[str] = mapped_column(String(80), default="")
    capacity_kg: Mapped[float] = mapped_column(Float)
    capacity_m3: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(default=True)
    driver_id: Mapped[int | None] = mapped_column(ForeignKey("drivers.id"))

    driver: Mapped[Driver | None] = relationship()


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(40), unique=True)
    customer_name: Mapped[str] = mapped_column(String(120))
    customer_phone: Mapped[str] = mapped_column(String(30), default="")
    address: Mapped[str] = mapped_column(String(255))
    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)
    delivery_date: Mapped[date] = mapped_column(Date, index=True)
    window_start: Mapped[time] = mapped_column(Time)
    window_end: Mapped[time] = mapped_column(Time)
    weight_kg: Mapped[float] = mapped_column(Float)
    volume_m3: Mapped[float] = mapped_column(Float)
    service_minutes: Mapped[int] = mapped_column(Integer, default=5)
    status: Mapped[OrderStatus] = mapped_column(_enum(OrderStatus), default=OrderStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RoutePlan(Base):
    """Resultado de una optimización para un día. Solo hay un plan vigente por fecha."""

    __tablename__ = "route_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan_date: Mapped[date] = mapped_column(Date, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    total_distance_km: Mapped[float] = mapped_column(Float, default=0)
    baseline_distance_km: Mapped[float] = mapped_column(Float, default=0)
    # Lista de {"order_id": int, "reason": str} con los pedidos que no se pudieron planificar
    unassigned: Mapped[list] = mapped_column(JSON, default=list)

    routes: Mapped[list["Route"]] = relationship(
        back_populates="plan", cascade="all, delete-orphan", order_by="Route.id"
    )


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("route_plans.id", ondelete="CASCADE"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    driver_id: Mapped[int | None] = mapped_column(ForeignKey("drivers.id"))
    distance_km: Mapped[float] = mapped_column(Float)
    duration_min: Mapped[int] = mapped_column(Integer)
    load_kg: Mapped[float] = mapped_column(Float)
    load_m3: Mapped[float] = mapped_column(Float)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)

    plan: Mapped[RoutePlan] = relationship(back_populates="routes")
    vehicle: Mapped[Vehicle] = relationship()
    driver: Mapped[Driver | None] = relationship()
    stops: Mapped[list["RouteStop"]] = relationship(
        back_populates="route", cascade="all, delete-orphan", order_by="RouteStop.sequence"
    )


class RouteStop(Base):
    __tablename__ = "route_stops"

    id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id", ondelete="CASCADE"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    sequence: Mapped[int] = mapped_column(Integer)
    eta: Mapped[time] = mapped_column(Time)

    route: Mapped[Route] = relationship(back_populates="stops")
    order: Mapped[Order] = relationship()
