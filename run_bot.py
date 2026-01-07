import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, FSInputFile
from backend.field_reader import FieldReader

# --- CONFIGURATION ---
API_TOKEN = '8133235026:AAH_YjBYERz9kLJjjKENR6YBWqWmAE8mx5c' 

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
reader = FieldReader() # Connected to Real Gemini

# --- RED FLAG LOGIC ---

# --- MODES ---
user_modes = {} # user_id -> mode_name

from backend.locales import LOCALES

# ... imports ...

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Entry Point for All Micro-Apps (Localized).
    """
    args = message.text.split(maxsplit=1)
    payload = args[1] if len(args) > 1 else ""
    
    # 🌍 Language Detection
    user_lang = message.from_user.language_code or "en"
    if "ru" in user_lang: 
        lang = "ru"
    else: 
        lang = "en" # Default Global

    # Detect Mode from Payload
    mode = "red_flag" # Default
    if payload in ["dream", "med", "paper", "reels"]:
        mode = payload
        
    # Set State
    user_modes[message.from_user.id] = mode
    
    # Get Localized Text
    text = LOCALES[lang]["welcome"].get(mode, LOCALES[lang]["welcome"]["red_flag"])
    
    # KEYBOARD (PERSISTENT)
    kb = get_main_keyboard(lang)
    
    await message.answer(text, parse_mode="Markdown", reply_markup=kb)

# --- MENU & LOGIC ---

def get_main_keyboard(lang="en"):
    """
    Persistent Menu for easy navigation.
    """
    if lang == "ru":
        buttons = [
            [types.KeyboardButton(text="🚩 RedFlag"), types.KeyboardButton(text="🌙 Сонник")],
            [types.KeyboardButton(text="🩸 Med"), types.KeyboardButton(text="📝 Юрист")],
            [types.KeyboardButton(text="🎬 Reels")]
        ]
    else:
        buttons = [
            [types.KeyboardButton(text="🚩 RedFlag"), types.KeyboardButton(text="🌙 Dream")],
            [types.KeyboardButton(text="🩸 Med"), types.KeyboardButton(text="📝 Law")],
            [types.KeyboardButton(text="🎬 Reels")]
        ]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(F.text.in_({"🚩 RedFlag", "🌙 Сонник", "🌙 Dream", "🩸 Med", "📝 Юрист", "📝 Law", "🎬 Reels"}))
async def handle_menu_click(message: types.Message):
    """
    Switch Mode via Menu.
    """
    user_lang = message.from_user.language_code or "en"
    lang = "ru" if "ru" in user_lang else "en"
    
    txt = message.text
    mode = "red_flag"
    
    if "Dream" in txt or "Сонник" in txt: mode = "dream"
    elif "Med" in txt: mode = "med"
    elif "Law" in txt or "Юрист" in txt: mode = "paper"
    elif "Reels" in txt: mode = "reels"
    
    user_modes[message.from_user.id] = mode
    
    # Send Welcome for New Mode
    text = LOCALES[lang]["welcome"].get(mode, LOCALES[lang]["welcome"]["red_flag"])
    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_keyboard(lang))


@dp.message(F.content_type.in_({'text', 'photo', 'document'}))
async def handle_content(message: types.Message):
    """
    Universal Handler
    """
    user_id = message.from_user.id
    mode = user_modes.get(user_id, "red_flag") # Default

    # 1. VISCERAL LOADING (Build Value)
    status_msg = await message.answer(f"⏳ **Очередь обработки: {mode}**...")
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1.0)

    # Fake Step 1
    await status_msg.edit_text("🧠 **Подключение к нейросети (Gemini 3)...**")
    await asyncio.sleep(1.5)

    # Fake Step 2
    if mode == "red_flag":
        await status_msg.edit_text("🚩 **Сканирование паттернов манипуляции...**")
    elif mode == "dream":
        await status_msg.edit_text("🔮 **Поиск архетипов в базе Юнга...**")
    elif mode == "med":
        await status_msg.edit_text("🩸 **Сверка с медицинскими протоколами...**")
    elif mode == "paper":
        await status_msg.edit_text("⚖️ **Поиск статей ГК РФ...**")
    await asyncio.sleep(1.5)

    # Fake Step 3 (Drama)
    await status_msg.edit_text("⚠️ **Обнаружены критические маркеры... Формирую отчет.**")
    await asyncio.sleep(1.0)
    
    text_content = ""
    media_content = None
    mime_type = None

    # 1. DOWNLOAD CONTENT
    try:
        if message.text:
            text_content = message.text
        
        elif message.photo:
            # Get largest photo
            file_id = message.photo[-1].file_id
            media_content = reader.download_file(file_id, API_TOKEN)
            mime_type = "image/jpeg"
            text_content = message.caption or ""

        elif message.document:
            file_id = message.document.file_id
            mime_type = message.document.mime_type
            
            # Allow PDF and Images
            if mime_type in ["application/pdf", "image/jpeg", "image/png"]:
                media_content = reader.download_file(file_id, API_TOKEN)
                text_content = message.caption or ""
            else:
                await status_msg.edit_text("❌ Формат не поддерживается. Пришлите PDF или Картинку.")
                return

        # 2. CALL GEMINI
        result = await reader.analyze_content(
            text=text_content, 
            media_content=media_content, 
            mime_type=mime_type, 
            mode=mode
        )
        
        raw_response = result.get("raw_text", "Ошибка генерации.")
        
        # ADD PROGRESS BAR (UI Hack)
        # We append this to the text to show "incompleteness"
        progress_bar = "\n\n░░░░░░░░░░ [80% Готово]\n🔒 **Полный прогноз скрыт.**"
        
        final_text = raw_response + progress_bar

        # 2.5 VOICE MODE (The Hook)
        # We take the first 200 chars or summary for voice to avoid long wait
        try:
            # Simple heuristic: Split by newline, take first paragraph or up to 200 chars
            voice_text = raw_response.split("\n")[0]
            if len(voice_text) < 50: # If too short, take more
                voice_text = raw_response[:200]
            
            # Clean up markdown for voice
            voice_text_clean = voice_text.replace("*", "").replace("#", "").replace("🚩", "")
            
            await bot.send_chat_action(message.chat.id, "record_voice")
            voice_path = await generate_voice(f"Послушай... {voice_text_clean}", folder="assets")
            
            voice_file = types.FSInputFile(voice_path)
            await message.answer_voice(voice_file, caption="🎙 **Аудио-резюме (AI)**")
            
            # Cleanup later (optional, for now we keep assets or rely on OS to clean tmp)
            # os.remove(voice_path) 
        except Exception as e:
            print(f"Voice Error: {e}") 
            # Non-blocking error, just skip voice

        # 2.5 VOICE MODE (The Hook)
        # We take the first 200 chars-ish
        try:
            user_lang = message.from_user.language_code or "en"
            lang = "ru" if "ru" in user_lang else "en"
            
            # Simple heuristic
            voice_text = raw_response.split("\n")[0]
            if len(voice_text) < 50: 
                voice_text = raw_response[:200]
            
            # Clean up markdown
            voice_text_clean = voice_text.replace("*", "").replace("#", "").replace("🚩", "")
            
            await bot.send_chat_action(message.chat.id, "record_voice")
            
            # Localized Intro
            intro_word = LOCALES[lang]["voice_intro"]
            voice_path = await generate_voice(f"{intro_word}... {voice_text_clean}", folder="assets")
            
            voice_file = types.FSInputFile(voice_path)
            await message.answer_voice(voice_file, caption="🎙 **AI Summary**")
            
        except Exception as e:
            print(f"Voice Error: {e}") 

        # 3. PAY BUTTON (Custom for each mode & Lang)
        btn_key = f"buy_{mode}"
        # Fallback to red_flag if key missing
        btn_text = LOCALES[lang]["buttons"].get(btn_key, LOCALES[lang]["buttons"]["buy_red_flag"]) 

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=btn_text, callback_data=f"buy_{mode}")]
        ])

        # Formatting Output
        await status_msg.edit_text(final_text, parse_mode="Markdown", reply_markup=keyboard)
    
    except Exception as e:
        await status_msg.edit_text(f"⚠️ Ошибка: {str(e)}")

# --- PAYMENT HANDLERS (TELEGRAM STARS) ---

@dp.callback_query(F.data.startswith("buy_"))
async def send_invoice(callback: types.CallbackQuery):
    """
    Sends an invoice for the selected service.
    """
    mode = callback.data.split("_")[1] # buy_dream -> dream
    
    prices = {
        "red_flag": 50,  # 50 XTR
        "dream": 25,     # 25 XTR
        "med": 100,      # 100 XTR
        "paper": 250     # 250 XTR
    }
    
    titles = {
        "red_flag": "🚩 Red Flag: Full Profile",
        "dream": "🌙 Dream: Fate Forecast",
        "med": "🩸 Med: Doctor Plan",
        "paper": "📝 Paper: Legal Pack"
    }

    desc = "Полный отчет + прогноз + рекомендации."
    price_amount = prices.get(mode, 50)
    
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=titles.get(mode, "Premium Report"),
        description=desc,
        payload=mode, # Store mode in payload to identify what to generate later
        provider_token="", # EMPTY FOR STARS!
        currency="XTR",
        prices=[types.LabeledPrice(label="Premium Access", amount=price_amount)],
        start_parameter="premium-buy"
    )
    await callback.answer()

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    """
    Must confirm that we are ready to accept payment.
    """
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    """
    🎉 PAYMENT SUCCESS! UNLOCK THE DEEP REPORT.
    """
    mode = message.successful_payment.invoice_payload # "dream", "med"...
    pmnt = message.successful_payment
    
    status_msg = await message.answer(
        f"✅ **Оплата принята! ({pmnt.total_amount} ⭐️)**\n"
        "Генерирую полный отчет..."
    )

    # RE-ANALYZE WITH PREMIUM PROMPT
    # We need the content again. 
    # HACK: For MVP, we don't have a database. 
    # We will ask user to Forward content if it's lost, OR we rely on text prompt?
    # BETTER: We just generate a generic expansion based on the mode + PREVIOUS CONTEXT?
    # NO, we need content.
    # SOLUTION: Use the 'Mock' logic for now or ask user to Reply? 
    # Wait, the simplest way for MVP where we don't store files:
    # Just ask user to RE-SEND the content, but this time it will trigger PREMIUM.
    # OR: Just update user_modes to 'premium' and ask to resend.
    
    # Let's try to be smart. We can't access old messages easily.
    # Let's update Mode to Premium and ask to Resend.
    
    premium_mode = f"{mode}_premium"
    user_modes[message.from_user.id] = premium_mode
    
    await status_msg.edit_text(
        "🔓 **PREMIUM РЕЖИМ АКТИВИРОВАН**\n\n"
        "Теперь перешлите сообщение / фото / файл **ЕЩЕ РАЗ**.\n"
        "Я прогоню его через Глубокий Анализ.",
        parse_mode="Markdown"
    )


@dp.callback_query(F.data == "buy_red_report")
async def buy_report(callback: types.CallbackQuery):
    await callback.message.answer("💳 **Включите VPN для оплаты (Demo).**")
    await callback.answer()

async def main():
    print("🚩 RED FLAG BOT (REAL GEMINI) STARTED")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
