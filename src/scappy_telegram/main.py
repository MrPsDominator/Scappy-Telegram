from scappy_telegram.config import Settings


def missing_required_settings(settings: Settings) -> list[str]:
    missing = []

    if not settings.telegram_api_id:
        missing.append("TELEGRAM_API_ID")
    if not settings.telegram_api_hash:
        missing.append("TELEGRAM_API_HASH")
    if not settings.source_channel_list:
        missing.append("SOURCE_CHANNELS")
    if settings.validator_mode == "http" and not settings.validator_url:
        missing.append("VALIDATOR_URL")
    if not settings.dry_run:
        if not settings.telegram_bot_token:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not settings.destination_channel:
            missing.append("DESTINATION_CHANNEL")

    return missing


def main() -> None:
    settings = Settings()
    missing = missing_required_settings(settings)

    if missing:
        missing_values = ", ".join(missing)
        raise SystemExit(f"Missing required configuration: {missing_values}")

    raise SystemExit("Scappy Telegram scaffold is configured, but the worker is not implemented yet.")
