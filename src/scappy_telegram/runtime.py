from __future__ import annotations

import logging

from scappy_telegram.config import Settings
from scappy_telegram.storage import OfferStore
from scappy_telegram.telegram_ingest import (
    build_telegram_client,
    iter_new_messages,
    iter_recent_messages,
)
from scappy_telegram.worker import OfferPipeline


LOGGER = logging.getLogger(__name__)


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def init_database(settings: Settings) -> None:
    OfferStore(settings.sqlite_path).migrate()


async def login_telegram(settings: Settings) -> None:
    configure_logging(settings.log_level)
    client = build_telegram_client(settings)
    await client.start()
    me = await client.get_me()
    LOGGER.info("Telegram session ready for %s", getattr(me, "username", None) or me.id)
    await client.disconnect()


async def run_service(settings: Settings) -> None:
    configure_logging(settings.log_level)
    pipeline = OfferPipeline(settings)
    client = build_telegram_client(settings)

    await client.start()
    LOGGER.info(
        "Scappy Telegram started: %d source channels, dry_run=%s, validator=%s",
        len(settings.source_channel_list),
        settings.dry_run,
        settings.validator_mode,
    )

    if settings.startup_backfill_limit > 0:
        for source_channel in settings.source_channel_list:
            LOGGER.info(
                "Processing startup backfill for %s, limit=%d",
                source_channel,
                settings.startup_backfill_limit,
            )
            async for message in iter_recent_messages(
                client,
                source_channel,
                settings.startup_backfill_limit,
            ):
                result = await pipeline.process_message(message)
                LOGGER.info(
                    "backfill channel=%s message=%s decision=%s reason=%s title=%s",
                    message.source_channel,
                    message.message_id,
                    result.decision.value,
                    result.reason,
                    result.title,
                )

    LOGGER.info("Listening for new Telegram messages")
    try:
        async for message in iter_new_messages(client, settings.source_channel_list):
            result = await pipeline.process_message(message)
            LOGGER.info(
                "message channel=%s message=%s decision=%s reason=%s title=%s published=%s",
                message.source_channel,
                message.message_id,
                result.decision.value,
                result.reason,
                result.title,
                result.published,
            )
    finally:
        await client.disconnect()
