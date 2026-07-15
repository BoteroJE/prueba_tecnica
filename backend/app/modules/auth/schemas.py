from typing import Literal

from pydantic import BaseModel

from app.modules.users.schemas import UserResponse


class TokenResponse(BaseModel):
    """
    Respuesta enviada después de un login exitoso.
    """

    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int
    user: UserResponse