from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_api_id: int | None = None
    telegram_api_hash: str | None = None
    telegram_session_path: str = "/app/data/telegram.session"
    source_channels: str = ""
    telegram_bot_token: str | None = None
    destination_channel: str | None = None
    validator_mode: Literal["local", "http"] = "local"
    validator_url: str | None = None
    validator_timeout_seconds: float = 10.0
    retention_days: int = 3
    startup_backfill_limit: int = 0
    database_url: str = Field(default="sqlite:////app/data/scappy.sqlite3")
    dry_run: bool = True
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def source_channel_list(self) -> list[str]:
        return [channel.strip() for channel in self.source_channels.split(",") if channel.strip()]

    @property
    def sqlite_path(self) -> str:
        if not self.database_url.startswith("sqlite:///"):
            raise ValueError("Only sqlite:/// database URLs are supported in the initial scaffold.")
        return self.database_url.removeprefix("sqlite:///")
