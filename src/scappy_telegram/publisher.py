from __future__ import annotations

import httpx

from scappy_telegram.models import OfferCandidate, PublishResult, ValidationResult


def format_offer_message(candidate: OfferCandidate, validation: ValidationResult) -> str:
    lines = [candidate.title]

    price = validation.normalized_price or candidate.price_text
    if price:
        lines.append(f"Prezzo: {price}")

    if candidate.previous_price_text:
        lines.append(f"Prezzo precedente: {candidate.previous_price_text}")

    url = validation.product_url or (candidate.links[0] if candidate.links else None)
    if url:
        lines.append(url)

    return "\n".join(lines)


class TelegramPublisher:
    def __init__(self, bot_token: str, destination_channel: str) -> None:
        self.bot_token = bot_token
        self.destination_channel = destination_channel

    async def publish(
        self,
        candidate: OfferCandidate,
        validation: ValidationResult,
    ) -> PublishResult:
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.destination_channel,
            "text": format_offer_message(candidate, validation),
            "disable_web_page_preview": False,
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            return PublishResult(
                published=False,
                reason=f"telegram_http_error_{exc.response.status_code}",
            )
        except httpx.RequestError as exc:
            return PublishResult(
                published=False,
                reason=f"telegram_request_error_{exc.__class__.__name__}",
            )

        data = response.json()
        message_id = data.get("result", {}).get("message_id")
        return PublishResult(published=True, message_id=message_id)
