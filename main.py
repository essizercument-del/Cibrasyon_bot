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
    
    await update.message.reply_text("Analiz yapılıyor, lütfen bekleyin...")
    
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_data
                    }
                },
                {
                    "text": """Sen bir vibrasyon analiz uzmanısın. Bu elektrik motoru vibrasyon spektrum grafiğini analiz et ve şunları belirt:\n\n1. GENEL DURUM: (Normal / İzleme Gerekli / Kritik / Acil Müdahale)\n\n2. TESPİT EDİLEN ANORMALLİKLER:\n- Hangi frekanslarda pik var\n- Olası arıza türü\n- Ciddiyet seviyesi\n\n3. RULMAN DURUMU:\n- İç bilezik, dış bilezik, top frekanslarında sorun var mı?\n\n4. MEKANİK SORUNLAR:\n- Dengesizlik, yanlış hizalama, gevşeklik var mı?\n\n5. ÖNERİ: Ne zaman ve nasıl müdahale edilmeli?\n\nKısa ve net Türkçe yaz."""
                }
            ]
        }]
    }
    
    gemini_response = requests.post(gemini
