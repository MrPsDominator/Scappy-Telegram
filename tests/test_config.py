from scappy_telegram.config import Settings
from scappy_telegram.main import missing_required_settings


def test_source_channel_list_splits_comma_separated_values() -> None:
    settings = Settings(source_channels=" deals_one, deals_two ,, -100123 ")

    assert settings.source_channel_list == ["deals_one", "deals_two", "-100123"]


def test_default_validator_is_local() -> None:
    settings = Settings()

    assert settings.validator_mode == "local"
    assert settings.retention_days == 3


def test_login_command_requires_only_telegram_api_credentials() -> None:
    settings = Settings(
        telegram_api_id=123,
        telegram_api_hash="hash",
        source_channels="",
    )

    assert missing_required_settings(settings, "login") == []


def test_init_db_command_does_not_require_telegram_credentials() -> None:
    assert missing_required_settings(Settings(), "init-db") == []
