import math
import threading
import time

import httpx

from app.config import settings

EARTH_RADIUS_KM = 6371.0088
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "RutaSmart-MVP/0.1 (proyecto academico)"


class GeocodingError(Exception):
    pass


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Distancia en línea recta (círculo máximo) entre dos puntos, en km."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


# La política de uso de Nominatim permite como máximo 1 petición por segundo.
_rate_lock = threading.Lock()
_last_call = 0.0


def geocode(address: str) -> tuple[float, float]:
    """Devuelve (lat, lng) de una dirección. En el Sprint 2 se sustituye por Mapbox (RF17)."""
    if settings.geocoder != "nominatim":
        raise GeocodingError("La geocodificación está desactivada: indica latitud y longitud")

    global _last_call
    with _rate_lock:
        wait = 1.0 - (time.monotonic() - _last_call)
        if wait > 0:
            time.sleep(wait)
        try:
            response = httpx.get(
                NOMINATIM_URL,
                params={"q": address, "format": "json", "limit": 1},
                headers={"User-Agent": USER_AGENT},
                timeout=8,
            )
            response.raise_for_status()
            results = response.json()
        except httpx.HTTPError as exc:
            raise GeocodingError("No se pudo contactar con el servicio de geocodificación") from exc
        finally:
            _last_call = time.monotonic()

    if not results:
        raise GeocodingError(f"Dirección no encontrada: {address}")
    return float(results[0]["lat"]), float(results[0]["lon"])
