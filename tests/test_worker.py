from pathlib import Path

import asyncio

from scappy_telegram.config import Settings
from scappy_telegram.models import PipelineDecision, RawTelegramMessage
from scappy_telegram.worker import OfferPipeline


def test_pipeline_rejects_non_offer_and_records_raw_message(tmp_path: Path) -> None:
    settings = Settings(
        telegram_api_id=123,
        telegram_api_hash="hash",
        source_channels="deals",
        database_url=f"sqlite:///{tmp_path / 'scappy.sqlite3'}",
    )
    pipeline = OfferPipeline(settings)
    message = RawTelegramMessage(
        source_channel="deals",
        message_id=1,
        text="Solo comunicazione di servizio",
    )

    result = asyncio.run(pipeline.process_message(message))

    assert result.decision == PipelineDecision.REJECTED
    assert result.reason == "missing_price"


def test_pipeline_marks_repeated_source_message_as_duplicate(tmp_path: Path) -> None:
    settings = Settings(
        telegram_api_id=123,
        telegram_api_hash="hash",
        source_channels="deals",
        database_url=f"sqlite:///{tmp_path / 'scappy.sqlite3'}",
    )
    pipeline = OfferPipeline(settings)
    message = RawTelegramMessage(
        source_channel="deals",
        message_id=1,
        text="SSD 1TB 59 EUR",
    )

    first = asyncio.run(pipeline.process_message(message))
    second = asyncio.run(pipeline.process_message(message))

    assert first.decision == PipelineDecision.APPROVED
    assert second.decision == PipelineDecision.DUPLICATE
    assert second.reason == "source_message_seen"
