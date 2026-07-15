from fastapi import APIRouter

from app.modules.auth.router import (
    router as auth_router,
)
from app.modules.dashboard.router import (
    router as dashboard_router,
)
from app.modules.eps.router import (
    router as eps_router,
)
from app.modules.patients.router import (
    router as patients_router,
)


api_router = APIRouter()


api_router.include_router(
    auth_router
)

api_router.include_router(
    dashboard_router
)

api_router.include_router(
    eps_router
)

api_router.include_router(
    patients_router
)