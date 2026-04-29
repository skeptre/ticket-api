from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "your-secret-key-change-in-production"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TICKET_API_",
        case_sensitive=True,
    )

    # Database configuration
    DATABASE_URL: str = "sqlite:///./ticket_api.db"

    # Security configuration
    SECRET_KEY: str = DEFAULT_SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application configuration
    DEBUG: bool = True
    APP_NAME: str = "Ticket API"
    VERSION: str = "1.0.0"

    @model_validator(mode="after")
    def validate_production_secret(self) -> "Settings":
        """Require an explicit secret when the app is not in debug mode."""
        if not self.DEBUG and self.SECRET_KEY == DEFAULT_SECRET_KEY:
            raise ValueError("TICKET_API_SECRET_KEY must be set when DEBUG is false")
        return self


settings = Settings()
