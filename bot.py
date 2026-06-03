from dotenv import load_dotenv
import os
import asyncio
import requests
import yfinance as yf
from telegram import Bot
from datetime import datetime
import pytz

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
STOCK_API_KEY = os.getenv("STOCK_API_KEY")

# Your custom watchlist — edit freely!
STOCKS = ["AAPL", "TSLA", "SPY", "NVDA", "META", "BBCA.JK", "TLKM.JK", "BBRI.JK"]

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.fast_info
    price = data.last_price
    prev_close = data.previous_close
    change = ((price - prev_close) / prev_close) * 100
    emoji = "📈" if change > 0 else "📉"
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
    
    message += "\n📰 Latest News:\n"
    for stock in STOCKS[:3]:
        news = get_stock_news(stock)
        if news:
            message += news + "\n"
    
    message += "\n" + get_usd_idr()
    message += "\n\nHave a great trading day! 💪"
    
    await bot.send_message(chat_id=CHAT_ID, text=message)

import schedule
import time

def run_bot():
    asyncio.run(main())

# Run every morning at 8:00 AM Jakarta time
schedule.every().day.at("08:00").do(run_bot)

# Run once immediately when you start it
run_bot()

print("✅ Bot is running! Will send every morning at 8AM Jakarta time 🕗")

while True:
    schedule.run_pending()
    time.sleep(60)