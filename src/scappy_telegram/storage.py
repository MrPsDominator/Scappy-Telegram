from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scappy_telegram.models import (
    OfferCandidate,
    PipelineDecision,
    PublishResult,
    RawTelegramMessage,
    ValidationResult,
)


class OfferStore:
    def __init__(self, sqlite_path: str) -> None:
        self.sqlite_path = sqlite_path

    def connect(self) -> sqlite3.Connection:
        path = Path(self.sqlite_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(path)
        connection.row_factory = sqlite3.Row
        return connection

    def migrate(self) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS raw_messages (
                    source_channel TEXT NOT NULL,
                    source_message_id INTEGER NOT NULL,
                    message_date TEXT NOT NULL,
                    text TEXT NOT NULL,
                    urls_json TEXT NOT NULL,
                    has_media INTEGER NOT NULL,
                    processing_status TEXT,
                    processing_reason TEXT,
                    fingerprint TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (source_channel, source_message_id)
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS offers (
                    fingerprint TEXT PRIMARY KEY,
                    source_channel TEXT NOT NULL,
                    source_message_id INTEGER NOT NULL,
                    candidate_json TEXT NOT NULL,
                    validation_json TEXT,
                    publish_json TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_offers_source_message
                ON offers (source_channel, source_message_id)
                """
            )

    def has_source_message(self, source_channel: str, source_message_id: int) -> bool:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT 1 FROM raw_messages
                WHERE source_channel = ? AND source_message_id = ?
                """,
                (source_channel, source_message_id),
            ).fetchone()
        return row is not None

    def has_fingerprint(self, fingerprint: str) -> bool:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM offers WHERE fingerprint = ?",
                (fingerprint,),
            ).fetchone()
        return row is not None

    def record_raw_message(self, message: RawTelegramMessage) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO raw_messages (
                    source_channel,
                    source_message_id,
                    message_date,
                    text,
                    urls_json,
                    has_media
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    message.source_channel,
                    message.message_id,
                    message.date.isoformat(),
                    message.text,
                    json.dumps(message.urls, ensure_ascii=False),
                    int(message.has_media),
                ),
            )

    def update_raw_message_decision(
        self,
        message: RawTelegramMessage,
        decision: PipelineDecision,
        reason: str | None = None,
        fingerprint: str | None = None,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE raw_messages
                SET processing_status = ?,
                    processing_reason = ?,
                    fingerprint = ?
                WHERE source_channel = ? AND source_message_id = ?
                """,
                (
                    decision.value,
                    reason,
                    fingerprint,
                    message.source_channel,
                    message.message_id,
                ),
            )

    def record_candidate(
        self,
        fingerprint: str,
        candidate: OfferCandidate,
        validation: ValidationResult | None = None,
        publish: PublishResult | None = None,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO offers (
                    fingerprint,
                    source_channel,
                    source_message_id,
                    candidate_json,
                    validation_json,
                    publish_json
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    fingerprint,
                    candidate.source_channel,
                    candidate.source_message_id,
                    candidate.model_dump_json(),
                    validation.model_dump_json() if validation else None,
                    publish.model_dump_json() if publish else None,
                ),
            )

    def delete_older_than(self, days: int) -> int:
        if days <= 0:
            return 0

        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        cutoff_text = cutoff.strftime("%Y-%m-%d %H:%M:%S")
        with self.connect() as connection:
            raw_cursor = connection.execute(
                "DELETE FROM raw_messages WHERE created_at < ?",
                (cutoff_text,),
            )
            offer_cursor = connection.execute(
                "DELETE FROM offers WHERE created_at < ?",
                (cutoff_text,),
            )
        return raw_cursor.rowcount + offer_cursor.rowcount


def dumps_pretty(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
