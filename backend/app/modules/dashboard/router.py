from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import (
    get_current_user,
)
from app.modules.dashboard.schemas import (
    DashboardResponse,
)
from app.modules.dashboard.service import (
    DashboardService,
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Consultar indicadores operativos",
)
def get_dashboard(
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> DashboardResponse:
    """
    Retorna los indicadores generales de pacientes.
    """

    service = DashboardService(
        session
    )

    return service.get_dashboard()