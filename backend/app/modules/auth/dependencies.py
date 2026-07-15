from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.users.model import User
from app.modules.users.repository import UserRepository


settings = get_settings()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=(
        f"{settings.api_v1_prefix}/auth/login"
    ),
)


def credentials_exception() -> HTTPException:
    """
    Respuesta estándar para token ausente, inválido
    o usuario no autorizado.
    """

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=(
            "No fue posible validar las credenciales."
        ),
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )


def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> User:
    """
    Obtiene el usuario asociado al JWT recibido.
    """

    try:
        payload = decode_access_token(
            token
        )

        username = payload.get("sub")
        token_type = payload.get("type")

        if not isinstance(username, str):
            raise credentials_exception()

        if token_type != "access":
            raise credentials_exception()

    except InvalidTokenError as exc:
        raise credentials_exception() from exc

    user_repository = UserRepository(
        session
    )

    user = user_repository.get_by_username(
        username
    )

    if user is None:
        raise credentials_exception()

    if not user.is_active:
        raise credentials_exception()

    return user


CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]