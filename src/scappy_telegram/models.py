from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RawTelegramMessage(BaseModel):
    source_channel: str
    message_id: int
    date: datetime = Field(default_factory=utc_now)
    text: str = ""
    urls: list[str] = Field(default_factory=list)
    has_media: bool = False


class PipelineDecision(str, Enum):
    APPROVED = "approved"
    DUPLICATE = "duplicate"
    ERROR = "error"
    IGNORED = "ignored"
    REJECTED = "rejected"


class OfferCandidate(BaseModel):
    source_channel: str
    source_message_id: int
    title: str
    original_text: str
    cleaned_text: str
    links: list[str] = Field(default_factory=list)
    price_text: str | None = None
    previous_price_text: str | None = None
    currency: str | None = None
    canonical_key: str


class ValidationStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    ERROR = "error"


class ValidationResult(BaseModel):
    status: ValidationStatus
    reason: str | None = None
    normalized_price: str | None = None
    product_url: str | None = None


class PublishResult(BaseModel):
    published: bool
    message_id: int | None = None
    reason: str | None = None


class PipelineResult(BaseModel):
    decision: PipelineDecision
    reason: str | None = None
    fingerprint: str | None = None
    title: str | None = None
    published: bool = False
