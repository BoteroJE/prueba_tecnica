from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


settings = get_settings()


connect_args: dict[str, Any] = {}

if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False


engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)


if settings.database_url.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(
        dbapi_connection: Any,
        connection_record: Any,
    ) -> None:
        """
        Activa la validación de llaves foráneas en SQLite.
        """

        del connection_record

        cursor = dbapi_connection.cursor()

        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI que proporciona una sesión
    de base de datos por solicitud.
    """

    database_session = SessionLocal()

    try:
        yield database_session
    finally:
        database_session.close()