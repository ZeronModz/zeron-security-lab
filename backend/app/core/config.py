from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "zeron-security-lab"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "info"

    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1

    database_url: str = "sqlite+aiosqlite:///./zeron_security.db"
    redis_url: str = "redis://localhost:6379/0"

    api_key: str = "API_KEY_CHANGE_ME"
    jwt_secret_key: str = "change-this-to-a-random-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    allowed_hosts: list[str] = ["*"]
    rate_limit_per_minute: int = 60
    max_request_size: int = 10485760
    request_timeout: int = 30

    allowed_targets: list[str] = []
    blocked_networks: str = "127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"

    browser_enabled: bool = True
    browser_timeout: int = 30000
    screenshot_max_width: int = 1920
    screenshot_max_height: int = 1080

    cloudflare_enabled: bool = True
    cloudflare_timeout: int = 60

    recaptcha_enabled: bool = True
    recaptcha_timeout: int = 30

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
