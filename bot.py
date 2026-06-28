import asyncio
import html

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

from config import BOT_TOKEN
from api import gift_api, extract_gift_id

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
        "🎁 <b>Telegram Gift Checker</b>\n\n"
        "لطفاً لینک Gift را ارسال کنید.\n\n"
        "<code>https://t.me/nft/PlushPepe-1234</code>"
    )


@dp.message(F.text)
async def check_gift(message: Message):

    gift_id = extract_gift_id(message.text.strip())

    wait = await message.answer(
        "🔍 در حال دریافت اطلاعات..."
    )

    data = await gift_api.get_gift(gift_id)

    if not data:
        await wait.edit_text(
            "❌ اطلاعاتی پیدا نشد."
        )
        return

    info = data.get("gift", data)

    text = []

    text.append(
        "🎁 <b>Gift Information</b>\n"
    )

    fields = [
        ("Name", "name"),
        ("Number", "number"),
        ("Model", "model"),
        ("Color", "color"),
        ("Backdrop", "backdrop"),
        ("Symbol", "symbol"),
        ("Rarity", "rarity"),
        ("Supply", "supply"),
        ("Floor", "floor"),
        ("Owner", "owner"),
    ]

    for title, key in fields:

        value = info.get(key)

        if value is None:
            continue

        text.append(
            f"<b>{title}:</b> {html.escape(str(value))}"
        )

    sales = info.get("sales") or info.get("last_sales") or []

    if sales:

        text.append(
            "\n🛒 <b>Last Sales</b>"
        )

        for sale in sales[:5]:

            price = sale.get("price", "-")
            date = sale.get("date", "-")
            buyer = sale.get("buyer", "-")

            text.append(
                f"• {price} TON | {date}\n"
                f"👤 {html.escape(str(buyer))}"
            )

========================
⬇️ ادامه را دقیقاً از اینجا بچسبان
========================
    markets = info.get("markets") or []

    if markets:

        text.append(
            "\n🌐 <b>Markets</b>"
        )

        for market in markets:

            name = market.get("name", "Market")
            url = market.get("url", "")

            if url:
                text.append(
                    f'• <a href="{url}">{html.escape(name)}</a>'
                )

    await wait.edit_text(
        "\n".join(text),
        disable_web_page_preview=True
    )


async def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN not found in GitHub Secrets."
        )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
