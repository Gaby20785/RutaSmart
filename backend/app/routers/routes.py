from datetime import date, time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import require_roles, staff
from app.models import Driver, Order, OrderStatus, Role, Route, RoutePlan, RouteStop, User, Vehicle
from app.schemas import OptimizeRequest, OrderOut, RouteOut, RoutePlanOut, UnassignedOut
from app.services.optimizer import Location, OrderInput, VehicleInput, optimize_routes

router = APIRouter(prefix="/api/routes", tags=["Rutas"])


def _to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute


def _to_time(minutes: int) -> time:
    minutes = max(0, min(minutes, 23 * 60 + 59))
    return time(minutes // 60, minutes % 60)


def _plan_out(db: Session, plan: RoutePlan) -> RoutePlanOut:
    unassigned_ids = [u["order_id"] for u in plan.unassigned]
    orders = {o.id: o for o in db.scalars(select(Order).where(Order.id.in_(unassigned_ids)))}
    unassigned = [
        UnassignedOut(order=OrderOut.model_validate(orders[u["order_id"]]), reason=u["reason"])
        for u in plan.unassigned
        if u["order_id"] in orders
    ]
    savings = 0.0
    if plan.baseline_distance_km > 0:
        savings = round((1 - plan.total_distance_km / plan.baseline_distance_km) * 100, 1)
    return RoutePlanOut(
        id=plan.id,
        plan_date=plan.plan_date,
        created_at=plan.created_at,
        total_distance_km=plan.total_distance_km,
        baseline_distance_km=plan.baseline_distance_km,
        savings_pct=savings,
        orders_planned=sum(len(r.stops) for r in plan.routes),
        vehicles_used=len(plan.routes),
        routes=[RouteOut.model_validate(r) for r in plan.routes],
        unassigned=unassigned,
    )


@router.post("/optimize", response_model=RoutePlanOut, status_code=status.HTTP_201_CREATED)
def optimize(req: OptimizeRequest, db: Session = Depends(get_db), user: User = Depends(staff)):
    """Genera las rutas óptimas del día con los pedidos pendientes o ya planificados.
    Sustituye el plan anterior de esa fecha, si existía."""
    orders = db.scalars(
        select(Order)
        .where(Order.delivery_date == req.plan_date)
        .where(Order.status.in_([OrderStatus.pending, OrderStatus.planned]))
        .order_by(Order.id)
    ).all()
    if not orders:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "No hay pedidos para planificar en esa fecha"
        )

    vehicle_query = select(Vehicle).where(Vehicle.is_active).order_by(Vehicle.id)
    if req.vehicle_ids:
        vehicle_query = vehicle_query.where(Vehicle.id.in_(req.vehicle_ids))
    vehicles = db.scalars(vehicle_query).all()
    if not vehicles:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No hay vehículos activos disponibles")

    result = optimize_routes(
        Location(settings.depot_lat, settings.depot_lng),
        [VehicleInput(v.id, v.capacity_kg, v.capacity_m3) for v in vehicles],
        [
            OrderInput(
                id=o.id,
                lat=o.lat,
                lng=o.lng,
                weight_kg=o.weight_kg,
                volume_m3=o.volume_m3,
                window_start=_to_minutes(o.window_start),
                window_end=_to_minutes(o.window_end),
                service_minutes=o.service_minutes,
            )
            for o in orders
        ],
        shift_start=_to_minutes(settings.shift_start),
        shift_end=_to_minutes(settings.shift_end),
        speed_kmh=settings.avg_speed_kmh,
        road_factor=settings.road_factor,
        time_limit_s=settings.optimizer_time_limit_s,
        balance_coefficient=settings.balance_coefficient if req.balance_workload else 0,
    )

    for old in db.scalars(select(RoutePlan).where(RoutePlan.plan_date == req.plan_date)):
        db.delete(old)
    db.flush()

    vehicles_by_id = {v.id: v for v in vehicles}
    plan = RoutePlan(
        plan_date=req.plan_date,
        created_by_id=user.id,
        total_distance_km=result.total_distance_km,
        baseline_distance_km=result.baseline_distance_km,
        unassigned=[
            {"order_id": oid, "reason": reason} for oid, reason in result.unassigned.items()
        ],
    )
    for r in result.routes:
        plan.routes.append(
            Route(
                vehicle_id=r.vehicle_id,
                driver_id=vehicles_by_id[r.vehicle_id].driver_id,
                distance_km=r.distance_km,
                duration_min=r.end_minute - r.start_minute,
                load_kg=r.load_kg,
                load_m3=r.load_m3,
                start_time=_to_time(r.start_minute),
                end_time=_to_time(r.end_minute),
                stops=[
                    RouteStop(
                        order_id=s.order_id, sequence=s.sequence, eta=_to_time(s.arrival_minute)
                    )
                    for s in r.stops
                ],
            )
        )
    for o in orders:
        o.status = OrderStatus.pending if o.id in result.unassigned else OrderStatus.planned

    db.add(plan)
    db.commit()
    db.refresh(plan)
    return _plan_out(db, plan)


@router.get("/plans", response_model=RoutePlanOut)
def get_plan(plan_date: date, db: Session = Depends(get_db), _: User = Depends(staff)):
    plan = db.scalar(select(RoutePlan).where(RoutePlan.plan_date == plan_date))
    if plan is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No hay rutas planificadas para esa fecha")
    return _plan_out(db, plan)


@router.get("/mine", response_model=list[RouteOut])
def my_routes(
    plan_date: date,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(Role.driver)),
):
    """Rutas asignadas al conductor autenticado (base de la app del repartidor, Sprint 2)."""
    return db.scalars(
        select(Route)
        .join(RoutePlan)
        .join(Driver, Route.driver_id == Driver.id)
        .where(RoutePlan.plan_date == plan_date, Driver.user_id == user.id)
    ).all()
