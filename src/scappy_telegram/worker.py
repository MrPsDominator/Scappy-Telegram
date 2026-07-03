from __future__ import annotations

from scappy_telegram.cleaning import build_offer_candidate
from scappy_telegram.config import Settings
from scappy_telegram.dedupe import candidate_fingerprint
from scappy_telegram.models import (
    PipelineDecision,
    PipelineResult,
    RawTelegramMessage,
    ValidationStatus,
)
from scappy_telegram.publisher import TelegramPublisher
from scappy_telegram.storage import OfferStore
from scappy_telegram.validator import build_validator


class OfferPipeline:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.store = OfferStore(settings.sqlite_path)
        self.store.migrate()
        self.validator = build_validator(settings)
        self.publisher = (
            TelegramPublisher(settings.telegram_bot_token, settings.destination_channel)
            if settings.telegram_bot_token and settings.destination_channel
            else None
        )

    async def process_message(self, message: RawTelegramMessage) -> PipelineResult:
        if self.store.has_source_message(message.source_channel, message.message_id):
            return PipelineResult(decision=PipelineDecision.DUPLICATE, reason="source_message_seen")

        self.store.record_raw_message(message)
        candidate = build_offer_candidate(message)
        if candidate is None:
            self.store.update_raw_message_decision(
                message,
                PipelineDecision.IGNORED,
                "no_candidate",
            )
            return PipelineResult(decision=PipelineDecision.IGNORED, reason="no_candidate")

        fingerprint = candidate_fingerprint(candidate)
        if self.store.has_fingerprint(fingerprint):
            self.store.update_raw_message_decision(
                message,
                PipelineDecision.DUPLICATE,
                "fingerprint_seen",
                fingerprint,
            )
            return PipelineResult(
                decision=PipelineDecision.DUPLICATE,
                reason="fingerprint_seen",
                fingerprint=fingerprint,
                title=candidate.title,
            )

        self.store.delete_older_than(self.settings.retention_days)
        validation = await self.validator.validate(candidate)
        publish = None

        if validation.status == ValidationStatus.APPROVED and not self.settings.dry_run:
            if self.publisher is None:
                raise ValueError("Publisher is not configured.")
            publish = await self.publisher.publish(candidate, validation)

        self.store.record_candidate(fingerprint, candidate, validation, publish)
        decision = (
            PipelineDecision.APPROVED
            if validation.status == ValidationStatus.APPROVED
            else PipelineDecision.REJECTED
            if validation.status == ValidationStatus.REJECTED
            else PipelineDecision.ERROR
        )
        self.store.update_raw_message_decision(
            message,
            decision,
            validation.reason,
            fingerprint,
        )
        return PipelineResult(
            decision=decision,
            reason=validation.reason,
            fingerprint=fingerprint,
            title=candidate.title,
            published=bool(publish and publish.published),
        )
