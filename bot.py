import os
import asyncio
import requests
import yfinance as yf
from telegram import Bot
from datetime import datetime
import pytz
import schedule
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── ENV ──────────────────────────────────────────────────────────────────────
TOKEN            = os.getenv("BOT_TOKEN")
CHAT_ID          = int(os.getenv("CHAT_ID"))
MOM_CHAT_ID      = int(os.getenv("MOM_CHAT_ID"))
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
NEWS_API_KEY     = os.getenv("NEWS_API_KEY")

RECIPIENTS = [CHAT_ID, MOM_CHAT_ID]

# ── WATCHLIST ─────────────────────────────────────────────────────────────────
STOCKS = ["AAPL", "TSLA", "SPY", "NVDA", "META", "BBCA.JK", "TLKM.JK", "BBRI.JK"]


# ── STOCK DATA ────────────────────────────────────────────────────────────────
def get_stock_price(symbol: str) -> str:
    try:
        info = yf.Ticker(symbol).fast_info
        price = info.last_price
        prev  = info.previous_close
        change = ((price - prev) / prev) * 100
        emoji = "📈" if change >= 0 else "📉"

        if symbol.endswith(".JK"):
            return f"{emoji} {symbol}: Rp {price:,.0f} ({change:+.2f}%)"
        return f"{emoji} {symbol}: ${price:.2f} ({change:+.2f}%)"
    except Exception as e:
        return f"⚠️ {symbol}: data unavailable ({e})"


def get_stock_news(symbol: str) -> str:
    try:
        news = yf.Ticker(symbol).news
        if news:
            return f"📰 {symbol}: {news[0]['content']['title']}"
    except Exception:
        pass
    return ""


# ── MARKET STATUS ─────────────────────────────────────────────────────────────
def get_market_status() -> str:
    now_est = datetime.now(pytz.timezone("US/Eastern"))
    now_wib = datetime.now(pytz.timezone("Asia/Jakarta"))

    us_open  = now_est.weekday() < 5 and (9, 30) <= (now_est.hour, now_est.minute) <= (16, 0)
    idx_open = now_wib.weekday() < 5 and (9, 0)  <= (now_wib.hour, now_wib.minute) <= (15, 30)

    return (
        f"🇺🇸 US Market: {'🟢 Open' if us_open else '🔴 Closed'}\n"
        f"🇮🇩 IDX: {'🟢 Open' if idx_open else '🔴 Closed'}"
    )


# ── FX RATE ───────────────────────────────────────────────────────────────────
def get_usd_idr() -> str:
    try:
        rate = yf.Ticker("USDIDR=X").fast_info.last_price
        return f"💱 USD/IDR: Rp {rate:,.0f}"
    except Exception:
        return "💱 USD/IDR: unavailable"


# ── NEWS ──────────────────────────────────────────────────────────────────────
def get_top_market_news() -> list:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": (
            "(Federal Reserve OR inflation OR interest rates OR recession "
            "OR stock market OR economy OR Bitcoin OR Nasdaq OR S&P 500)"
        ),
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY,
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json().get("articles", [])
    except Exception as e:
        print(f"[NewsAPI] Error: {e}")
        return []


# ── AI BRIEFING ───────────────────────────────────────────────────────────────
def generate_market_briefing(articles: list) -> str:
    if not articles:
        return "⚠️ No market news found today."

    news_text = "\n".join(
        f"Title: {a.get('title', '')}\nDescription: {a.get('description', '')}\n"
        for a in articles[:10]
    )

    prompt = f"""You are a professional financial analyst.

Below are today's financial news articles.

Select the 5 most important stories for investors.

For each story provide:
1. Headline
2. One-sentence summary
3. Why it matters

Keep the entire response under 300 words.

Articles:
{news_text}"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/free",
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[OpenRouter] Error: {e}")
        return "⚠️ AI briefing unavailable today."


# ── MAIN ──────────────────────────────────────────────────────────────────────
async def main():
    bot = Bot(token=TOKEN)
    now_wib = datetime.now(pytz.timezone("Asia/Jakarta"))

    # ── Header ────────────────────────────────────────────────────────────────
    message = (
        f"🌅 Good morning! {now_wib.strftime('%A, %d %B %Y')}\n\n"
        f"{get_market_status()}\n"
        f"{get_usd_idr()}\n"
    )

    # ── Watchlist ─────────────────────────────────────────────────────────────
    message += "\n📊 Watchlist\n"
    for symbol in STOCKS:
        message += get_stock_price(symbol) + "\n"

    # ── Stock headlines ───────────────────────────────────────────────────────
    news_lines = [get_stock_news(s) for s in STOCKS]
    news_lines = [n for n in news_lines if n]
    if news_lines:
        message += "\n📰 Stock Headlines\n" + "\n".join(news_lines) + "\n"

    # ── AI market briefing ────────────────────────────────────────────────────
    articles = get_top_market_news()
    briefing = generate_market_briefing(articles)

    message += "\n\n🔥 AI Market Briefing\n\n" + briefing

    # ── Read-more links ───────────────────────────────────────────────────────
    if articles:
        message += "\n\n📚 Read More:\n"
        for article in articles[:5]:
            title = article.get("title", "Untitled")
            url   = article.get("url", "")
            message += f"\n• {title}\n{url}\n"

    message += "\nHave a great trading day! 💪"

    # ── Send ──────────────────────────────────────────────────────────────────
    for recipient in RECIPIENTS:
        await bot.send_message(chat_id=recipient, text=message)
    print(f"[{now_wib.strftime('%H:%M')} WIB] Message sent to {len(RECIPIENTS)} recipients.")


# ── SCHEDULER ─────────────────────────────────────────────────────────────────
def run_bot():
    asyncio.run(main())

if __name__ == "__main__":
    run_bot()  # fire once immediately

    schedule.every().day.at("01:00").do(run_bot)
    print("✅ Bot is running — will send every morning at 08:00 WIB.")

    while True:
        schedule.run_pending()
        time.sleep(60)