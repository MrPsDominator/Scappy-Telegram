from __future__ import annotations

from scappy_telegram.cleaning import build_offer_candidate
from scappy_telegram.config import Settings
from scappy_telegram.dedupe import candidate_fingerprint
from scappy_telegram.models import RawTelegramMessage, ValidationStatus
from scappy_telegram.publisher import TelegramPublisher
from scappy_telegram.storage import OfferStore
from scappy_telegram.validator import build_validator


class OfferPipeline:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.store = OfferStore(settings.sqlite_path)
        self.validator = build_validator(settings)
        self.publisher = (
            TelegramPublisher(settings.telegram_bot_token, settings.destination_channel)
            if settings.telegram_bot_token and settings.destination_channel
            else None
        )

    async def process_message(self, message: RawTelegramMessage) -> bool:
        candidate = build_offer_candidate(message)
        if candidate is None:
            return False

        fingerprint = candidate_fingerprint(candidate)
        if self.store.has_fingerprint(fingerprint):
            return False

        self.store.delete_older_than(self.settings.retention_days)
        validation = await self.validator.validate(candidate)
        publish = None

        if validation.status == ValidationStatus.APPROVED and not self.settings.dry_run:
            if self.publisher is None:
                raise ValueError("Publisher is not configured.")
            publish = await self.publisher.publish(candidate, validation)

        self.store.record_candidate(fingerprint, candidate, validation, publish)
        return validation.status == ValidationStatus.APPROVED
