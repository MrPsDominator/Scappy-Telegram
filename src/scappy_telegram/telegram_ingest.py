from __future__ import annotations

from collections.abc import AsyncIterator

from telethon import TelegramClient

from scappy_telegram.config import Settings
from scappy_telegram.models import RawTelegramMessage


def build_telegram_client(settings: Settings) -> TelegramClient:
    if settings.telegram_api_id is None or settings.telegram_api_hash is None:
        raise ValueError("Telegram API credentials are required.")

    return TelegramClient(
        settings.telegram_session_path,
        settings.telegram_api_id,
        settings.telegram_api_hash,
    )


async def iter_recent_messages(
    client: TelegramClient,
    source_channel: str,
    limit: int = 50,
) -> AsyncIterator[RawTelegramMessage]:
    async for message in client.iter_messages(source_channel, limit=limit):
        text = message.message or ""
        yield RawTelegramMessage(
            source_channel=source_channel,
            message_id=message.id,
            date=message.date,
            text=text,
            has_media=bool(message.media),
        )
