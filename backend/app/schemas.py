from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from app.models import OrderStatus, Role


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- Usuarios y autenticación ----------


class UserOut(ORMModel):
    id: int
    email: str
    full_name: str
    role: Role
    is_active: bool


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=72)
    role: Role


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Conductores ----------


class DriverBase(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=6, max_length=30)
    license_number: str = Field(min_length=3, max_length=30)


class DriverCreate(DriverBase):
    """Si se indican email y contraseña, se crea también la cuenta de acceso del conductor."""

    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=72)

    @model_validator(mode="after")
    def account_fields_together(self):
        if (self.email is None) != (self.password is None):
            raise ValueError("Para crear la cuenta del conductor indica email y contraseña")
        return self


class DriverUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    phone: str | None = Field(default=None, min_length=6, max_length=30)
    license_number: str | None = Field(default=None, min_length=3, max_length=30)
    is_active: bool | None = None


class DriverOut(DriverBase, ORMModel):
    id: int
    is_active: bool
    user_id: int | None


class DriverBrief(ORMModel):
    id: int
    full_name: str
    phone: str


# ---------- Vehículos ----------


def _normalize_plate(value: str) -> str:
    return value.replace(" ", "").replace("-", "").upper()


class VehicleBase(BaseModel):
    plate: str = Field(min_length=4, max_length=15)
    model: str = Field(default="", max_length=80)
    capacity_kg: float = Field(gt=0, le=40000)
    capacity_m3: float = Field(gt=0, le=100)
    driver_id: int | None = None

    @field_validator("plate")
    @classmethod
    def normalize_plate(cls, v: str) -> str:
        return _normalize_plate(v)


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    plate: str | None = Field(default=None, min_length=4, max_length=15)
    model: str | None = Field(default=None, max_length=80)
    capacity_kg: float | None = Field(default=None, gt=0, le=40000)
    capacity_m3: float | None = Field(default=None, gt=0, le=100)
    driver_id: int | None = None
    is_active: bool | None = None

    @field_validator("plate")
    @classmethod
    def normalize_plate(cls, v: str | None) -> str | None:
        return _normalize_plate(v) if v else v


class VehicleBrief(ORMModel):
    id: int
    plate: str
    model: str
    capacity_kg: float
    capacity_m3: float


class VehicleOut(VehicleBase, ORMModel):
    id: int
    is_active: bool
    driver: DriverBrief | None


# ---------- Pedidos ----------


class OrderBase(BaseModel):
    reference: str = Field(min_length=1, max_length=40)
    customer_name: str = Field(min_length=2, max_length=120)
    customer_phone: str = Field(default="", max_length=30)
    address: str = Field(min_length=5, max_length=255)
    delivery_date: date
    window_start: time
    window_end: time
    weight_kg: float = Field(gt=0, le=5000)
    volume_m3: float = Field(gt=0, le=50)
    service_minutes: int = Field(default=5, ge=1, le=120)

    @model_validator(mode="after")
    def window_is_valid(self):
        if self.window_end <= self.window_start:
            raise ValueError("La hora de fin de la ventana debe ser posterior a la de inicio")
        return self


class OrderCreate(OrderBase):
    """Si no se indican lat/lng, la dirección se geocodifica automáticamente."""

    lat: float | None = Field(default=None, ge=-90, le=90)
    lng: float | None = Field(default=None, ge=-180, le=180)

    @model_validator(mode="after")
    def coordinates_together(self):
        if (self.lat is None) != (self.lng is None):
            raise ValueError("Indica latitud y longitud, o ninguna de las dos")
        return self


class OrderOut(OrderBase, ORMModel):
    id: int
    lat: float
    lng: float
    status: OrderStatus


class ImportRowError(BaseModel):
    row: int
    reference: str | None
    error: str


class ImportResult(BaseModel):
    created: int
    errors: list[ImportRowError]


# ---------- Rutas ----------


class OptimizeRequest(BaseModel):
    plan_date: date
    vehicle_ids: list[int] | None = None
    # True: reparte el trabajo entre conductores (algo más de km). False: mínimos km.
    balance_workload: bool = True


class StopOut(ORMModel):
    sequence: int
    eta: time
    order: OrderOut


class RouteOut(ORMModel):
    id: int
    vehicle: VehicleBrief
    driver: DriverBrief | None
    distance_km: float
    duration_min: int
    load_kg: float
    load_m3: float
    start_time: time
    end_time: time
    stops: list[StopOut]


class UnassignedOut(BaseModel):
    order: OrderOut
    reason: str


class RoutePlanOut(BaseModel):
    id: int
    plan_date: date
    created_at: datetime | None
    total_distance_km: float
    baseline_distance_km: float
    savings_pct: float
    orders_planned: int
    vehicles_used: int
    routes: list[RouteOut]
    unassigned: list[UnassignedOut]


class DepotOut(BaseModel):
    name: str
    lat: float
    lng: float


class AppConfigOut(BaseModel):
    depot: DepotOut
    shift_start: time
    shift_end: time
