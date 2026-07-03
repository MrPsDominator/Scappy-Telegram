from scappy_telegram.cleaning import (
    build_offer_candidate,
    extract_previous_price,
    extract_urls,
    normalize_url,
)
from scappy_telegram.models import RawTelegramMessage


def test_extract_urls_strips_trailing_punctuation() -> None:
    assert extract_urls("Link: https://example.com/item?x=1).") == [
        "https://example.com/item?x=1"
    ]


def test_normalize_url_removes_tracking_and_affiliate_params() -> None:
    assert (
        normalize_url(
            "https://EXAMPLE.com/item?utm_source=tg&tag=affiliate&sku=123&fbclid=abc#section"
        )
        == "https://example.com/item?sku=123"
    )


def test_build_offer_candidate_extracts_price_and_clean_url() -> None:
    message = RawTelegramMessage(
        source_channel="deals",
        message_id=10,
        text="Super SSD 1TB\nPrezzo 59,99 EUR\nhttps://shop.example/p?utm_campaign=x&sku=ssd",
    )

    candidate = build_offer_candidate(message)

    assert candidate is not None
    assert candidate.title == "Super SSD 1TB"
    assert candidate.price_text == "59,99 EUR"
    assert candidate.links == ["https://shop.example/p?sku=ssd"]


def test_extract_previous_price_from_common_words() -> None:
    assert extract_previous_price("Ora 59,99 EUR, prima 89,90 EUR") == "89,90 EUR"
