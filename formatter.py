from html import escape


def line(title: str, value) -> str:
    if value in (None, "", [], {}):
        return ""

    return f"<b>{escape(title)}:</b> {escape(str(value))}"


def section(title: str) -> str:
    return f"\n<b>{escape(title)}</b>"


def market(name: str, price, cheapest=False) -> str:
    icon = "🏆 " if cheapest else "• "

    if price in (None, ""):
        price = "-"

    return f"{icon}{escape(name)}: {escape(str(price))}"


def sale(price, date=None, buyer=None) -> str:
    text = f"• {price}"

    if date:
        text += f" | {date}"

    if buyer:
        text += f" | {buyer}"

    return text


def build_message(data: dict) -> str:

    text = []

    text.append("🎁 <b>Gift Information</b>\n")

    fields = [
        ("Name", data.get("name")),
        ("Number", data.get("number")),
        ("Emoji", data.get("emoji")),
        ("Model", data.get("model")),
        ("Color", data.get("color")),
        ("Backdrop", data.get("backdrop")),
        ("Symbol", data.get("symbol")),
        ("Rarity", data.get("rarity")),
        ("Owner", data.get("owner")),
    ]

    for title, value in fields:
        row = line(title, value)
        if row:
            text.append(row)

    return "\n".join(text)
