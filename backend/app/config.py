from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    debug: bool = False
    secret_key: str = "INSECURE-CHANGE-ME"
    database_url: str = "sqlite:///./flowforge.db"

    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173"
    )

    trusted_hosts: str = "localhost,127.0.0.1"

    access_token_minutes: int = 30
    rate_limit_auth: str = "10/minute"
    rate_limit_api: str = "120/minute"
    max_request_bytes: int = 1_048_576

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def allowed_origins(self):
        return [
            x.strip().rstrip("/")
            for x in self.cors_origins.split(",")
            if x.strip()
        ]

    @property
    def allowed_hosts(self):
        return [
            x.strip()
            for x in self.trusted_hosts.split(",")
            if x.strip()
        ]


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()


if settings.app_env.lower() == "production":
    if (
        settings.secret_key == "INSECURE-CHANGE-ME"
        or len(settings.secret_key) < 40
    ):
        raise RuntimeError(
            "Production SECRET_KEY must be unique and at least 40 characters."
        )

    if settings.debug:
        raise RuntimeError("DEBUG must be false in production.")

    if not settings.allowed_origins or "*" in settings.allowed_origins:
        raise RuntimeError(
            "Production CORS_ORIGINS must be an explicit allowlist."
        )

    if not settings.allowed_hosts:
        raise RuntimeError(
            "Production TRUSTED_HOSTS must be configured."
        )
