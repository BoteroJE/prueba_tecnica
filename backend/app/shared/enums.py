from enum import Enum


class DocumentType(str, Enum):
    CC = "CC"
    TI = "TI"
    CE = "CE"
    PA = "PA"


class Gender(str, Enum):
    FEMALE = "Femenino"
    MALE = "Masculino"
    OTHER = "Otro"
    PREFER_NOT_TO_SAY = "Prefiere no informar"


class Priority(str, Enum):
    HIGH = "Alta"
    MEDIUM = "Media"
    LOW = "Baja"


class PatientStatus(str, Enum):
    PENDING = "Pendiente"
    IN_PROGRESS = "En atención"
    ATTENDED = "Atendido"


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERADOR"


def enum_values(enum_class: type[Enum]) -> list[str]:
    """
    Indica a SQLAlchemy que debe guardar los valores
    del enum y no los nombres internos de Python.

    Por ejemplo:
    - Guarda "En atención"
    - No guarda "IN_PROGRESS"
    """

    return [
        str(member.value)
        for member in enum_class
    ]