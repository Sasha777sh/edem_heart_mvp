import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo

# --- CONFIGURATION ---
# 1. Create a new bot via @BotFather
# 2. Paste the token below
API_TOKEN = 'INSERT_NEW_BOT_TOKEN_HERE' 

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- MODES ---
user_modes = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Handle /start with optional payload (Deep Linking).
    """
    args = message.text.split(maxsplit=1)
    payload = args[1] if len(args) > 1 else ""

    if payload == "red_flag":
        await message.answer(
            "🚩 **Red Flag Scanner.**\n\n"
            "Я вижу скрытые манипуляции в переписке.\n"
            "Пришли мне скриншот диалога или перешли сообщения.\n\n"
            "Я найду:\n"
            "— Газлайтинг (когда из тебя делают сумасшедшего)\n"
            "— Двойные послания\n"
            "— Игнор и эмоциональные качели\n\n"
            "👇 **Жду материалы.**",
            parse_mode="Markdown"
        )
        user_modes[message.from_user.id] = "red_flag"
        return

    # Default Start
    await message.answer(
        "🚩 **Red Flag Scanner**\n\n"
        "Этот бот проверяет отношения на токсичность.\n"
        "Просто перешли сообщение или скриншот.",
        parse_mode="Markdown"
    )
    user_modes[message.from_user.id] = "red_flag"

@dp.message(F.content_type.in_({'text', 'photo', 'document'}))
async def handle_content(message: types.Message):
    """
    Handle content for analysis.
    """
    user_id = message.from_user.id
    
    # 1. Notify User
    status_msg = await message.answer("🧠 **Анализирую переписку...**")

    # 2. SIMULATION (Connect AI here)
    # In real version, call FieldReader / Gemini here.
    await asyncio.sleep(2) 

    # 3. Response
    response_text = (
        "🚩 **НАЙДЕНЫ КРАСНЫЕ ФЛАГИ**\n\n"
        "1. **Газлайтинг**: Фраза 'Ты все выдумываешь' — это попытка обесценить твои чувства.\n"
        "2. **Проекция**: Он обвиняет тебя в том, что делает сам.\n\n"
        "💡 **Вердикт**: Уровень токсичности 85%. Рекомендуется дистанцироваться."
    )

    await status_msg.edit_text(response_text, parse_mode="Markdown")

async def main():
    print("🔥 Red Flag Bot Started...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
