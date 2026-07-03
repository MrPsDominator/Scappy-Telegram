from scappy_telegram.config import Settings


def test_source_channel_list_splits_comma_separated_values() -> None:
    settings = Settings(source_channels=" deals_one, deals_two ,, -100123 ")

    assert settings.source_channel_list == ["deals_one", "deals_two", "-100123"]


def test_default_validator_is_local() -> None:
    settings = Settings()

    assert settings.validator_mode == "local"
    assert settings.retention_days == 3
