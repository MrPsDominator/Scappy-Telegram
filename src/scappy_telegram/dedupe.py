from __future__ import annotations

import hashlib

from scappy_telegram.models import OfferCandidate


def candidate_fingerprint(candidate: OfferCandidate) -> str:
    payload = "|".join(
        [
            candidate.canonical_key,
            candidate.price_text or "",
            ",".join(candidate.links),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
