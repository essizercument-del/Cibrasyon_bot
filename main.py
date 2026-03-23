import os
import logging
import anthropic
import requests
import base64
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

async def analyze_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_url = file.file_path
    
    response = requests.get(file_url)
    image_data = base64.standard_b64encode(response.content).decode("utf-8")
    
    message = anthropic_client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": """Sen bir vibrasyon analiz uzmanısın. Bu elektrik motoru vibrasyon spektrum grafiğini analiz et ve şunları belirt:

1. GENEL DURUM: (Normal / İzleme Gerekli / Kritik / Acil Müdahale)

2. TESPİT EDİLEN ANORMALLİKLER:
- Hangi frekanslarda pik var
- Olası arıza türü
- Ciddiyet seviyesi

3. RULMAN DURUMU:
- İç bilezik, dış bilezik, top frekanslarında sorun var mı?

4. MEKANİK SORUNLAR:
- Dengesizlik, yanlış hizalama, gevşeklik var mı?

5. ÖNERİ: Ne zaman ve nasıl müdahale edilmeli?

Kısa ve net yaz, teknik terimlerle."""
                    }
                ],
            }
        ],
    )
    
    await update.message.reply_text(message.content[0].text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Vibrasyon spektrum grafiğini gönderin, analiz edeyim.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, analyze_image))
    from telegram.ext import CommandHandler
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
