# -*- coding: utf-8 -*-
from flask import Flask, request
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    symbol = data.get("symbol", "N/A")
    side = data.get("side", "N/A")
    price = data.get("price", "N/A")

    message = (
        f"*Neues Signal erhalten:*\n"
        f"📈 Symbol: `{symbol}`\n"
        f"📊 Richtung: *{side}*\n"
        f"💵 Preis: `{price}`"
    )
    send_telegram_message(message)
    return {"status": "ok"}, 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)