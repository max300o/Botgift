from apis.base import BaseAPI


class MRKTAPI(BaseAPI):

    BASE = "https://api.mrkt.io"

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
            "source": "mrkt",
            "search": await self.search(gift),
            "floor": await self.floor(gift),
            "sales": await self.sales(gift),
        }


mrkt_api = MRKTAPI()
