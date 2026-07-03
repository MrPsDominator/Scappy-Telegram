from __future__ import annotations

import httpx

from scappy_telegram.config import Settings
from scappy_telegram.models import OfferCandidate, ValidationResult, ValidationStatus


class LocalRuleValidator:
    async def validate(self, candidate: OfferCandidate) -> ValidationResult:
        if not candidate.price_text:
            return ValidationResult(
                status=ValidationStatus.REJECTED,
                reason="missing_price",
            )
        if not candidate.title or candidate.title == "Offerta senza titolo":
            return ValidationResult(
                status=ValidationStatus.REJECTED,
                reason="missing_product_title",
            )

        return ValidationResult(
            status=ValidationStatus.APPROVED,
            reason="local_rules_price_detected",
            normalized_price=candidate.price_text,
            product_url=candidate.links[0] if candidate.links else None,
        )


class HttpValidatorClient:
    def __init__(self, url: str, timeout_seconds: float = 10.0) -> None:
        self.url = url
        self.timeout_seconds = timeout_seconds

    async def validate(self, candidate: OfferCandidate) -> ValidationResult:
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(
                    self.url,
                    json=candidate.model_dump(mode="json"),
                )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            return ValidationResult(status=ValidationStatus.ERROR, reason=str(exc))

        payload = response.json()
        status = payload.get("status")
        if not status:
            status = ValidationStatus.APPROVED if payload.get("approved") else ValidationStatus.REJECTED

        try:
            validation_status = ValidationStatus(status)
        except ValueError:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                reason=f"Unknown validator status: {status}",
            )

        return ValidationResult(
            status=validation_status,
            reason=payload.get("reason"),
            normalized_price=payload.get("normalized_price"),
            product_url=payload.get("product_url"),
        )


def build_validator(settings: Settings) -> LocalRuleValidator | HttpValidatorClient:
    if settings.validator_mode == "local":
        return LocalRuleValidator()
    if not settings.validator_url:
        raise ValueError("VALIDATOR_URL is required when VALIDATOR_MODE=http.")
    return HttpValidatorClient(settings.validator_url, settings.validator_timeout_seconds)
