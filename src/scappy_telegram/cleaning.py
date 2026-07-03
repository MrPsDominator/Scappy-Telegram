from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from scappy_telegram.models import OfferCandidate, RawTelegramMessage


URL_RE = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
PRICE_RE = re.compile(
    r"(?P<prefix>EUR|USD|GBP|€|\$|£)\s*(?P<prefix_amount>\d+(?:[.,]\d{1,2})?)"
    r"|(?P<suffix_amount>\d+(?:[.,]\d{1,2})?)\s*(?P<suffix>EUR|USD|GBP|€|\$|£)",
    re.IGNORECASE,
)
PREVIOUS_PRICE_RE = re.compile(
    r"(?:prima|precedente|prezzo\s+precedente|anziche|anziché|listino|da)\D{0,20}"
    r"(?P<amount>\d+(?:[.,]\d{1,2})?)\s*(?P<currency>EUR|USD|GBP|€|\$|£)",
    re.IGNORECASE,
)

TRACKING_PARAMS = {
    "ascsubtag",
    "camp",
    "campaign",
    "fbclid",
    "gclid",
    "igshid",
    "mc_cid",
    "mc_eid",
    "ref",
    "ref_",
    "tag",
}

AFFILIATE_PARAM_MARKERS = (
    "aff",
    "affiliate",
    "campaign",
    "clickid",
    "partner",
    "referral",
    "tracking",
)

TRAILING_URL_PUNCTUATION = ".,;:!?)\"]}"


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    for match in URL_RE.finditer(text):
        urls.append(match.group(0).rstrip(TRAILING_URL_PUNCTUATION))
    return urls


def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = []

    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith("utm_"):
            continue
        if lowered in TRACKING_PARAMS:
            continue
        if any(marker in lowered for marker in AFFILIATE_PARAM_MARKERS):
            continue
        query.append((key, value))

    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path,
            urlencode(query, doseq=True),
            "",
        )
    )


def clean_text(text: str) -> str:
    without_urls = URL_RE.sub("", text)
    lines = []
    for raw_line in without_urls.splitlines():
        line = " ".join(raw_line.strip().split())
        if line:
            lines.append(line)
    return "\n".join(lines)


def extract_price(text: str) -> tuple[str | None, str | None]:
    match = PRICE_RE.search(text)
    if not match:
        return None, None

    if match.group("prefix_amount"):
        currency = match.group("prefix")
        amount = match.group("prefix_amount")
    else:
        currency = match.group("suffix")
        amount = match.group("suffix_amount")

    return f"{amount} {currency}", currency


def extract_previous_price(text: str) -> str | None:
    match = PREVIOUS_PRICE_RE.search(text)
    if not match:
        return None
    return f"{match.group('amount')} {match.group('currency')}"


def build_offer_candidate(message: RawTelegramMessage) -> OfferCandidate | None:
    urls = message.urls or extract_urls(message.text)
    normalized_urls = [normalize_url(url) for url in urls]
    cleaned = clean_text(message.text)
    title = next((line for line in cleaned.splitlines() if line), "").strip()

    if not title and not normalized_urls:
        return None

    price_text, currency = extract_price(message.text)
    previous_price_text = extract_previous_price(message.text)
    canonical_key = "|".join(
        [
            message.source_channel.lower(),
            title.lower(),
            price_text or "",
            normalized_urls[0] if normalized_urls else "",
        ]
    )

    return OfferCandidate(
        source_channel=message.source_channel,
        source_message_id=message.message_id,
        title=title or "Offerta senza titolo",
        original_text=message.text,
        cleaned_text=cleaned,
        links=normalized_urls,
        price_text=price_text,
        previous_price_text=previous_price_text,
        currency=currency,
        canonical_key=canonical_key,
    )
