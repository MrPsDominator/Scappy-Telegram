from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

from scappy_telegram.config import Settings
from scappy_telegram.models import RawTelegramMessage

ChannelRef = str | int


def build_telegram_client(settings: Settings) -> TelegramClient:
    if settings.telegram_api_id is None or settings.telegram_api_hash is None:
        raise ValueError("Telegram API credentials are required.")

    return TelegramClient(
        settings.telegram_session_path,
        settings.telegram_api_id,
        settings.telegram_api_hash,
    )


def parse_channel_ref(value: str) -> ChannelRef:
    stripped = value.strip()
    if stripped.lstrip("-").isdigit():
        return int(stripped)
    return stripped


def raw_message_from_telethon(source_channel: str, message: Message) -> RawTelegramMessage:
    return RawTelegramMessage(
        source_channel=source_channel,
        message_id=message.id,
        date=message.date,
        text=message.message or "",
        has_media=bool(message.media),
    )


async def iter_recent_messages(
    client: TelegramClient,
    source_channel: str,
    limit: int = 50,
) -> AsyncIterator[RawTelegramMessage]:
    async for message in client.iter_messages(parse_channel_ref(source_channel), limit=limit):
        yield raw_message_from_telethon(source_channel, message)


async def iter_new_messages(
    client: TelegramClient,
    source_channels: list[str],
) -> AsyncIterator[RawTelegramMessage]:
    queue: asyncio.Queue[RawTelegramMessage] = asyncio.Queue()
    event_builder = events.NewMessage(chats=[parse_channel_ref(channel) for channel in source_channels])

    async def handler(event: events.NewMessage.Event) -> None:
        chat = await event.get_chat()
        source_channel = getattr(chat, "username", None) or str(event.chat_id)
        await queue.put(raw_message_from_telethon(source_channel, event.message))

    client.add_event_handler(handler, event_builder)
    try:
        while True:
            yield await queue.get()
    finally:
        client.remove_event_handler(handler)
