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
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "👋 Hello! I'm your AI assistant powered by Gemini. Just send me a message and I'll respond!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "🤖 I can help you with various tasks using Gemini AI. Just send me any message and I'll respond!"
    )

def get_gemini_response(prompt: str) -> str:
    """Get response from Gemini AI API."""
    headers = {
        'Content-Type': 'application/json'
    }
    
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
        
        # Extract the text from the response
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        return "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and respond using Gemini AI."""
    user_message = update.message.text
    
    # Get response from Gemini
    ai_response = get_gemini_response(user_message)
    
    # Send the response back to the user
    await update.message.reply_text(ai_response)

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 
