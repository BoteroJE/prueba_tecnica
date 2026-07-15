from pydantic import BaseModel, Field


class DashboardResponse(BaseModel):
    """
    Indicadores generales de la atención de pacientes.
    """

    total_patients: int = Field(
        ge=0,
        description="Cantidad total de pacientes registrados.",
    )

    pending_patients: int = Field(
        ge=0,
        description="Pacientes pendientes de atención.",
    )

    in_progress_patients: int = Field(
        ge=0,
        description="Pacientes actualmente en atención.",
    )

    attended_patients: int = Field(
        ge=0,
        description="Pacientes que ya fueron atendidos.",
    )

    high_priority_patients: int = Field(
        ge=0,
        description="Pacientes clasificados con prioridad alta.",
    )