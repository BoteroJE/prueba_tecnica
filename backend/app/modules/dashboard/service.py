from sqlalchemy.orm import Session

from app.modules.dashboard.repository import (
    DashboardRepository,
)
from app.modules.dashboard.schemas import (
    DashboardResponse,
)


class DashboardService:
    """
    Reglas y coordinación del dashboard.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.repository = DashboardRepository(
            session
        )

    def get_dashboard(
        self,
    ) -> DashboardResponse:
        metrics = self.repository.get_metrics()

        return DashboardResponse(
            **metrics
        )