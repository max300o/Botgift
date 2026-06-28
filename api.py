import aiohttp
from aiohttp import ClientTimeout
from config import API_BASE, HEADERS
import logging
import re

logger = logging.getLogger(__name__)


class GiftAPI:

    def __init__(self):
        self.base = API_BASE

    async def request(self, endpoint: str):
        url = f"{self.base}{endpoint}"
        timeout = ClientTimeout(total=30)

        try:
            async with aiohttp.ClientSession(headers=HEADERS, timeout=timeout) as session:
                async with session.get(url) as resp:
                    logger.info(f"GET {url} -> {resp.status}")

                    if resp.status != 200:
                        text = await resp.text()
                        logger.error(f"Error response: {text[:200]}")
                        return None

                    try:
                        return await resp.json(content_type=None)
                    except Exception as e:
                        logger.error(f"JSON parse error: {e}")
                        return None

        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None

    async def get_gift(self, gift_name: str, gift_number: str = None):
        # اول با slug کامل تست می‌کنیم
        data = await self.request(f"/gift/{gift_name}")
        if data:
            return data
        # اگر نشد، با عدد تست می‌کنیم
        if gift_number:
            data = await self.request(f"/gift/{gift_number}")
            if data:
                return data
        return None


gift_api = GiftAPI()


def extract_gift_id(text: str):
    """
    از لینک t.me/nft/CloverPin-70441
    اسم gift و عدد رو جدا می‌کنه
    returns: (gift_name, gift_number) مثل ("CloverPin", "70441")
    """
    text = text.strip()

    slug = text
    for prefix in ["https://t.me/nft/", "http://t.me/nft/", "t.me/nft/"]:
        if prefix in text:
            slug = text.split(prefix)[-1]
            break

    # جدا کردن اسم و عدد: CloverPin-70441 -> ("CloverPin", "70441")
    match = re.match(r'^([A-Za-z]+(?:[A-Z][a-z]*)*)-(\d+)$', slug)
    if match:
        return match.group(1), match.group(2)

    return slug, None
