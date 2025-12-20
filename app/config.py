from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    bot_token: str
    public_url: str = "http://localhost:8000"
    frontend_url: str = ""  # Frontend URL for CORS (optional)
    log_level: str = "INFO"
    openai_api_key: str = ""
    database_url: str  # Required: Supabase PostgreSQL connection string

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

