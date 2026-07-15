from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import (
    get_current_user,
)
from app.modules.patients.schemas import (
    PatientCreate,
    PatientListResponse,
    PatientResponse,
    PatientUpdate,
)
from app.modules.patients.service import (
    PatientService,
)
from app.shared.enums import (
    PatientStatus,
    Priority,
)


router = APIRouter(
    prefix="/patients",
    tags=["Pacientes"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "",
    response_model=PatientListResponse,
    summary="Consultar pacientes",
)
def list_patients(
    session: Annotated[
        Session,
        Depends(get_db),
    ],
    page: Annotated[
        int,
        Query(
            ge=1,
            description="Número de página.",
        ),
    ] = 1,
    page_size: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description=(
                "Registros por página."
            ),
        ),
    ] = 20,
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=100,
            description=(
                "Nombre o documento del paciente."
            ),
        ),
    ] = None,
    patient_status: Annotated[
        PatientStatus | None,
        Query(
            alias="status",
            description=(
                "Filtrar por estado."
            ),
        ),
    ] = None,
    priority: Annotated[
        Priority | None,
        Query(
            description=(
                "Filtrar por prioridad."
            ),
        ),
    ] = None,
    eps_id: Annotated[
        int | None,
        Query(
            gt=0,
            description="Filtrar por EPS.",
        ),
    ] = None,
) -> PatientListResponse:
    service = PatientService(session)

    return service.list_patients(
        page=page,
        page_size=page_size,
        search=search,
        patient_status=patient_status,
        priority=priority,
        eps_id=eps_id,
    )


@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="Consultar un paciente",
    responses={
        404: {
            "description": (
                "Paciente no encontrado."
            ),
        },
    },
)
def get_patient(
    patient_id: Annotated[
        int,
        Path(gt=0),
    ],
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> PatientResponse:
    service = PatientService(session)

    return service.get_patient(
        patient_id
    )


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un paciente",
    responses={
        404: {
            "description": (
                "EPS no encontrada."
            ),
        },
        409: {
            "description": (
                "Documento duplicado."
            ),
        },
    },
)
def create_patient(
    payload: PatientCreate,
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> PatientResponse:
    service = PatientService(session)

    return service.create_patient(
        payload
    )


@router.patch(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="Actualizar un paciente",
    responses={
        404: {
            "description": (
                "Paciente o EPS no encontrada."
            ),
        },
        409: {
            "description": (
                "Documento duplicado."
            ),
        },
    },
)
def update_patient(
    patient_id: Annotated[
        int,
        Path(gt=0),
    ],
    payload: PatientUpdate,
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> PatientResponse:
    service = PatientService(session)

    return service.update_patient(
        patient_id,
        payload,
    )


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un paciente",
    responses={
        404: {
            "description": (
                "Paciente no encontrado."
            ),
        },
    },
)
def delete_patient(
    patient_id: Annotated[
        int,
        Path(gt=0),
    ],
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> Response:
    service = PatientService(session)

    service.delete_patient(
        patient_id
    )

    return Response(
        status_code=(
            status.HTTP_204_NO_CONTENT
        )
    )