from apis.base import BaseAPI


class PortalAPI(BaseAPI):

    BASE = "https://api.portal.market"

    async def search(self, gift: str):

        url = f"{self.BASE}/search?q={gift}"

        return await self.get_json(url)

    async def floor(self, gift: str):

        url = f"{self.BASE}/floor/{gift}"

        return await self.get_json(url)

    async def sales(self, gift: str):

        url = f"{self.BASE}/sales/{gift}"

        return await self.get_json(url)

    async def info(self, gift: str):

        return {
            "source": "portal",
            "search": await self.search(gift),
            "floor": await self.floor(gift),
            "sales": await self.sales(gift),
        }


portal_api = PortalAPI()
