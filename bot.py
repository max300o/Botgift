import asyncio
import html
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

from config import BOT_TOKEN
from api import gift_api, extract_gift_id

logging.basicConfig(level=logging.INFO)

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

    gift_name, gift_number = extract_gift_id(message.text.strip())

    wait = await message.answer("🔍 در حال دریافت اطلاعات...")

    data = await gift_api.get_gift(gift_name, gift_number)

    if not data:
        await wait.edit_text("❌ اطلاعاتی پیدا نشد.")
        return

    gift = data.get("gift", {})
    models = data.get("models", [])
    backdrops = data.get("backdrops", [])
    symbols = data.get("symbols", [])

    text = [f"🎁 <b>{html.escape(gift.get('name', gift_name))}</b>\n"]

    # مدل‌ها
    if models:
        text.append("🎨 <b>Models:</b>")
        for m in models[:5]:
            name = html.escape(str(m.get("name", "-")))
            rarity = m.get("rarity", "-")
            text.append(f"  • {name} — {rarity}%")
        if len(models) > 5:
            text.append(f"  <i>و {len(models) - 5} مدل دیگر...</i>")

    # بک‌دراپ‌ها
    if backdrops:
        text.append("\n🖼 <b>Backdrops:</b>")
        for b in backdrops[:5]:
            name = html.escape(str(b.get("name", "-")))
            rarity = b.get("rarity", "-")
            text.append(f"  • {name} — {rarity}%")
        if len(backdrops) > 5:
            text.append(f"  <i>و {len(backdrops) - 5} بک‌درآپ دیگر...</i>")

    # سیمبل‌ها
    if symbols:
        text.append("\n✨ <b>Symbols:</b>")
        for s in symbols[:5]:
            name = html.escape(str(s.get("name", "-")))
            rarity = s.get("rarity", "-")
            text.append(f"  • {name} — {rarity}%")
        if len(symbols) > 5:
            text.append(f"  <i>و {len(symbols) - 5} سیمبل دیگر...</i>")

    await wait.edit_text("\n".join(text), disable_web_page_preview=True)


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not found in GitHub Secrets.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
