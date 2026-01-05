import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo
import sys
import os

# Configuration
API_TOKEN = '8133235026:AAH_YjBYERz9kLJjjKENR6YBWqWmAE8mx5c' # Provided by user

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- WEB APP URL ---
# IMPORTANT: Telegram Web Apps require HTTPS.
# Since we are running locally on localhost:8000, we need a Tunnel (like ngrok).
# For now, I will use a placeholder or ask the user to run ngrok.
# If user has a public URL, they should replace this.
# Example: "https://<your-ngrok-id>.ngrok-free.app/shadow"
WEB_APP_URL = "https://Sasha777sh.github.io/edem_heart_mvp/frontend/shadow_reader.html" 

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Send a message with a button that opens the Web App.
    """
    kb = [
        [types.KeyboardButton(text="🔮 Открыть Shadow Reader", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        "👁 **Shadow Reader (Теневой Аналитик)**\n\n"
        "Я — твое зеркало. Я вижу то, что скрыто за словами.\n"
        "Загрузи в меня текст, и я покажу тебе истинные мотивы.\n\n"
        "Нажми кнопку ниже, чтобы открыть сканер.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(F.text)
async def echo(message: types.Message):
    await message.answer("Используй кнопку внизу, чтобы открыть Аналитик.")

async def main():
    print("🤖 Shadow Reader Bot Started...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
