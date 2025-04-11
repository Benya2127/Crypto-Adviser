import os
import logging
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Пример логики сигнала (упрощённо)
def analyze_price_history(data):
    if len(data) < 2:
        return "Недостаточно данных"
    if data[-1] > data[-2]:
        return "Продать"
    elif data[-1] < data[-2]:
        return "Купить"
    else:
        return "Держать"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я крипто-бот. Напиши /signal <символ>")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Пожалуйста, укажи символ монеты. Например: /signal BTC")
        return

    symbol = context.args[0].upper() + "USDT"
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=10"
    try:
        response = requests.get(url)
        data = response.json()
        closes = [float(candle[4]) for candle in data]
        signal_result = analyze_price_history(closes)
        await update.message.reply_text(f"Сигнал для {symbol}: {signal_result}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.run_polling()

if __name__ == "__main__":
    main()