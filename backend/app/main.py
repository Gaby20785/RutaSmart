from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, drivers, orders, routes, vehicles
from app.schemas import AppConfigOut, DepotOut


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Sprint 1: creación directa del esquema. Migraciones con Alembic previstas en Sprint 3.
    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="RutaSmart API",
    version="0.1.0",
    description="Optimizador de rutas de entrega con seguimiento en vivo · MVP Sprint 1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module in (auth, drivers, vehicles, orders, routes):
    app.include_router(module.router)


@app.get("/api/health", tags=["Sistema"])
def health():
    return {"status": "ok", "version": app.version}


@app.get("/api/config", response_model=AppConfigOut, tags=["Sistema"])
def config():
    return AppConfigOut(
        depot=DepotOut(name=settings.depot_name, lat=settings.depot_lat, lng=settings.depot_lng),
        shift_start=settings.shift_start,
        shift_end=settings.shift_end,
    )
