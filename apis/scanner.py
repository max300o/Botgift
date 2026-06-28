from bs4 import BeautifulSoup

from apis.base import BaseAPI


class ScannerAPI(BaseAPI):

    BASE = "https://giftscan.bot"

    async def get(self, gift: str):

        url = f"{self.BASE}/gift/{gift}"

        html = await self.get_text(url)

        if not html:
            return None

        soup = BeautifulSoup(html, "lxml")

        return {
            "source": "scanner",
            "html": html,
            "title": soup.title.text.strip() if soup.title else None,
            "image": self._image(soup),
            "description": self._description(soup),
        }

    def _image(self, soup):

        tag = soup.find("meta", property="og:image")

        if tag:
            return tag.get("content")

        return None

    def _description(self, soup):

        tag = soup.find("meta", property="og:description")

        if tag:
            return tag.get("content")

        return None


scanner_api = ScannerAPI()
