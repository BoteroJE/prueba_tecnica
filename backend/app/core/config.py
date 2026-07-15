from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# backend/app/core/config.py
# parents[0] = core
# parents[1] = app
# parents[2] = backend
BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Configuración general de la aplicación.

    Los valores pueden sobrescribirse desde el archivo .env
    o mediante variables de entorno del sistema operativo.
    """

    app_name: str = "Clinic Patient Tracker API"
    app_version: str = "0.1.0"
    app_environment: str = "development"
    debug: bool = True

    api_v1_prefix: str = "/api/v1"

    database_url: str = (
        f"sqlite:///{(BACKEND_DIR / 'data' / 'clinic.db').as_posix()}"
    )

    jwt_secret_key: str = Field(
        default="change-this-development-secret-key-before-production-2026",
        min_length=32,
    )
    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = Field(
        default=60,
        ge=1,
        le=1440,
    )

    cors_origins: list[str] = [
        "http://localhost:5173",
    ]

    seed_file: str = "data/raw/datos_sinteticos.ods"

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def seed_file_path(self) -> Path:
        """
        Retorna la ruta absoluta del archivo ODS.
        """

        path = Path(self.seed_file)

        if path.is_absolute():
            return path

        return BACKEND_DIR / path

    def ensure_directories(self) -> None:
        """
        Crea las carpetas de datos cuando todavía no existen.
        """

        (BACKEND_DIR / "data").mkdir(
            parents=True,
            exist_ok=True,
        )

        self.seed_file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


@lru_cache
def get_settings() -> Settings:
    """
    Retorna una única instancia de configuración.
    """

    return Settings()