from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


if TYPE_CHECKING:
    from app.modules.patients.model import Patient


class Eps(Base):
    __tablename__ = "eps"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    patients: Mapped[list["Patient"]] = relationship(
        back_populates="eps",
    )

    def __repr__(self) -> str:
        return (
            f"Eps(id={self.id!r}, "
            f"code={self.code!r}, "
            f"name={self.name!r})"
        )