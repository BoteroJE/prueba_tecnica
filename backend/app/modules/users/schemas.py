from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.shared.enums import UserRole


class UserResponse(BaseModel):
    """
    Información pública de un usuario.

    Nunca debe incluir password_hash.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    username: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime