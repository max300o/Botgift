import asyncio

from apis.telegram import telegram_api
from apis.tonnel import tonnel_api
from apis.mrkt import mrkt_api
from apis.portal import portal_api
from apis.scanner import scanner_api


class APIClient:

    async def fetch(self, gift: str):

        telegram_task = telegram_api.get(gift)
        tonnel_task = tonnel_api.info(gift)
        mrkt_task = mrkt_api.info(gift)
        portal_task = portal_api.info(gift)
        scanner_task = scanner_api.get(gift)

        telegram, tonnel, mrkt, portal, scanner = await asyncio.gather(
            telegram_task,
            tonnel_task,
            mrkt_task,
            portal_task,
            scanner_task,
            return_exceptions=True,
        )

        return {
            "telegram": None if isinstance(telegram, Exception) else telegram,
            "tonnel": None if isinstance(tonnel, Exception) else tonnel,
            "mrkt": None if isinstance(mrkt, Exception) else mrkt,
            "portal": None if isinstance(portal, Exception) else portal,
            "scanner": None if isinstance(scanner, Exception) else scanner,
        }


api = APIClient()
