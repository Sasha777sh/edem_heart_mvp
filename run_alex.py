import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from backend.field_reader import FieldReader
from backend.brain import VoiceMode
from dotenv import load_dotenv

# --- CONFIGURATION ---
API_TOKEN = '8246331470:AAH8UJ3Hx2VbPJx91cUWAKPOgwI6ZIy0BdE' # Alex Bot Token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env (for GEMINI_API_KEY)
load_dotenv()

# Initialize Bot
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Initialize Brain
field_reader = FieldReader()

# --- HANDLERS ---

@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    """
    Entry point for Alex / Dome Luxe.
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    logger.info(f"ALEX BOT: New user {user_id} ({username})")

    # Force ALEX_SALES mode
    current_mode = "alex_sales" 
    
    # Get initial greeting from AI
    # We pass a fake "start" input to get the opening hook
    response_text = field_reader.get_response(
        user_id=str(user_id),
        user_text="[SYSTEM: User clicked /start. Introduce yourself as Alex from Dome Luxe. Brief & Punchy.]",
        mode=current_mode
    )

    # Keyboard (Call to Action)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    # Alex want's the phone number, or a link to the site
    keyboard.add(types.InlineKeyboardButton(text="📱 Write to WhatsApp", url="https://wa.me/66956667788")) # Replace with actual
    keyboard.add(types.InlineKeyboardButton(text="🏰 View Villas (Site)", url="https://dome-luxe-global.vercel.app/dome"))

    await message.answer(response_text, reply_markup=keyboard)


@dp.message_handler(content_types=['text', 'photo', 'voice'])
async def handle_message(message: types.Message):
    """
    Main chat loop.
    """
    user_id = str(message.from_user.id)
    user_text = ""

    # 1. Handle Voice
    if message.voice:
        await message.answer("🎧 Listening...")
        # (Simplified: In a real separate bot we might skip voice or copy the transcriber logic)
        # For MVP Alex, let's treat voice as text placeholder or implement basic transcoding if needed.
        # But `run_bot.py` has the heavy lifting. Let's keep Alex text-first for speed, 
        # or we need to duplicate the download & whisper logic. 
        # User said "Alex doesn't need to be complicated".
        user_text = "[USER SENT A VOICE MESSAGE]" 
    
    # 2. Handle Text
    elif message.text:
        user_text = message.text

    # 3. Handle Photo (e.g. land plot)
    elif message.photo:
         await message.answer("👀 Looking at the land...")
         # Again, duplicating vision logic might be overkill if not needed.
         # But Alex is a "Global Dome Architect", he might need to see land.
         # For now, let's just pass a text description.
         user_text = "[USER SENT A PHOTO]"

    if not user_text:
        return

    # ALEX ALWAYS RESPONDS IN ALEX MODE
    response = field_reader.get_response(
        user_id=user_id,
        user_text=user_text,
        mode="alex_sales"
    )

    await message.answer(response)

if __name__ == '__main__':
    print("💎 ALEX SALES BOT STARTED")
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logger.error(f"Alex Bot Error: {e}")
