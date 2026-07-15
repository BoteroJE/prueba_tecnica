from dataclasses import asdict, dataclass
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
)
from app.importers.ods_reader import read_ods_sheet
from app.modules.eps.model import Eps
from app.modules.patients.model import Patient
from app.modules.users.model import User
from app.shared.enums import (
    DocumentType,
    Gender,
    PatientStatus,
    Priority,
    UserRole,
)


EnumType = TypeVar(
    "EnumType",
    bound=Enum,
)


@dataclass
class EntityImportStats:
    created: int = 0
    updated: int = 0


@dataclass
class ImportResult:
    eps: EntityImportStats
    users: EntityImportStats
    patients: EntityImportStats

    def to_dict(
        self,
    ) -> dict[str, dict[str, int]]:
        return {
            "eps": asdict(self.eps),
            "users": asdict(self.users),
            "patients": asdict(self.patients),
        }


class OdsImportError(ValueError):
    """
    Error de validación durante la importación.
    """

    pass


def _required(
    row: dict[str, str],
    field: str,
    sheet: str,
) -> str:
    """
    Obtiene un campo obligatorio.
    """

    value = row.get(field, "").strip()

    if not value:
        row_number = row.get(
            "__row_number__",
            "?",
        )

        raise OdsImportError(
            f"Hoja '{sheet}', fila {row_number}: "
            f"falta el campo obligatorio '{field}'."
        )

    return value


def _optional(
    row: dict[str, str],
    field: str,
) -> str | None:
    """
    Obtiene un campo opcional.
    """

    value = row.get(field, "").strip()

    return value or None


def _parse_integer(
    value: str,
    *,
    field: str,
    row_number: str,
) -> int:
    try:
        result = int(value)
    except ValueError as exc:
        raise OdsImportError(
            f"Fila {row_number}: '{field}' "
            f"debe ser un número entero: {value!r}."
        ) from exc

    if result <= 0:
        raise OdsImportError(
            f"Fila {row_number}: '{field}' "
            "debe ser mayor que cero."
        )

    return result


def _parse_date(
    value: str,
    *,
    field: str,
    row_number: str,
) -> date:
    try:
        result = date.fromisoformat(value)
    except ValueError as exc:
        raise OdsImportError(
            f"Fila {row_number}: '{field}' "
            f"no es una fecha válida: {value!r}."
        ) from exc

    if result > date.today():
        raise OdsImportError(
            f"Fila {row_number}: '{field}' "
            f"no puede ser futura: {value!r}."
        )

    return result


def _parse_datetime(
    value: str,
    *,
    field: str,
    row_number: str,
) -> datetime:
    normalized_value = value.strip().replace(
        "T",
        " ",
    )

    supported_formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    )

    for date_format in supported_formats:
        try:
            return datetime.strptime(
                normalized_value,
                date_format,
            )
        except ValueError:
            continue

    raise OdsImportError(
        f"Fila {row_number}: '{field}' "
        f"no es una fecha y hora válida: {value!r}."
    )


def _parse_bool(
    value: str,
    *,
    field: str,
    row_number: str,
) -> bool:
    normalized_value = value.strip().casefold()

    true_values = {
        "verdadero",
        "true",
        "1",
        "sí",
        "si",
    }

    false_values = {
        "falso",
        "false",
        "0",
        "no",
    }

    if normalized_value in true_values:
        return True

    if normalized_value in false_values:
        return False

    raise OdsImportError(
        f"Fila {row_number}: '{field}' "
        f"no es un booleano válido: {value!r}."
    )


def _parse_enum(
    enum_class: type[EnumType],
    value: str,
    *,
    field: str,
    row_number: str,
) -> EnumType:
    try:
        return enum_class(value)
    except ValueError as exc:
        allowed_values = ", ".join(
            str(member.value)
            for member in enum_class
        )

        raise OdsImportError(
            f"Fila {row_number}: "
            f"valor inválido para '{field}': "
            f"{value!r}. "
            f"Valores permitidos: {allowed_values}."
        ) from exc


def _import_eps(
    session: Session,
    rows: list[dict[str, str]],
) -> tuple[
    dict[str, Eps],
    EntityImportStats,
]:
    stats = EntityImportStats()

    existing_eps = {
        eps.code: eps
        for eps in session.scalars(
            select(Eps)
        ).all()
    }

    for row in rows:
        code = _required(
            row,
            "eps_codigo",
            "Catalogos",
        )

        name = _required(
            row,
            "eps_nombre",
            "Catalogos",
        )

        eps = existing_eps.get(code)

        if eps is None:
            eps = Eps(
                code=code,
                name=name,
                is_active=True,
            )

            session.add(eps)

            existing_eps[code] = eps

            stats.created += 1

            continue

        changed = (
            eps.name != name
            or not eps.is_active
        )

        eps.name = name
        eps.is_active = True

        if changed:
            stats.updated += 1

    # Necesitamos los IDs de las EPS antes
    # de crear los pacientes.
    session.flush()

    return existing_eps, stats


def _import_users(
    session: Session,
    rows: list[dict[str, str]],
) -> EntityImportStats:
    stats = EntityImportStats()

    current_users = session.scalars(
        select(User)
    ).all()

    existing_by_username = {
        user.username: user
        for user in current_users
    }

    existing_by_id = {
        user.id: user
        for user in current_users
    }

    for row in rows:
        row_number = row.get(
            "__row_number__",
            "?",
        )

        source_id = _parse_integer(
            _required(
                row,
                "usuario_id",
                "Usuarios_Login",
            ),
            field="usuario_id",
            row_number=row_number,
        )

        username = _required(
            row,
            "usuario",
            "Usuarios_Login",
        )

        full_name = _required(
            row,
            "nombre",
            "Usuarios_Login",
        )

        role = _parse_enum(
            UserRole,
            _required(
                row,
                "rol",
                "Usuarios_Login",
            ),
            field="rol",
            row_number=row_number,
        )

        is_active = _parse_bool(
            _required(
                row,
                "activo",
                "Usuarios_Login",
            ),
            field="activo",
            row_number=row_number,
        )

        demo_password = _required(
            row,
            "password_demo",
            "Usuarios_Login",
        )

        user = existing_by_username.get(
            username
        )

        if user is None:
            conflicting_user = existing_by_id.get(
                source_id
            )

            if conflicting_user is not None:
                raise OdsImportError(
                    "Hoja 'Usuarios_Login', "
                    f"fila {row_number}: "
                    f"usuario_id {source_id} ya pertenece "
                    f"al usuario "
                    f"{conflicting_user.username!r}."
                )

            user = User(
                id=source_id,
                username=username,
                full_name=full_name,
                password_hash=hash_password(
                    demo_password
                ),
                role=role,
                is_active=is_active,
            )

            session.add(user)

            existing_by_username[username] = user
            existing_by_id[source_id] = user

            stats.created += 1

            continue

        password_is_valid = verify_password(
            demo_password,
            user.password_hash,
        )

        changed = (
            user.full_name != full_name
            or user.role != role
            or user.is_active != is_active
            or not password_is_valid
        )

        user.full_name = full_name
        user.role = role
        user.is_active = is_active

        if not password_is_valid:
            user.password_hash = hash_password(
                demo_password
            )

        if changed:
            stats.updated += 1

    return stats


def _import_patients(
    session: Session,
    rows: list[dict[str, str]],
    eps_by_code: dict[str, Eps],
) -> EntityImportStats:
    stats = EntityImportStats()

    current_patients = session.scalars(
        select(Patient)
    ).all()

    existing_by_document = {
        patient.document_number: patient
        for patient in current_patients
    }

    existing_by_id = {
        patient.id: patient
        for patient in current_patients
    }

    for row in rows:
        row_number = row.get(
            "__row_number__",
            "?",
        )

        source_id = _parse_integer(
            _required(
                row,
                "paciente_id",
                "Pacientes",
            ),
            field="paciente_id",
            row_number=row_number,
        )

        document_number = _required(
            row,
            "documento",
            "Pacientes",
        )

        eps_code = _required(
            row,
            "eps_codigo",
            "Pacientes",
        )

        eps = eps_by_code.get(eps_code)

        if eps is None:
            raise OdsImportError(
                "Hoja 'Pacientes', "
                f"fila {row_number}: "
                f"la EPS {eps_code!r} "
                "no existe en Catalogos."
            )

        birth_date = _parse_date(
            _required(
                row,
                "fecha_nacimiento",
                "Pacientes",
            ),
            field="fecha_nacimiento",
            row_number=row_number,
        )

        created_at = _parse_datetime(
            _required(
                row,
                "fecha_creacion",
                "Pacientes",
            ),
            field="fecha_creacion",
            row_number=row_number,
        )

        updated_at = _parse_datetime(
            _required(
                row,
                "fecha_actualizacion",
                "Pacientes",
            ),
            field="fecha_actualizacion",
            row_number=row_number,
        )

        if updated_at < created_at:
            raise OdsImportError(
                "Hoja 'Pacientes', "
                f"fila {row_number}: "
                "fecha_actualizacion es anterior "
                "a fecha_creacion."
            )

        values = {
            "document_type": _parse_enum(
                DocumentType,
                _required(
                    row,
                    "tipo_documento",
                    "Pacientes",
                ),
                field="tipo_documento",
                row_number=row_number,
            ),
            "full_name": _required(
                row,
                "nombre_completo",
                "Pacientes",
            ),
            "birth_date": birth_date,
            "gender": _parse_enum(
                Gender,
                _required(
                    row,
                    "genero",
                    "Pacientes",
                ),
                field="genero",
                row_number=row_number,
            ),
            "phone": _required(
                row,
                "telefono",
                "Pacientes",
            ),
            "email": _optional(
                row,
                "correo",
            ),
            "city": _optional(
                row,
                "ciudad",
            ),
            "eps_id": eps.id,
            "priority": _parse_enum(
                Priority,
                _required(
                    row,
                    "prioridad",
                    "Pacientes",
                ),
                field="prioridad",
                row_number=row_number,
            ),
            "status": _parse_enum(
                PatientStatus,
                _required(
                    row,
                    "estado",
                    "Pacientes",
                ),
                field="estado",
                row_number=row_number,
            ),
            "created_at": created_at,
            "updated_at": updated_at,
        }

        patient = existing_by_document.get(
            document_number
        )

        if patient is None:
            conflicting_patient = (
                existing_by_id.get(source_id)
            )

            if conflicting_patient is not None:
                raise OdsImportError(
                    "Hoja 'Pacientes', "
                    f"fila {row_number}: "
                    f"paciente_id {source_id} "
                    "ya pertenece al documento "
                    f"{conflicting_patient.document_number!r}."
                )

            patient = Patient(
                id=source_id,
                document_number=document_number,
                **values,
            )

            session.add(patient)

            existing_by_document[
                document_number
            ] = patient

            existing_by_id[source_id] = patient

            stats.created += 1

            continue

        changed = any(
            getattr(patient, field) != value
            for field, value in values.items()
        )

        for field, value in values.items():
            setattr(
                patient,
                field,
                value,
            )

        if changed:
            stats.updated += 1

    return stats


def import_ods_data(
    session: Session,
    file_path: Path,
) -> ImportResult:
    """
    Importa todos los datos dentro de una única transacción.

    Si cualquier fila falla, se revierte toda la operación.
    """

    eps_rows = read_ods_sheet(
        file_path,
        "Catalogos",
    )

    user_rows = read_ods_sheet(
        file_path,
        "Usuarios_Login",
    )

    patient_rows = read_ods_sheet(
        file_path,
        "Pacientes",
    )

    try:
        eps_by_code, eps_stats = _import_eps(
            session,
            eps_rows,
        )

        user_stats = _import_users(
            session,
            user_rows,
        )

        patient_stats = _import_patients(
            session,
            patient_rows,
            eps_by_code,
        )

        session.commit()

    except Exception:
        session.rollback()
        raise

    return ImportResult(
        eps=eps_stats,
        users=user_stats,
        patients=patient_stats,
    )