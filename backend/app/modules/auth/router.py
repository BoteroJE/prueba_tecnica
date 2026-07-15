from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.schemas import TokenResponse
from app.modules.auth.service import AuthService
from app.modules.users.schemas import UserResponse


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    responses={
        401: {
            "description": (
                "Usuario o contraseña incorrectos."
            ),
        },
    },
)
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> TokenResponse:
    """
    Valida las credenciales y genera un token JWT.
    """

    auth_service = AuthService(
        session
    )

    user = auth_service.authenticate(
        username=form_data.username,
        password=form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "Usuario o contraseña incorrectos."
            ),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    return auth_service.create_login_response(
        user
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Consultar usuario autenticado",
)
def get_authenticated_user(
    current_user: CurrentUser,
) -> UserResponse:
    """
    Retorna el usuario asociado al token enviado.
    """

    return UserResponse.model_validate(
        current_user
    )