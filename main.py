import os
import logging
import requests
import base64
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()

async def analyze_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_url = file.file_path
    response = requests.get(file_url)
    image_data = base64.standard_b64encode(response.content).decode("utf-8")
    await update.message.reply_text("Analiz yapiliyor, lutfen bekleyin...")
    headers = {"Authorization": "Bearer " + OPENAI_API_KEY, "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_data}},
                {"type": "text", "text": "Sen bir vibrasyon analiz uzmanissin. Bu elektrik motoru vibrasyon spektrum grafigini analiz et. 1. GENEL DURUM: Normal / Izleme Gerekli / Kritik / Acil Mudahale. 2. ANORMALLİKLER: hangi frekanslarda pik var, olasi ariza turu, ciddiyet. 3. RULMAN DURUMU: ic bilezik, dis bilezik, top frekanslari. 4. MEKANİK SORUNLAR: dengesizlik, yanlis hizalama, gevşeklik. 5. ONERİ: ne zaman mudahale edilmeli. Kisa ve net Turkce yaz."}
            ]
        }],
        "max_tokens": 1024
    }
    result = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()
    if "choices" in result:
        analysis = result["choices"][0]["message"]["content"]
    else:
        analysis = "Hata: " + str(result)
    await update.message.reply_text(analysis)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Vibrasyon spektrum grafigini gonderin, analiz edeyim.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, analyze_image))
    app.run_polling()

if __name__ == "__main__":
    main()
