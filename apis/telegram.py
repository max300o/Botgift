from apis.base import BaseAPI


class TelegramAPI(BaseAPI):

    BASE = "https://t.me"

    async def get(self, gift: str):

        url = f"{self.BASE}/nft/{gift}"

        html = await self.get_text(url)

        if not html:
            return None

        return {
            "source": "telegram",
            "html": html,
        }


telegram_api = TelegramAPI()
