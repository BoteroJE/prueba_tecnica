from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.shared.enums import UserRole, enum_values


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    username: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        index=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(
            UserRole,
            values_callable=enum_values,
            native_enum=False,
            validate_strings=True,
            create_constraint=True,
            name="user_role",
        ),
        nullable=False,
        default=UserRole.OPERATOR,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, "
            f"username={self.username!r})"
        )