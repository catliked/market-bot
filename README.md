📈 Market Digest Bot

A personal automated financial market digest bot built in Python that delivers a daily morning briefing via Telegram — covering live stock prices, market status, financial news, and currency rates.

## 🚀 What It Does

Every morning at 8AM (Jakarta time), the bot automatically sends a personalised market update to Telegram including:

- 📊 Live stock prices for a custom watchlist (US + Indonesian stocks)
- 🟢 Real-time market open/close status for US and IDX markets
- 📰 Latest news headlines per stock
- 💱 USD/IDR exchange rate
- 📉📈 Price change percentage with directional emojis

---

## 🛠️ Tech Stack

- **Language:** Python 3.14
- **Libraries:** yfinance, python-telegram-bot, requests, schedule, pytz, python-dotenv
- **APIs:** Yahoo Finance, Telegram Bot API
- **Deployment:** Railway (cloud, runs 24/7)
- **Version Control:** Git + GitHub

---

## ✨ Features

- Tracks both US stocks (AAPL, TSLA, SPY, NVDA, META) and Indonesian blue chips (BBCA.JK, TLKM.JK, BBRI.JK)
- Automatically detects Indonesian stocks and displays prices in Rupiah (Rp) instead of USD
- Secure API key management using environment variables
- Fully automated — no manual trigger needed
- Deployed to cloud server, runs independently of local machine

---

## 📱 Sample Output

```
🌅 Good morning! Wednesday, 04 June 2026

📊 Market Status:
🇺🇸 US Market: 🟢 Open
🇮🇩 IDX: 🔴 Closed

💰 Your Watchlist:
📉 AAPL: $311.48 (-1.12%)
📈 TSLA: $424.89 (0.74%)
📉 SPY: $755.24 (-0.58%)
📉 NVDA: $217.23 (-2.06%)
📈 META: $614.67 (2.41%)
📈 BBCA.JK: Rp 9,250 (0.54%)

📰 Latest News:
📰 AAPL: Nvidia chief meets Foxconn chairman at Taiwan tech show
📰 TSLA: SpaceX Is About to IPO...
📰 SPY: UFO Turned a Forgotten Thesis Into 165% Returns

💱 USD/IDR: Rp 17,926

Have a great trading day! 💪
\```

## 💡 Why I Built This

As someone actively learning investing, I wanted a personalised daily briefing that cuts through information overload and delivers only what matters — my watchlist, market status, and relevant news — automatically every morning.

Built as a first Python project to learn APIs, automation, bot development, and cloud deployment.

## 🧠 What I Learned

- Calling and handling REST APIs in Python
- Secure secret management with environment variables
- Asynchronous programming with asyncio
- Telegram Bot API integration
- Automated scheduling
- Cloud deployment with Railway
- Git version control and GitHub

## 🔧 Setup

\```bash
git clone https://github.com/catliked/market-bot
cd market-bot
pip install -r requirements.txt
\```

Create a `.env` file:
\```
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_chat_id
STOCK_API_KEY=your_alphavantage_key
NEWS_API_KEY=your_newsapi_key
\```

Run:
\```bash
python bot.py
\```

---
*Built by Michelle — June 2026*
🇮🇩 IDX: 🔴 Closed

💰 Your Watchlist:
📉 AAPL: $311.48 (-1.12%)
📈 TSLA: $424.89 (0.74%)
📉 SPY: $755.24 (-0.58%)
📉 NVDA: $217.23 (-2.06%)
📈 META: $614.67 (2.41%)
📈 BBCA.JK: Rp 9,250 (0.54%)

📰 Latest News:
📰 AAPL: Nvidia chief meets Foxconn chairman at Taiwan tech show
📰 TSLA: SpaceX Is About to IPO...
📰 SPY: UFO Turned a Forgotten Thesis Into 165% Returns

💱 USD/IDR: Rp 17,926

Have a great trading day! 💪
```

---

## 💡 Why I Built This

As someone actively learning investing, I wanted a personalised daily briefing that cuts through information overload and delivers only what matters — my watchlist, market status, and relevant news — automatically every morning.

Built as a first Python project to learn APIs, automation, bot development, and cloud deployment.

---

## 🧠 What I Learned

- Calling and handling REST APIs in Python
- Secure secret management with `.env` files and environment variables
- Asynchronous programming with `asyncio`
- Telegram Bot API integration
- Automated scheduling with `schedule`
- Cloud deployment with Railway
- Git version control and GitHub

---

## 🔧 Setup (Local)

```bash
git clone https://github.com/catliked/market-bot
cd market-bot
pip install -r requirements.txt
```

Create a `.env` file:
```
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_chat_id
STOCK_API_KEY=your_alphavantage_key
NEWS_API_KEY=your_newsapi_key
```

Run:
```bash
python bot.py
```

---

*Built by Michelle — June 2026*

---

Also copy the README into your GitHub repo too — just edit the `README.md` file directly on GitHub and paste it there. Makes your repo look super professional 👊
