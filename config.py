import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

REQUEST_TIMEOUT = 20

CACHE_TTL = 60

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0 Safari/537.36"
)

MAX_SALES = 10

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json,text/html,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}
