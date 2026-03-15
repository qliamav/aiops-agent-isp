from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str

    splynx_base_url: str
    splynx_api_key: str

    genieacs_base_url: str
    genieacs_username: str
    genieacs_password: str

    log_level: str = "INFO"
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60


settings = Settings()
