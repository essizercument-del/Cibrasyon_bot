import os
import logging
import requests
import base64
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

async def analyze_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_url = file.file_path
    response = requests.get(file_url)
    image_data = base64.standard_b64encode(response.content).decode("utf-8")
    await update.message.reply_text("Analiz yapiliyor, lutfen bekleyin...")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY
    payload = {"contents": [{"parts": [{"inline_data": {"mime_type": "image/jpeg", "data": image_data}}, {"text": "Sen bir vibrasyon analiz uzmanissin. Bu elektrik motoru vibrasyon spektrum grafigini analiz et. 1. GENEL DURUM: Normal / Izleme Gerekli / Kritik / Acil Mudahale. 2. ANORMALLİKLER: hangi frekanslarda pik var, olasi ariza turu, ciddiyet. 3. RULMAN DURUMU: ic bilezik, dis bilezik, top frekanslari. 4. MEKANİK SORUNLAR: dengesizlik, yanlis hizalama, gevşeklik. 5. ONERİ: ne zaman mudahale edilmeli. Kisa ve net Turkce yaz."}]}]}
    result = requests.post(url, json=payload).json()
    if "candidates" in result:
        analysis = result["candidates"][0]["content"]["parts"][0]["text"]
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
