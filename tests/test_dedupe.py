from scappy_telegram.dedupe import candidate_fingerprint
from scappy_telegram.models import OfferCandidate


def test_candidate_fingerprint_is_stable() -> None:
    candidate = OfferCandidate(
        source_channel="deals",
        source_message_id=1,
        title="SSD",
        original_text="SSD 59 EUR",
        cleaned_text="SSD 59 EUR",
        links=["https://shop.example/ssd"],
        price_text="59 EUR",
        previous_price_text=None,
        currency="EUR",
        canonical_key="deals|ssd|59 EUR|https://shop.example/ssd",
    )

    assert candidate_fingerprint(candidate) == candidate_fingerprint(candidate)
