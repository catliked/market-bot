import os
import asyncio
import requests
import yfinance as yf
from telegram import Bot
from datetime import datetime
import pytz

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
MOM_CHAT_ID = int(os.getenv("MOM_CHAT_ID"))

RECIPIENTS = [CHAT_ID, MOM_CHAT_ID]
STOCK_API_KEY = os.getenv("STOCK_API_KEY")

def get_top_market_news():
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": "(stock market OR Federal Reserve OR inflation OR interest rates OR Bitcoin OR S&P 500 OR Nasdaq OR economy)",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": "NEWS_API_KEY"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "ok":
        return []

    return data["articles"]

KEYWORDS = {
    "federal reserve": 10,
    "interest rate": 10,
    "inflation": 9,
    "recession": 9,
    "oil": 8,
    "china": 8,
    "tariff": 8,
    "bitcoin": 7,
    "earnings": 6,
    "nasdaq": 6,
    "s&p": 6,
    "stocks": 5
}

def score_article(article):
    text = (
        (article.get("title") or "") +
        " " +
        (article.get("description") or "")
    ).lower()

    score = 0

    for keyword, weight in KEYWORDS.items():
        if keyword in text:
            score += weight

    return score

def get_best_market_stories():
    articles = get_top_market_news()

    scored = sorted(
        articles,
        key=score_article,
        reverse=True
    )

    return scored[:5]

def format_news_section():
    stories = get_best_market_stories()

    text = "🔥 *Top Market Stories*\n\n"

    for i, article in enumerate(stories, 1):

        title = article["title"]
        url = article["url"]

        text += f"{i}. [{title}]({url})\n\n"

    return text

# Your custom watchlist — edit freely!
STOCKS = ["AAPL", "TSLA", "SPY", "NVDA", "META", "BBCA.JK", "TLKM.JK", "BBRI.JK"]

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.fast_info
    price = data.last_price
    prev_close = data.previous_close
    change = ((price - prev_close) / prev_close) * 100
    emoji = "📈" if change > 0 else "📉"
    
    # Use Rp for Indonesian stocks, $ for US stocks
    if symbol.endswith(".JK"):
        return f"{emoji} {symbol}: Rp {price:,.0f} ({change:.2f}%)"
    else:
        return f"{emoji} {symbol}: ${price:.2f} ({change:.2f}%)"

def get_stock_news(symbol):
    ticker = yf.Ticker(symbol)
    news = ticker.news
    if news:
        top = news[0]
        return f"📰 {symbol}: {top['content']['title']}"
    return ""

def get_market_status():
    now_est = datetime.now(pytz.timezone("US/Eastern"))
    now_wib = datetime.now(pytz.timezone("Asia/Jakarta"))
    
    # US market hours 9:30AM - 4:00PM EST weekdays
    us_open = now_est.weekday() < 5 and (9, 30) <= (now_est.hour, now_est.minute) <= (16, 0)
    
    # IDX market hours 9:00AM - 3:30PM WIB weekdays
    idx_open = now_wib.weekday() < 5 and (9, 0) <= (now_wib.hour, now_wib.minute) <= (15, 30)
    
    us_status = "🟢 Open" if us_open else "🔴 Closed"
    idx_status = "🟢 Open" if idx_open else "🔴 Closed"
    
    return f"🇺🇸 US Market: {us_status}\n🇮🇩 IDX: {idx_status}"

def get_usd_idr():
    ticker = yf.Ticker("USDIDR=X")
    rate = ticker.fast_info.last_price
    return f"💱 USD/IDR: Rp {rate:,.0f}"

async def main():
    bot = Bot(token=TOKEN)
    
    now_wib = datetime.now(pytz.timezone("Asia/Jakarta"))
    greeting = f"🌅 Good morning! {now_wib.strftime('%A, %d %B %Y')}\n"
    
    message = greeting
    message += "\n📊 Market Status:\n"
    message += get_market_status()
    
    message += "\n\n💰 Your Watchlist:\n"
    for stock in STOCKS:
        message += get_stock_price(stock) + "\n"
    
    message += "\n\n"
    message += format_news_section()
    
    message += "\n" + get_usd_idr()
    message += "\n\nHave a great trading day! 💪"
    
    for recipient in RECIPIENTS:
        await bot.send_message(
            chat_id=recipient,
            text=message,
            parse_mode="Markdown"
            )
        
import schedule
import time

def run_bot():
    asyncio.run(main())

# Schedule only, no immediate run
schedule.every().day.at("01:00").do(run_bot)

print("✅ Bot is running! Will send every morning at 8AM Jakarta time 🕗")

while True:
    schedule.run_pending()
    time.sleep(60)