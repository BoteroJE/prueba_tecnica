from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import (
    get_current_user,
)
from app.modules.eps.schemas import EpsResponse
from app.modules.eps.service import EpsService


router = APIRouter(
    prefix="/eps",
    tags=["EPS"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "",
    response_model=list[EpsResponse],
    summary="Consultar catálogo de EPS",
)
def list_eps(
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> list[EpsResponse]:
    service = EpsService(session)

    eps_records = service.list_active()

    return [
        EpsResponse.model_validate(eps)
        for eps in eps_records
    ]