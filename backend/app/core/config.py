"""Application configuration loaded from environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed, validated application settings.

    Missing required variables cause an immediate startup failure
    with a clear diagnostic message.
    """

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # --- Application ---
    APP_NAME: str = "FleetFlow"
    DEBUG: bool = False

    # --- Database ---
    DATABASE_URL: str  # e.g. postgresql+asyncpg://user:pass@localhost:5432/fleetflow

    # --- Security ---
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    BCRYPT_ROUNDS: int = 12

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]


settings = Settings()  # type: ignore[call-arg]
