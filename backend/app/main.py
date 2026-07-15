from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api_router import api_router
from app.core.config import get_settings
from app.db.init_db import create_database_tables

from app.core.exception_handlers import (
    register_exception_handlers,
)


settings = get_settings()


@asynccontextmanager
async def lifespan(
    application: FastAPI,
) -> AsyncIterator[None]:
    """
    Acciones ejecutadas al iniciar y detener FastAPI.
    """

    del application

    settings.ensure_directories()
    create_database_tables()

    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "API REST para administrar pacientes en espera "
        "de atención, sus prioridades, estados e "
        "indicadores operativos."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=(
        f"{settings.api_v1_prefix}/openapi.json"
    ),
    lifespan=lifespan,
)

register_exception_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)


@app.get(
    "/",
    tags=["Sistema"],
    summary="Información general",
)
def root() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "documentation": "/docs",
    }


@app.get(
    f"{settings.api_v1_prefix}/health",
    tags=["Sistema"],
    summary="Verificar el estado de la API",
)
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": (
            settings.app_environment
        ),
    }