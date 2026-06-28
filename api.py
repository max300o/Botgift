import aiohttp
from config import API_BASE, HEADERS


class GiftAPI:

    def __init__(self):
        self.base = API_BASE

    async def request(self, endpoint: str):
        url = f"{self.base}{endpoint}"

        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url, timeout=30) as resp:

                if resp.status != 200:
                    return None

                try:
                    return await resp.json()
                except:
                    return None

    async def get_gift(self, gift_id: str):
        return await self.request(f"/gift/{gift_id}")

    async def get_backdrops(self):
        return await self.request("/backdrops")

    async def get_models(self):
        return await self.request("/models")

    async def get_symbols(self):
        return await self.request("/symbols")

    async def get_colors(self):
        return await self.request("/colors")


gift_api = GiftAPI()


def extract_gift_id(text: str):

    text = text.strip()

    if "https://t.me/nft/" in text:
        return text.split("/")[-1]

    if "t.me/nft/" in text:
        return text.split("/")[-1]

    return text
