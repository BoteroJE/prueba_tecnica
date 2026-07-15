from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings


settings = get_settings()

password_hasher = PasswordHash.recommended()

# Se utiliza para ejecutar una verificación de contraseña incluso cuando
# el usuario no existe. Esto reduce diferencias de tiempo entre:
# - usuario inexistente
# - contraseña incorrecta
DUMMY_PASSWORD_HASH = password_hasher.hash(
    "dummy-password-that-is-never-used"
)


def hash_password(password: str) -> str:
    """
    Convierte una contraseña en un hash seguro.

    La contraseña original nunca debe almacenarse
    directamente en la base de datos.
    """

    normalized_password = password.strip()

    if not normalized_password:
        raise ValueError(
            "La contraseña no puede estar vacía."
        )

    return password_hasher.hash(
        normalized_password
    )


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Compara una contraseña recibida con el hash almacenado.
    """

    if not plain_password or not hashed_password:
        return False

    return password_hasher.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    *,
    subject: str,
    role: str,
) -> str:
    """
    Crea un token JWT de acceso.

    El campo sub identifica de manera única al usuario.
    """

    now = datetime.now(timezone.utc)

    expiration = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Decodifica y valida un token JWT.

    PyJWT verificará:
    - Firma.
    - Algoritmo.
    - Fecha de vencimiento.
    - Presencia de sub, iat y exp.
    """

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[
            settings.jwt_algorithm,
        ],
        options={
            "require": [
                "sub",
                "iat",
                "exp",
            ],
        },
    )