from pathlib import Path

from scappy_telegram.models import PipelineDecision, RawTelegramMessage
from scappy_telegram.storage import OfferStore


def test_store_records_raw_message_and_decision(tmp_path: Path) -> None:
    store = OfferStore(str(tmp_path / "scappy.sqlite3"))
    store.migrate()
    message = RawTelegramMessage(
        source_channel="deals",
        message_id=123,
        text="Informazione senza prezzo",
    )

    store.record_raw_message(message)
    store.update_raw_message_decision(message, PipelineDecision.IGNORED, "no_candidate")

    assert store.has_source_message("deals", 123)
