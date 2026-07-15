from sqlalchemy import (
    case,
    func,
    or_,
    select,
)
from sqlalchemy.orm import (
    Session,
    joinedload,
)

from app.modules.patients.model import Patient
from app.shared.enums import (
    PatientStatus,
    Priority,
)


def escape_like_value(
    value: str,
) -> str:
    """
    Evita que %, _ y \\ introducidos por el usuario
    actúen como comodines SQL.
    """

    return (
        value
        .replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


class PatientRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def get_by_id(
        self,
        patient_id: int,
    ) -> Patient | None:
        statement = (
            select(Patient)
            .options(
                joinedload(Patient.eps)
            )
            .where(
                Patient.id == patient_id
            )
        )

        return self.session.scalar(statement)

    def get_by_document(
        self,
        document_number: str,
    ) -> Patient | None:
        statement = select(Patient).where(
            Patient.document_number
            == document_number
        )

        return self.session.scalar(statement)

    def list(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None,
        patient_status: PatientStatus | None,
        priority: Priority | None,
        eps_id: int | None,
    ) -> tuple[list[Patient], int]:
        conditions = []

        if search:
            escaped_search = escape_like_value(
                search.strip()
            )

            search_pattern = (
                f"%{escaped_search}%"
            )

            conditions.append(
                or_(
                    Patient.full_name.ilike(
                        search_pattern,
                        escape="\\",
                    ),
                    Patient.document_number.ilike(
                        search_pattern,
                        escape="\\",
                    ),
                )
            )

        if patient_status is not None:
            conditions.append(
                Patient.status
                == patient_status
            )

        if priority is not None:
            conditions.append(
                Patient.priority
                == priority
            )

        if eps_id is not None:
            conditions.append(
                Patient.eps_id == eps_id
            )

        count_statement = (
            select(
                func.count(Patient.id)
            )
            .where(*conditions)
        )

        total = int(
            self.session.scalar(
                count_statement
            )
            or 0
        )

        status_order = case(
            (
                Patient.status
                == PatientStatus.PENDING,
                1,
            ),
            (
                Patient.status
                == PatientStatus.IN_PROGRESS,
                2,
            ),
            (
                Patient.status
                == PatientStatus.ATTENDED,
                3,
            ),
            else_=4,
        )

        priority_order = case(
            (
                Patient.priority
                == Priority.HIGH,
                1,
            ),
            (
                Patient.priority
                == Priority.MEDIUM,
                2,
            ),
            (
                Patient.priority
                == Priority.LOW,
                3,
            ),
            else_=4,
        )

        offset = (
            page - 1
        ) * page_size

        list_statement = (
            select(Patient)
            .options(
                joinedload(Patient.eps)
            )
            .where(*conditions)
            .order_by(
                status_order.asc(),
                priority_order.asc(),
                Patient.created_at.asc(),
                Patient.id.asc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        patients = list(
            self.session.scalars(
                list_statement
            ).all()
        )

        return patients, total

    def add(
        self,
        patient: Patient,
    ) -> Patient:
        self.session.add(patient)
        self.session.flush()

        return patient

    def delete(
        self,
        patient: Patient,
    ) -> None:
        self.session.delete(patient)
        self.session.flush()