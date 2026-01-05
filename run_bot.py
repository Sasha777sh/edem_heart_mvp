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
WEB_APP_URL = "https://shy-knives-hide.loca.lt/shadow" 

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Send a message with a button that opens the Web App.
    """
    kb = [
        [types.KeyboardButton(text="🔮 Включить Mini App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [
            types.KeyboardButton(text="👁 Диалог"),
            types.KeyboardButton(text="💼 Переговоры")
        ],
        [
            types.KeyboardButton(text="⚔️ Market Scanner"),
            types.KeyboardButton(text="👥 Кадры/HR")
        ],
        [
            types.KeyboardButton(text="🛒 E-Com (WB/Ozon)")
        ],
        [
            types.KeyboardButton(text="ℹ️ Режимы"),
            types.KeyboardButton(text="❓ Зачем это?")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        "👁 **Field Reader (Аналитик Поля)**\n\n"
        "Я вижу то, что скрыто за словами.\n"
        "Выбери режим ниже или просто перешли мне сообщение.\n\n"
        "👇 **МЕНЮ УПРАВЛЕНИЯ** 👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

from backend.field_reader import FieldReader
import json

# Initialize Native Field Engine
field_engine = FieldReader(api_key="AIzaSyAVcKK5KcpduBv2hh-uvMreDGvTHX-uURE")

# User state storage (in-memory for MVP)
user_modes = {}

@dp.message(Command("mode"))
async def cmd_mode(message: types.Message):
    """
    Select Analysis Mode.
    """
    kb = [
        [
            types.KeyboardButton(text="👁 Диалог"),
            types.KeyboardButton(text="💼 Переговоры")
        ],
        [
            types.KeyboardButton(text="⚔️ Market Scanner"),
            types.KeyboardButton(text="👥 Кадры/HR")
        ],
        [
            types.KeyboardButton(text="🛒 E-Com (WB/Ozon)")
        ],
        [
            types.KeyboardButton(text="ℹ️ Режимы"),
            types.KeyboardButton(text="❓ Зачем это?")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите режим или справку:", reply_markup=keyboard)

@dp.message(F.text == "ℹ️ Режимы")
async def show_modes_info(message: types.Message):
    # Mode 1: Communication
    await message.answer_photo(
        photo=types.FSInputFile("assets/mode_communication.png"),
        caption="👁 **1. ДИАЛОГ (Communication)**\n\nАнализ личных переписок. Защита от манипуляций. Показывает скрытые мотивы и возвращает ответственность."
    )
    # Mode 2: Negotiation
    await message.answer_photo(
        photo=types.FSInputFile("assets/mode_negotiation.png"),
        caption="💼 **2. ПЕРЕГОВОРЫ (Contract Analyst)**\n\nАнализ контрактов и офферов. Находит юридические риски, асимметрию прав и скрытые 'мины' в условиях."
    )
    # Mode 3: Market Scanner
    await message.answer_photo(
        photo=types.FSInputFile("assets/mode_competitor.png"),
        caption="⚔️ **3. MARKET SCANNER (Аудит Рынка)**\n\nАнализ конкурентов. Находит структурные уязвимости рынка и рычаги для твоего роста. Просто кинь домен."
    )
    # Mode 4: E-Com
    await message.answer_photo(
        photo=types.FSInputFile("assets/mode_marketplace.png"),
        caption="🛒 **4. E-COM AUDIT (WB/Ozon)**\n\nАнализ карточек товаров. Находит разрыв между обещаниями и отзывами. Показывает, как забрать трафик конкурента."
    )

@dp.message(F.text == "❓ Зачем это?")
async def show_philosophy(message: types.Message):
    text = (
        "🌪 **ФИЛОСОФИЯ АНАЛИЗА**\n\n"
        "Это дает тебе **свободу не играть в чужие игры**.\n\n"
        "🔴 **КАК ЭТО БЫЛО РАНЬШЕ:**\n"
        "1. Тебе пишут херню (манипуляцию).\n"
        "2. Ты эмоционально реагируешь (злишься, оправдываешься).\n"
        "3. Ты тратишь энергию, а собеседник «кормится» твоей реакцией.\n\n"
        "🟢 **ЧТО ДАЕТ ЭТОТ ИНСТРУМЕНТ:**\n"
        "1. **Дистанция**. Ты видишь механику: «Ага, это стратегия 'Жертва'». Тебя это больше не цепляет.\n"
        "2. **Сохранение энергии**. Ты не вступаешь в бой, который не можешь выиграть.\n"
        "3. **Ход конем**. Бот дает ответ, который ломает сценарий и возвращает ответственность агрессору.\n\n"
        "🎯 **ЦЕЛЬ:**\n"
        "Чтобы твой интеллект работал на ТВОИ задачи, а не обслуживал комплексы людей в интернете.\n"
        "Это инструмент **гигиены внимания**."
    )
    await message.answer(text, parse_mode="Markdown")

# --- HELPERS ---

def get_mode_tip(mode: str) -> str:
    tips = {
        "communication": "💡 Совет: Перешли переписку или голосовое.",
        "negotiation": "💡 Совет: Сфоткай первую страницу договора.",
        "competitor": "💡 Совет: Напиши домен конкурента (пример: tbank.ru).",
        "hr": "💡 Совет: Кинь скриншот резюме или вакансии.",
        "marketplace": "💡 Совет: Кинь ссылку на товар или скриншот карточки."
    }
    return tips.get(mode, "")

async def fake_progress_bar(message: types.Message, text: str):
    # Simple visual update to show "aliveness"
    phases = ["🌑", "🌒", "🌓", "🌔", "🌕"]
    for phase in phases:
        await message.edit_text(f"{phase} {text}...")
        await asyncio.sleep(0.3)

# --- HANDLERS ---

@dp.message(F.text.in_({"👁 Диалог", "💼 Переговоры", "⚔️ Конкурент", "⚔️ Market Scanner", "👥 Кадры/HR", "🛒 E-Com (WB/Ozon)"}))
async def set_mode(message: types.Message):
    mode_map = {
        "👁 Диалог": "communication",
        "💼 Переговоры": "negotiation",
        "⚔️ Market Scanner": "competitor",
        "⚔️ Конкурент": "competitor",
        "👥 Кадры/HR": "hr",
        "🛒 E-Com (WB/Ozon)": "marketplace"
    }
    selected_mode = mode_map[message.text]
    user_modes[message.from_user.id] = selected_mode
    
    tip = get_mode_tip(selected_mode)
    
    await message.answer(
        f"✅ Режим установлен: **{message.text}**.\n{tip}",
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )

from backend.pdf_generator import generate_report_pdf

def get_risk_level(analysis: dict) -> str:
    # Basic heuristic: Red if many negative keywords, Green if positive, Yellow default
    text = str(analysis).lower()
    if "риск" in text or "цена ошибки" in text or "слепое место" in text:
        return "🔴 HIGH RISK"
    if "асимметрия" in text:
        return "🟡 MEDIUM RISK"
    return "🟢 LOW RISK" # Rare in this bot :)

def format_response(analysis: dict, mode: str) -> str:
    mode_titles = {
        "communication": "АНАЛИЗ ДИАЛОГА",
        "negotiation": "АНАЛИЗ ПЕРЕГОВОРОВ (CONTRACT)",
        "competitor": "MARKET SCANNER (АУДИТ РЫНКА)",
        "hr": "РИСК-АНАЛИЗ (HR)",
        "marketplace": "E-COM AUDIT (ТОВАР)"
    }
    title = mode_titles.get(mode, "АНАЛИЗ")
    risk_header = get_risk_level(analysis)
    
    footer = "\n\n__Generated by Field Reader AI__"
    
    content = ""
    if mode in ["hr", "negotiation", "competitor", "marketplace"]:
         content = (
            f"📊 **{title}** | {risk_header}\n\n"
            f"{analysis.get('behavior', 'No data')}\n\n"
            f"{analysis.get('imposed_role', 'No data')}\n\n"
            f"{analysis.get('hidden_motivation', 'No data')}\n\n"
            f"{analysis.get('fear', 'No data')}\n\n"
            f"{analysis.get('recommendation', 'No data')}"
        )
    else:
        content = (
            f"📊 **{title}** | {risk_header}\n\n"
            f"🎭 **Суть/Роль**: {analysis.get('imposed_role', 'Не определена')}\n"
            f"🧊 **Маркеры**: {analysis.get('behavior', 'No data')}\n\n"
            f"🎯 **Скрытый мотив**: {analysis.get('hidden_motivation', 'No data')}\n"
            f"😱 **Риск/Страх**: {analysis.get('fear', 'No data')}\n\n"
            f"🛡 **Вердикт**: {analysis.get('recommendation', 'No data')}"
        )
    
    return content + footer

# Inline keyboard for actions
def get_action_keyboard(analysis_id: str = "temp"):
    # In a real app, we'd store analysis_id to retrieve data for PDF
    kb = [
        [
            types.InlineKeyboardButton(text="📄 Скачать PDF", callback_data="get_pdf"),
            types.InlineKeyboardButton(text="✍️ Ответ", callback_data="gen_reply")
        ],
        [types.InlineKeyboardButton(text="🗑 Скрыть отчет", callback_data="delete_msg")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

@dp.callback_query(F.data == "delete_msg")
async def delete_message_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()

@dp.callback_query(F.data == "get_pdf")
async def get_pdf_handler(callback: types.CallbackQuery):
    await callback.answer("⏳ Генерирую PDF...")
    # For MVP, we reconstruct simple data from the message or context. 
    # Since we don't have DB, we'll create a generic report for now.
    # ideally we pass the analysis object.
    
    # Mock analysis for PDF generation based on current mode
    pdf_buffer = generate_report_pdf(
        {"behavior": "See chat history", "recommendation": "Consult Field Reader"}, 
        "REPORT_EXPORT"
    )
    
    file = types.BufferedInputFile(pdf_buffer.getvalue(), filename="FieldReader_Report.pdf")
    await callback.message.answer_document(document=file, caption="✅ Ваш отчет готов.")

@dp.callback_query(F.data == "gen_reply")
async def gen_reply_handler(callback: types.CallbackQuery):
    await callback.answer("Генерирую вариант ответа...")
    await callback.message.answer("📝 **Рекомендуемый ответ:**\n\n'Мы готовы обсудить условия, но только после фиксации SLA и штрафов за просрочку.'\n\n(Скопируйте и отправьте)")

@dp.message(F.text)
async def analyze_message(message: types.Message):
    """
    Analyze any text sent to the bot.
    """
    if message.text == "/start" or message.text == "ℹ️ Режимы" or message.text == "❓ Зачем это?": return 

    current_mode = user_modes.get(message.from_user.id, "communication")
    
    # IMPROVEMENT 1: Native typing action
    await bot.send_chat_action(message.chat.id, action="typing")
    
    status_msg = await message.answer(f"🌑 Загрузка контекста ({current_mode})...")
    
    # IMPROVEMENT 2: Fake visual loader
    asyncio.create_task(fake_progress_bar(status_msg, f"Анализ ({current_mode})"))

    try:
        analysis = field_engine.analyze_content(text=message.text, mode=current_mode)
        
        if "error" in analysis:
            await status_msg.edit_text(f"Ошибка анализа: {analysis['error']}")
            return

        response_text = format_response(analysis, current_mode)
        
        # IMPROVEMENT 3: Inline Action Keyboard
        await status_msg.edit_text(response_text, parse_mode="Markdown", reply_markup=get_action_keyboard())
        
    except Exception as e:
        await status_msg.edit_text(f"Сбой системы: {e}")

@dp.message(F.photo)
async def analyze_photo(message: types.Message):
    """
    Analyze photos (Documents/Screenshots).
    """
    current_mode = user_modes.get(message.from_user.id, "communication")
    
    await bot.send_chat_action(message.chat.id, action="upload_photo")
    status_msg = await message.answer(f"🌑 Сканирование документа ({current_mode})...")
    
    asyncio.create_task(fake_progress_bar(status_msg, "OCR Чтение"))

    try:
        # Download photo
        photo = message.photo[-1]
        file_io = io.BytesIO()
        await bot.download(photo, destination=file_io)
        file_io.seek(0)
        image = Image.open(file_io)

        # Analyze
        analysis = field_engine.analyze_content(image_data=image, mode=current_mode)

        if "error" in analysis:
            await status_msg.edit_text(f"Ошибка анализа: {analysis['error']}")
            return

        response_text = format_response(analysis, current_mode)
        await status_msg.edit_text(response_text, parse_mode="Markdown", reply_markup=get_action_keyboard())

    except Exception as e:
        await status_msg.edit_text(f"Сбой сканирования: {e}")

async def main():
    print("🤖 Field Reader Bot Started (Text + Vision)...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
