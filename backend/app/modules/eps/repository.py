from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.eps.model import Eps


class EpsRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def get_by_id(
        self,
        eps_id: int,
    ) -> Eps | None:
        return self.session.get(
            Eps,
            eps_id,
        )

    def get_by_code(
        self,
        code: str,
    ) -> Eps | None:
        statement = select(Eps).where(
            Eps.code == code.strip()
        )

        return self.session.scalar(statement)

    def list_active(
        self,
    ) -> list[Eps]:
        statement = (
            select(Eps)
            .where(Eps.is_active.is_(True))
            .order_by(Eps.name.asc())
        )

        return list(
            self.session.scalars(
                statement
            ).all()
        )