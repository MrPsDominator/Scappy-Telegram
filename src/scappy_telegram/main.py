import argparse
import asyncio

from scappy_telegram.config import Settings
from scappy_telegram.runtime import init_database, login_telegram, run_service


def missing_required_settings(settings: Settings, command: str = "run") -> list[str]:
    missing = []

    if command == "init-db":
        return missing

    if not settings.telegram_api_id:
        missing.append("TELEGRAM_API_ID")
    if not settings.telegram_api_hash:
        missing.append("TELEGRAM_API_HASH")
    if command == "login":
        return missing

    if command == "run" and not settings.source_channel_list:
        missing.append("SOURCE_CHANNELS")
    if settings.validator_mode == "http" and not settings.validator_url:
        missing.append("VALIDATOR_URL")
    if not settings.dry_run:
        if not settings.telegram_bot_token:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not settings.destination_channel:
            missing.append("DESTINATION_CHANNEL")

    return missing


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="scappy-telegram")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("run", help="Run the Telegram listener and processing pipeline.")
    subparsers.add_parser("login", help="Create or refresh the Telethon session.")
    subparsers.add_parser("init-db", help="Create or update the SQLite schema.")
    subparsers.add_parser("check-config", help="Validate required configuration.")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    command = args.command or "run"
    settings = Settings()
    missing = missing_required_settings(settings, command)

    if missing:
        missing_values = ", ".join(missing)
        raise SystemExit(f"Missing required configuration: {missing_values}")

    if command == "check-config":
        print("Configuration OK")
        return
    if command == "init-db":
        init_database(settings)
        print(f"Database ready: {settings.sqlite_path}")
        return
    if command == "login":
        asyncio.run(login_telegram(settings))
        return
    if command == "run":
        asyncio.run(run_service(settings))
        return

    parser.error(f"Unknown command: {command}")
