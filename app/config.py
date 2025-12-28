from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    bot_token: str = ""  # Telegram bot token (set via BOT_TOKEN env var)
    public_url: str = "http://localhost:8000"
    frontend_url: str = ""  # Frontend URL for CORS (optional)
    log_level: str = "INFO"
    openai_api_key: str = ""
    database_url: str = ""  # Supabase PostgreSQL connection string (set via DATABASE_URL env var)
    secret_key: str = "your-secret-key-change-in-production"  # JWT secret key (set via SECRET_KEY env var)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

