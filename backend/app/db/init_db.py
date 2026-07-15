from app.core.database import engine
from app.db.base import Base

# Estos imports registran los modelos dentro de Base.metadata.
from app.modules.eps.model import Eps  # noqa: F401
from app.modules.patients.model import Patient  # noqa: F401
from app.modules.users.model import User  # noqa: F401


def create_database_tables() -> None:
    """
    Crea las tablas que todavía no existen.

    Para esta prueba técnica utilizamos create_all porque
    el esquema es pequeño. Las migraciones con Alembic
    pueden incorporarse posteriormente.
    """

    Base.metadata.create_all(
        bind=engine,
    )