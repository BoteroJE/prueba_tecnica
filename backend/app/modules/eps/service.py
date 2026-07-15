from sqlalchemy.orm import Session

from app.modules.eps.model import Eps
from app.modules.eps.repository import EpsRepository


class EpsService:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.repository = EpsRepository(
            session
        )

    def list_active(
        self,
    ) -> list[Eps]:
        return self.repository.list_active()