import os
import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ["BOT_TOKEN"]
API_BASE = "https://api.changes.tg"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\nربات گیفت‌یاب فعال است.\n\nاستفاده: /gift <نام گیفت>"
    )


async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ لطفاً نام گیفت را وارد کنید.\nمثال: /gift rose")
        return

    gift_name = " ".join(context.args)
    await update.message.reply_text(f"🔍 در حال جستجوی «{gift_name}»...")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(f"{API_BASE}/gift/{gift_name}")

        if res.status_code == 200:
            data = res.json()
            name = data.get("name", gift_name)
            rarity = data.get("rarity", "نامشخص")
            await update.message.reply_text(
                f"🎁 گیفت پیدا شد!\n\n"
                f"نام: {name}\n"
                f"نادر بودن: {rarity}%"
            )
        elif res.status_code == 404:
            await update.message.reply_text(f"❌ گیفت «{gift_name}» پیدا نشد.")
        else:
            await update.message.reply_text("⚠️ خطا در دریافت اطلاعات. دوباره تلاش کنید.")

    except httpx.TimeoutException:
        await update.message.reply_text("⏱ سرور پاسخ نداد. دوباره تلاش کنید.")
    except Exception as e:
        logger.error(f"Error in gift command: {e}")
        await update.message.reply_text("❌ خطایی رخ داد.")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gift", gift))
    logger.info("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
