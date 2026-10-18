from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import admin_only, staff
from app.models import Driver, Role, User
from app.schemas import DriverCreate, DriverOut, DriverUpdate
from app.security import hash_password

router = APIRouter(prefix="/api/drivers", tags=["Conductores"])

DUPLICATE = "Ya existe un conductor con ese número de licencia o un usuario con ese email"


def _get_or_404(db: Session, driver_id: int) -> Driver:
    driver = db.get(Driver, driver_id)
    if driver is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conductor no encontrado")
    return driver


@router.get("", response_model=list[DriverOut])
def list_drivers(
    include_inactive: bool = False, db: Session = Depends(get_db), _: User = Depends(staff)
):
    query = select(Driver).order_by(Driver.full_name)
    if not include_inactive:
        query = query.where(Driver.is_active)
    return db.scalars(query).all()


@router.post("", response_model=DriverOut, status_code=status.HTTP_201_CREATED)
def create_driver(data: DriverCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    driver = Driver(**data.model_dump(exclude={"email", "password"}))
    if data.email and data.password:
        driver.user = User(
            email=data.email.lower(),
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
            role=Role.driver,
        )
    db.add(driver)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, DUPLICATE) from None
    db.refresh(driver)
    return driver


@router.put("/{driver_id}", response_model=DriverOut)
def update_driver(
    driver_id: int,
    data: DriverUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
):
    driver = _get_or_404(db, driver_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(driver, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, DUPLICATE) from None
    db.refresh(driver)
    return driver


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_driver(driver_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    """Baja lógica: el conductor se conserva para el histórico de rutas."""
    driver = _get_or_404(db, driver_id)
    driver.is_active = False
    if driver.user:
        driver.user.is_active = False
    db.commit()
