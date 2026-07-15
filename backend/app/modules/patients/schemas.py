import re
from datetime import date, datetime
from typing import Annotated, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from app.modules.eps.schemas import EpsResponse
from app.shared.enums import (
    DocumentType,
    Gender,
    PatientStatus,
    Priority,
)


DocumentNumber = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=4,
        max_length=20,
        pattern=r"^[A-Za-z0-9.\-]+$",
    ),
]

FullName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=150,
    ),
]

PhoneNumber = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=7,
        max_length=20,
    ),
]

CityName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=2,
        max_length=80,
    ),
]


def validate_birth_date(
    value: date,
) -> date:
    if value > date.today():
        raise ValueError(
            "La fecha de nacimiento no puede ser futura."
        )

    return value


def validate_phone_number(
    value: str,
) -> str:
    """
    Permite números, espacios, paréntesis, guiones
    y un signo + al inicio.
    """

    if not re.fullmatch(
        r"\+?[0-9()\-\s]+",
        value,
    ):
        raise ValueError(
            "El teléfono contiene caracteres no permitidos."
        )

    digits = re.sub(
        r"\D",
        "",
        value,
    )

    if not 7 <= len(digits) <= 15:
        raise ValueError(
            "El teléfono debe contener entre "
            "7 y 15 dígitos."
        )

    return value


class PatientBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    document_type: DocumentType
    document_number: DocumentNumber
    full_name: FullName
    birth_date: date
    gender: Gender
    phone: PhoneNumber

    email: EmailStr | None = None
    city: CityName | None = None

    eps_id: int = Field(
        gt=0,
    )

    priority: Priority

    status: PatientStatus = (
        PatientStatus.PENDING
    )

    @field_validator("birth_date")
    @classmethod
    def birth_date_not_future(
        cls,
        value: date,
    ) -> date:
        return validate_birth_date(value)

    @field_validator("phone")
    @classmethod
    def phone_has_valid_format(
        cls,
        value: str,
    ) -> str:
        return validate_phone_number(value)


class PatientCreate(PatientBase):
    """
    Datos permitidos al registrar un paciente.
    """

    pass


class PatientUpdate(BaseModel):
    """
    Todos los campos son opcionales porque PATCH permite
    modificar únicamente los valores enviados.

    Los campos obligatorios del paciente no pueden enviarse
    explícitamente como null.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    document_type: DocumentType | None = None
    document_number: DocumentNumber | None = None
    full_name: FullName | None = None
    birth_date: date | None = None
    gender: Gender | None = None
    phone: PhoneNumber | None = None

    email: EmailStr | None = None
    city: CityName | None = None

    eps_id: int | None = Field(
        default=None,
        gt=0,
    )

    priority: Priority | None = None
    status: PatientStatus | None = None

    @field_validator("birth_date")
    @classmethod
    def birth_date_not_future(
        cls,
        value: date | None,
    ) -> date | None:
        if value is None:
            return None

        return validate_birth_date(value)

    @field_validator("phone")
    @classmethod
    def phone_has_valid_format(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return validate_phone_number(value)

    @model_validator(mode="after")
    def validate_update_fields(
        self,
    ) -> Self:
        if not self.model_fields_set:
            raise ValueError(
                "Debe proporcionar al menos un campo "
                "para actualizar."
            )

        required_fields = {
            "document_type",
            "document_number",
            "full_name",
            "birth_date",
            "gender",
            "phone",
            "eps_id",
            "priority",
            "status",
        }

        for field_name in (
            required_fields
            & self.model_fields_set
        ):
            if getattr(self, field_name) is None:
                raise ValueError(
                    f"El campo '{field_name}' "
                    "no puede ser null."
                )

        return self


class PatientResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    document_type: DocumentType
    document_number: str
    full_name: str
    birth_date: date
    gender: Gender
    phone: str
    email: str | None
    city: str | None
    priority: Priority
    status: PatientStatus
    created_at: datetime
    updated_at: datetime
    eps: EpsResponse


class PatientListResponse(BaseModel):
    items: list[PatientResponse]

    page: int
    page_size: int
    total: int
    total_pages: int

    has_previous: bool
    has_next: bool