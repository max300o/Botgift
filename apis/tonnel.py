from apis.base import BaseAPI


class TonnelAPI(BaseAPI):

    BASE = "https://api.tonnel.network"

    async def search(self, gift: str):

        url = f"{self.BASE}/search?query={gift}"

        return await self.get_json(url)

    async def floor(self, gift: str):

        url = f"{self.BASE}/floor/{gift}"

        return await self.get_json(url)

    async def sales(self, gift: str):

        url = f"{self.BASE}/sales/{gift}"

        return await self.get_json(url)

    async def info(self, gift: str):

        result = {
            "source": "tonnel",
            "search": await self.search(gift),
            "floor": await self.floor(gift),
            "sales": await self.sales(gift),
        }

        return result


tonnel_api = TonnelAPI()
