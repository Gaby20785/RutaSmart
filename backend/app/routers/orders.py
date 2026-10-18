import csv
import io
from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import staff
from app.models import Order, OrderStatus, User
from app.schemas import ImportResult, ImportRowError, OrderCreate, OrderOut
from app.services.geo import GeocodingError, geocode

router = APIRouter(prefix="/api/orders", tags=["Pedidos"])

CSV_COLUMNS = [
    "reference",
    "customer_name",
    "customer_phone",
    "address",
    "lat",
    "lng",
    "delivery_date",
    "window_start",
    "window_end",
    "weight_kg",
    "volume_m3",
    "service_minutes",
]
REQUIRED_COLUMNS = set(CSV_COLUMNS) - {"customer_phone", "lat", "lng", "service_minutes"}
NUMERIC_COLUMNS = {"lat", "lng", "weight_kg", "volume_m3"}
MAX_CSV_BYTES = 2 * 1024 * 1024
MAX_CSV_ROWS = 1000


def _get_or_404(db: Session, order_id: int) -> Order:
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido no encontrado")
    return order


def _resolve_coordinates(data: OrderCreate) -> tuple[float, float]:
    if data.lat is not None and data.lng is not None:
        return data.lat, data.lng
    return geocode(data.address)


def _format_validation_error(exc: ValidationError) -> str:
    parts = []
    for err in exc.errors():
        field = ".".join(str(p) for p in err["loc"])
        message = err["msg"].removeprefix("Value error, ")
        parts.append(f"{field}: {message}" if field else message)
    return "; ".join(parts)


@router.get("", response_model=list[OrderOut])
def list_orders(
    delivery_date: date | None = None,
    status_filter: OrderStatus | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(staff),
):
    query = select(Order).order_by(Order.delivery_date, Order.window_start, Order.id)
    if delivery_date:
        query = query.where(Order.delivery_date == delivery_date)
    if status_filter:
        query = query.where(Order.status == status_filter)
    return db.scalars(query).all()


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate, db: Session = Depends(get_db), _: User = Depends(staff)):
    try:
        lat, lng = _resolve_coordinates(data)
    except GeocodingError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, str(exc)) from None
    order = Order(**data.model_dump(exclude={"lat", "lng"}), lat=lat, lng=lng)
    db.add(order)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Ya existe un pedido con esa referencia"
        ) from None
    db.refresh(order)
    return order


@router.put("/{order_id}", response_model=OrderOut)
def update_order(
    order_id: int, data: OrderCreate, db: Session = Depends(get_db), _: User = Depends(staff)
):
    order = _get_or_404(db, order_id)
    if order.status in (OrderStatus.delivered, OrderStatus.failed):
        raise HTTPException(status.HTTP_409_CONFLICT, "No se puede modificar un pedido ya cerrado")
    address_changed = data.address != order.address
    if data.lat is None and not address_changed:
        lat, lng = order.lat, order.lng
    else:
        try:
            lat, lng = _resolve_coordinates(data)
        except GeocodingError as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, str(exc)) from None
    for key, value in data.model_dump(exclude={"lat", "lng"}).items():
        setattr(order, key, value)
    order.lat, order.lng = lat, lng
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Ya existe un pedido con esa referencia"
        ) from None
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db), _: User = Depends(staff)):
    order = _get_or_404(db, order_id)
    if order.status != OrderStatus.pending:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Solo se pueden eliminar pedidos pendientes de planificar"
        )
    db.delete(order)
    db.commit()


@router.post("/import", response_model=ImportResult)
async def import_orders(
    file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(staff)
):
    """Importa pedidos desde CSV (separador `,` o `;`). Las filas con errores se
    informan sin bloquear el resto."""
    raw = await file.read(MAX_CSV_BYTES + 1)
    if len(raw) > MAX_CSV_BYTES:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "El archivo supera los 2 MB")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")

    first_line = text.split("\n", 1)[0]
    delimiter = ";" if first_line.count(";") > first_line.count(",") else ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    headers = {h.strip() for h in (reader.fieldnames or [])}
    missing = REQUIRED_COLUMNS - headers
    if missing:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"Faltan columnas obligatorias: {', '.join(sorted(missing))}",
        )

    existing = set(db.scalars(select(Order.reference)).all())
    created = 0
    errors: list[ImportRowError] = []

    for row_number, row in enumerate(reader, start=2):
        if row_number - 1 > MAX_CSV_ROWS:
            errors.append(ImportRowError(row=row_number, reference=None, error="Límite de filas"))
            break
        values = {k.strip(): (v or "").strip() for k, v in row.items() if k}
        if not any(values.values()):
            continue
        reference = values.get("reference") or None
        for key in NUMERIC_COLUMNS:
            if "," in values.get(key, "") and "." not in values[key]:
                values[key] = values[key].replace(",", ".")  # decimales con coma (Excel ES)
        payload = {k: v for k, v in values.items() if k in CSV_COLUMNS and v != ""}

        try:
            data = OrderCreate.model_validate(payload)
        except ValidationError as exc:
            errors.append(
                ImportRowError(
                    row=row_number, reference=reference, error=_format_validation_error(exc)
                )
            )
            continue
        if data.reference in existing:
            errors.append(
                ImportRowError(row=row_number, reference=reference, error="Referencia duplicada")
            )
            continue
        try:
            lat, lng = _resolve_coordinates(data)
        except GeocodingError as exc:
            errors.append(ImportRowError(row=row_number, reference=reference, error=str(exc)))
            continue

        db.add(Order(**data.model_dump(exclude={"lat", "lng"}), lat=lat, lng=lng))
        existing.add(data.reference)
        created += 1

    db.commit()
    return ImportResult(created=created, errors=errors)
