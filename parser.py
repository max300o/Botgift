import re

GIFT_PATTERNS = [
    r"https?://t\.me/nft/([A-Za-z0-9_-]+)",
    r"t\.me/nft/([A-Za-z0-9_-]+)",
    r"^([A-Za-z0-9_-]+)$",
]


def extract_gift(text: str) -> str | None:
    if not text:
        return None

    text = text.strip()

    for pattern in GIFT_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def normalize_gift(gift: str) -> str:
    return gift.strip()


def gift_url(gift: str) -> str:
    return f"https://t.me/nft/{gift}"
