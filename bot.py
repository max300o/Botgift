import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import F

from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from parser import extract_gift
from formatter import build_message
from apis.client import api
from cache import cache

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


@dp.message(F.text == "/start")
async def start(message: Message):

    await message.answer(
        "🎁 GiftHunter Pro\n\n"
        "لینک Gift را ارسال کنید."
    )


@dp.message(F.text)
async def gift(message: Message):

    gift = extract_gift(message.text)

    if not gift:
        await message.answer(
            "❌ لینک یا شناسه Gift معتبر نیست."
        )
        return

    cached = cache.get(gift)

    if cached:
        await message.answer(
            cached
        )
        return

    wait = await message.answer(
        "🔍 درحال جستجو..."
    )

    result = await api.fetch(gift)

    data = {}

    data["name"] = gift

    scanner = result.get("scanner")

    if scanner:

        if scanner.get("title"):
            data["name"] = scanner["title"]

        if scanner.get("description"):
            data["description"] = scanner["description"]

    tonnel = result.get("tonnel")

    if tonnel:

        floor = tonnel.get("floor")

        if floor:
            data["tonnel"] = floor

    mrkt = result.get("mrkt")

    if mrkt:

        floor = mrkt.get("floor")

        if floor:
            data["mrkt"] = floor

    portal = result.get("portal")

    if portal:

        floor = portal.get("floor")

        if floor:
            data["portal"] = floor

    text = build_message(data)

    cache.set(
        gift,
        text
    )

# >>> ادامه فایل از خط بعدی <<<
    await wait.edit_text(
        text
    )


async def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing."
        )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
