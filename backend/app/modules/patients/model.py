from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.modules.eps.model import Eps
from app.shared.enums import (
    DocumentType,
    Gender,
    PatientStatus,
    Priority,
    enum_values,
)


class Patient(Base):
    __tablename__ = "patients"

    __table_args__ = (
        Index(
            "ix_patients_status_priority",
            "status",
            "priority",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    document_type: Mapped[DocumentType] = mapped_column(
        SqlEnum(
            DocumentType,
            values_callable=enum_values,
            native_enum=False,
            validate_strings=True,
            create_constraint=True,
            name="document_type",
        ),
        nullable=False,
    )

    document_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        index=True,
        nullable=False,
    )

    birth_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    gender: Mapped[Gender] = mapped_column(
        SqlEnum(
            Gender,
            values_callable=enum_values,
            native_enum=False,
            validate_strings=True,
            create_constraint=True,
            name="gender",
        ),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    eps_id: Mapped[int] = mapped_column(
        ForeignKey(
            "eps.id",
            ondelete="RESTRICT",
        ),
        index=True,
        nullable=False,
    )

    eps: Mapped[Eps] = relationship(
        back_populates="patients",
    )

    priority: Mapped[Priority] = mapped_column(
        SqlEnum(
            Priority,
            values_callable=enum_values,
            native_enum=False,
            validate_strings=True,
            create_constraint=True,
            name="patient_priority",
        ),
        nullable=False,
        default=Priority.MEDIUM,
    )

    status: Mapped[PatientStatus] = mapped_column(
        SqlEnum(
            PatientStatus,
            values_callable=enum_values,
            native_enum=False,
            validate_strings=True,
            create_constraint=True,
            name="patient_status",
        ),
        nullable=False,
        default=PatientStatus.PENDING,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    def __repr__(self) -> str:
        return (
            f"Patient(id={self.id!r}, "
            f"document_number={self.document_number!r}, "
            f"full_name={self.full_name!r})"
        )