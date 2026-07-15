from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    verify_password,
)
from app.modules.auth.schemas import TokenResponse
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserResponse


settings = get_settings()


class AuthService:
    """
    Reglas de negocio relacionadas con autenticación.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.user_repository = UserRepository(
            session
        )

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> User | None:
        """
        Valida usuario, contraseña y estado de la cuenta.
        """

        user = self.user_repository.get_by_username(
            username
        )

        # Se verifica un hash aunque el usuario no exista,
        # evitando una respuesta notablemente más rápida.
        hash_to_verify = (
            user.password_hash
            if user is not None
            else DUMMY_PASSWORD_HASH
        )

        password_is_valid = verify_password(
            password,
            hash_to_verify,
        )

        if user is None:
            return None

        if not password_is_valid:
            return None

        if not user.is_active:
            return None

        return user

    def create_login_response(
        self,
        user: User,
    ) -> TokenResponse:
        """
        Genera el JWT y la respuesta completa del login.
        """

        access_token = create_access_token(
            subject=user.username,
            role=user.role.value,
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=(
                settings.access_token_expire_minutes
                * 60
            ),
            user=UserResponse.model_validate(
                user
            ),
        )