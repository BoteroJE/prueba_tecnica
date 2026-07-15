from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.modules.patients.model import Patient
from app.shared.enums import (
    PatientStatus,
    Priority,
)


class DashboardRepository:
    """
    Consultas agregadas para los indicadores operativos.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def get_metrics(
        self,
    ) -> dict[str, int]:
        """
        Calcula todos los indicadores mediante una única
        consulta a la base de datos.
        """

        statement = select(
            func.count(
                Patient.id
            ).label(
                "total_patients"
            ),

            func.coalesce(
                func.sum(
                    case(
                        (
                            Patient.status
                            == PatientStatus.PENDING,
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label(
                "pending_patients"
            ),

            func.coalesce(
                func.sum(
                    case(
                        (
                            Patient.status
                            == PatientStatus.IN_PROGRESS,
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label(
                "in_progress_patients"
            ),

            func.coalesce(
                func.sum(
                    case(
                        (
                            Patient.status
                            == PatientStatus.ATTENDED,
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label(
                "attended_patients"
            ),

            func.coalesce(
                func.sum(
                    case(
                        (
                            Patient.priority
                            == Priority.HIGH,
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label(
                "high_priority_patients"
            ),
        )

        result = self.session.execute(
            statement
        ).mappings().one()

        return {
            "total_patients": int(
                result["total_patients"]
            ),
            "pending_patients": int(
                result["pending_patients"]
            ),
            "in_progress_patients": int(
                result["in_progress_patients"]
            ),
            "attended_patients": int(
                result["attended_patients"]
            ),
            "high_priority_patients": int(
                result["high_priority_patients"]
            ),
        }