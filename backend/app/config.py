from datetime import time

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./rutasmart.db"
    secret_key: str = "dev-secret-cambiar-en-produccion"
    access_token_minutes: int = 480
    bcrypt_rounds: int = 12
    cors_origins: str = "http://localhost:5173"

    # Almacén (depósito) desde el que salen y vuelven todas las rutas
    depot_name: str = "Almacén RutaSmart (Villaverde)"
    depot_lat: float = 40.3720
    depot_lng: float = -3.6950

    # Parámetros del optimizador
    shift_start: time = time(8, 0)
    shift_end: time = time(20, 0)
    avg_speed_kmh: float = 30.0
    road_factor: float = 1.3  # corrige la distancia en línea recta a distancia por carretera
    optimizer_time_limit_s: int = 3
    # Peso de la ruta más larga en el objetivo cuando se pide equilibrar la carga
    balance_coefficient: int = 2

    # "nominatim" (OpenStreetMap) o "none" para exigir latitud/longitud
    geocoder: str = "nominatim"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
