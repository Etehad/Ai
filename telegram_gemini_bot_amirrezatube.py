import os
import json
import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیمات لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = "7656731366:AAE8L5_jm4Z8WOzKDqtdehIGgo9yH3rUt2Y"
GEMINI_API_KEY = "AIzaSyCRuG0Gz7kyVTMKSZZylr8aAB_v5ESj8e0"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به دستور /start در چت خصوصی"""
    try:
        if update.message.chat.type == "private":
            await update.message.reply_text(
                "سلام! لطفاً سوال خود را از هوش مصنوعی بپرسید."
            )
    except Exception as e:
        logger.error(f"خطا در دستور start: {str(e)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال پیام راهنما"""
    try:
        await update.message.reply_text(
            "🤖 من با هوش مصنوعی Gemini کار می‌کنم. فقط پیام بده تا جوابت رو بدم!"
        )
    except Exception as e:
        logger.error(f"خطا در دستور help: {str(e)}")

def get_gemini_response(prompt: str) -> str:
    """دریافت پاسخ از Gemini AI API"""
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
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()

        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        return "متأسفم، نتونستم پاسخ مناسبی پیدا کنم."
    except requests.exceptions.Timeout:
        logger.error("Timeout در ارتباط با Gemini API")
        return "متأسفانه در حال حاضر سرور پاسخگو نیست. لطفاً کمی بعد دوباره تلاش کنید."
    except Exception as e:
        logger.error(f"خطا در دریافت پاسخ از Gemini: {str(e)}")
        return "متأسفانه خطایی رخ داده است. لطفاً دوباره تلاش کنید."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message
        chat_type = message.chat.type
        text = message.text.strip()

        if chat_type in ["group", "supergroup"]:
            if text.startswith("/"):
                prompt = text[1:]
                response = get_gemini_response(prompt)
                await message.reply_text(response)
        elif chat_type == "private":
            if text == "/start":
                await message.reply_text("سلام! لطفاً سوال خود را از هوش مصنوعی بپرسید.")
            else:
                response = get_gemini_response(text)
                await message.reply_text(response)
    except Exception as e:
        logger.error(f"خطا در پردازش پیام: {str(e)}")
        await message.reply_text("متأسفانه خطایی رخ داده است. لطفاً دوباره تلاش کنید.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت خطاهای عمومی"""
    logger.error(f"خطا در پردازش به‌روزرسانی: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "متأسفانه خطایی رخ داده است. لطفاً دوباره تلاش کنید."
        )

def main():
    """راه‌اندازی ربات"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error handler
    application.add_error_handler(error_handler)

    logger.info("Bot is running...")
    
    # اجرای ربات با مکانیزم‌های بهبود پایداری
    while True:
        try:
            application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False
            )
        except Exception as e:
            logger.error(f"خطا در اجرای ربات: {str(e)}")
            logger.info("تلاش مجدد در 5 ثانیه...")
            asyncio.sleep(5)

if __name__ == '__main__':
    main()
