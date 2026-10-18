from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import admin_only, staff
from app.models import Driver, User, Vehicle
from app.schemas import VehicleCreate, VehicleOut, VehicleUpdate

router = APIRouter(prefix="/api/vehicles", tags=["Vehículos"])


def _get_or_404(db: Session, vehicle_id: int) -> Vehicle:
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Vehículo no encontrado")
    return vehicle


def _check_driver(db: Session, driver_id: int | None) -> None:
    if driver_id is None:
        return
    driver = db.get(Driver, driver_id)
    if driver is None or not driver.is_active:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Conductor no válido")


def _commit(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Ya existe un vehículo con esa matrícula"
        ) from None


@router.get("", response_model=list[VehicleOut])
def list_vehicles(
    include_inactive: bool = False, db: Session = Depends(get_db), _: User = Depends(staff)
):
    query = select(Vehicle).order_by(Vehicle.plate)
    if not include_inactive:
        query = query.where(Vehicle.is_active)
    return db.scalars(query).all()


@router.post("", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    data: VehicleCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)
):
    _check_driver(db, data.driver_id)
    vehicle = Vehicle(**data.model_dump())
    db.add(vehicle)
    _commit(db)
    db.refresh(vehicle)
    return vehicle


@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(
    vehicle_id: int,
    data: VehicleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
):
    vehicle = _get_or_404(db, vehicle_id)
    changes = data.model_dump(exclude_unset=True)
    if "driver_id" in changes:
        _check_driver(db, changes["driver_id"])
    for key, value in changes.items():
        setattr(vehicle, key, value)
    _commit(db)
    db.refresh(vehicle)
    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_vehicle(
    vehicle_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)
):
    vehicle = _get_or_404(db, vehicle_id)
    vehicle.is_active = False
    db.commit()
