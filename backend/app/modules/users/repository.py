from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.model import User


class UserRepository:
    """
    Consultas relacionadas con usuarios.

    Este repositorio no contiene reglas de autenticación;
    solamente accede a la base de datos.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        normalized_username = username.strip()

        statement = select(User).where(
            User.username == normalized_username
        )

        return self.session.scalar(statement)

    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:
        return self.session.get(
            User,
            user_id,
        )