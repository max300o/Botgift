import aiohttp

from config import (
    REQUEST_TIMEOUT,
    HEADERS,
)


class BaseAPI:

    async def get_json(self, url, headers=None):

        headers = headers or HEADERS

        timeout = aiohttp.ClientTimeout(
            total=REQUEST_TIMEOUT
        )

        async with aiohttp.ClientSession(
            timeout=timeout,
            headers=headers
        ) as session:

            async with session.get(url) as response:

                if response.status != 200:
                    return None

                try:
                    return await response.json()

                except Exception:
                    return None

    async def get_text(self, url, headers=None):

        headers = headers or HEADERS

        timeout = aiohttp.ClientTimeout(
            total=REQUEST_TIMEOUT
        )

        async with aiohttp.ClientSession(
            timeout=timeout,
            headers=headers
        ) as session:

            async with session.get(url) as response:

                if response.status != 200:
                    return None

                return await response.text()
