from pathlib import Path

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.db.init_db import create_database_tables
from app.importers.ods_importer import (
    ImportResult,
    import_ods_data,
)


def seed_database(
    file_path: Path | None = None,
) -> ImportResult:
    """
    Crea las tablas e importa los datos del ODS.

    Si no se proporciona una ruta, se utiliza SEED_FILE,
    definido en .env.
    """

    settings = get_settings()

    source_file = (
        file_path
        if file_path is not None
        else settings.seed_file_path
    )

    create_database_tables()

    with SessionLocal() as session:
        return import_ods_data(
            session,
            source_file,
        )