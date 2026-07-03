import anyio

from scappy_telegram.models import OfferCandidate, ValidationStatus
from scappy_telegram.validator import LocalRuleValidator


def test_local_validator_rejects_messages_without_price() -> None:
    candidate = OfferCandidate(
        source_channel="news",
        source_message_id=1,
        title="Messaggio informativo",
        original_text="Nessuna offerta qui",
        cleaned_text="Nessuna offerta qui",
        links=[],
        canonical_key="news|messaggio informativo||",
    )

    result = anyio.run(LocalRuleValidator().validate, candidate)

    assert result.status == ValidationStatus.REJECTED
    assert result.reason == "missing_price"


def test_local_validator_approves_candidate_with_price() -> None:
    candidate = OfferCandidate(
        source_channel="deals",
        source_message_id=2,
        title="SSD 1TB",
        original_text="SSD 1TB 59 EUR",
        cleaned_text="SSD 1TB 59 EUR",
        links=["https://shop.example/ssd"],
        price_text="59 EUR",
        canonical_key="deals|ssd 1tb|59 EUR|https://shop.example/ssd",
    )

    result = anyio.run(LocalRuleValidator().validate, candidate)

    assert result.status == ValidationStatus.APPROVED
    assert result.normalized_price == "59 EUR"
