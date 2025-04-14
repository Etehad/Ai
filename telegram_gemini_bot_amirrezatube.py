import os
import json
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
TELEGRAM_TOKEN = "7656731366:AAE8L5_jm4Z8WOzKDqtdehIGgo9yH3rUt2Y"  # Replace with your BotFather token
GEMINI_API_KEY = "AIzaSyCRuG0Gz7kyVTMKSZZylr8aAB_v5ESj8e0"  # Replace with your Gemini API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to /start command in private chat with a help message."""
    if update.message.chat.type == "private":
        await update.message.reply_text(
            "سلام! لطفاً سوال خود را از هوش مصنوعی بپرسید."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message."""
    await update.message.reply_text(
        "🤖 من با هوش مصنوعی Gemini کار می‌کنم. فقط پیام بده تا جوابت رو بدم!"
    )

def get_gemini_response(prompt: str) -> str:
    """Get response from Gemini AI API."""
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        result = response.json()

        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        return "متأسفم، نتونستم پاسخ مناسبی پیدا کنم."
    except Exception as e:
        return f"خطا در دریافت پاسخ: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat_type = message.chat.type
    text = message.text.strip()

    if chat_type in ["group", "supergroup"]:
        if text.startswith("/"):
            prompt = text[1:]  # حذف کاراکتر اول /
            response = get_gemini_response(prompt)
            await message.reply_text(response)
    elif chat_type == "private":
        if text == "/start":
            await message.reply_text("سلام! لطفاً سوال خود را از هوش مصنوعی بپرسید.")
        else:
            response = get_gemini_response(text)
            await message.reply_text(response)

def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
