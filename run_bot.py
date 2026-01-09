import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# FORCIBLY LOAD ENV
load_dotenv()

# DEBUG PRINT TO CONSOLE
key = os.getenv("GEMINI_API_KEY")
if key:
    print(f"✅ FOUND GEMINI_API_KEY: {key[:5]}...{key[-4:]}")
else:
    print("❌ ERROR: GEMINI_API_KEY NOT FOUND IN ENV")

# AIOGRAM 2.x IMPORTS
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.dispatcher.filters import Text
from backend.field_reader import FieldReader
from backend.database import (
    get_user, create_user, get_referral_stats, use_credit,
    get_user_mode, set_user_mode, add_to_history, get_user_history, update_streak
)
from backend.voice import generate_voice
from backend.locales import LOCALES

# --- CONFIGURATION ---
API_TOKEN = '8133235026:AAEY1RbrpIGt1WCmHiqHVM2sSaztG0khCAc' 

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
reader = FieldReader() # Connected to Real Gemini

# --- HANDLERS (Aiogram 2.x) ---

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """
    Entry Point for All Micro-Apps (Localized + Referral Tracking).
    """
    args = message.text.split(maxsplit=1)
    payload = args[1] if len(args) > 1 else ""
    
    # 🌍 Language Detection
    user_lang = message.from_user.language_code or "en"
    lang = "ru" if "ru" in user_lang else "en"

    # 👥 REFERRAL TRACKING
    referrer_id = None
    mode = "red_flag" # Default
    
    if payload.startswith("ref_"):
        try:
            referrer_id = int(payload.replace("ref_", ""))
        except:
            pass
    elif payload in ["dream", "med", "paper", "reels", "psycho", "prompts", "alex_sales", "dome",
                     "avito", "angry", "ex", "boss", "toast"]:
        mode = payload
    
    # Create user if new
    user_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or "User"
    
    is_new = create_user(user_id, username, first_name, referrer_id)
    
    # Notify referrer
    if is_new and referrer_id:
        stats = get_referral_stats(referrer_id)
        refs = stats["referrals"]
        credits = stats["credits"]
        
        notify_text = f"🎉 +1 Реферал!\n\nВсего: {refs}\nКредиты: {credits}"
        if refs % 3 == 0:
            notify_text += f"\n\n🔓 Новый кредит разблокирован! Используй /premium для бесплатного прогона."
        
        try:
            await bot.send_message(referrer_id, notify_text)
        except:
            pass
        
    # Set State
    set_user_mode(message.from_user.id, mode)
    
    # Get Localized Text
    text = LOCALES[lang]["welcome"].get(mode, LOCALES[lang]["welcome"]["red_flag"])
    
    # KEYBOARD
    kb = get_main_keyboard(lang)
    
    await message.answer(text, parse_mode="Markdown", reply_markup=kb)


def get_main_keyboard(lang="en"):
    if lang == "ru":
        buttons = [
            [types.KeyboardButton(text="🚩 RedFlag"), types.KeyboardButton(text="🌙 Сонник")],
            [types.KeyboardButton(text="🩸 Med"), types.KeyboardButton(text="🧠 Psychosom")],
            [types.KeyboardButton(text="📟 Prompts"), types.KeyboardButton(text="🛒 Market")],
            [types.KeyboardButton(text="📝 Юрист"), types.KeyboardButton(text="🏰 Dome")],
            [types.KeyboardButton(text="🤵 Alex"), types.KeyboardButton(text="🎬 Reels")]
        ]
    else:
        buttons = [
            [types.KeyboardButton(text="🚩 RedFlag"), types.KeyboardButton(text="🌙 Dream")],
            [types.KeyboardButton(text="🩸 Med"), types.KeyboardButton(text="🧠 Psychosom")],
            [types.KeyboardButton(text="📟 Prompts"), types.KeyboardButton(text="🛒 Market")],
            [types.KeyboardButton(text="📝 Law"), types.KeyboardButton(text="🏰 Dome")],
            [types.KeyboardButton(text="🤵 Alex"), types.KeyboardButton(text="🎬 Reels")]
        ]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


@dp.message_handler(lambda message: message.text in ["🚩 RedFlag", "🌙 Сонник", "🌙 Dream", "🩸 Med", "📝 Юрист", "📝 Law", "🎬 Reels", "🧠 Psychosom", "📟 Prompts", "🛒 Market", "🏰 Dome", "🤵 Alex", "💵 Avito", "🤬 Angry", "💔 Ex", "👔 Boss", "🥂 Toast"])
async def handle_menu_click(message: types.Message):
    """ Switch Mode via Menu. """
    user_lang = message.from_user.language_code or "en"
    lang = "ru" if "ru" in user_lang else "en"
    txt = message.text
    
    if "Dream" in txt or "Сонник" in txt: mode = "dream"
    elif "Med" in txt: mode = "med"
    elif "Law" in txt or "Юрист" in txt: mode = "paper"
    elif "Reels" in txt: mode = "reels"
    elif "Psychosom" in txt: mode = "psycho"
    elif "Prompts" in txt: mode = "prompts"
    elif "Market" in txt: mode = "market"
    elif "Dome" in txt: mode = "dome"
    elif "Alex" in txt: mode = "alex_sales"
    elif "Avito" in txt: mode = "avito"
    elif "Angry" in txt: mode = "angry"
    elif "Ex" in txt: mode = "ex"
    elif "Boss" in txt: mode = "boss"
    elif "Toast" in txt: mode = "toast"
    elif "RedFlag" in txt: mode = "red_flag"
    else: mode = "red_flag"

    set_user_mode(message.from_user.id, mode)
    print(f"🔄 User {message.from_user.id} switched to mode: {mode}")
    
    text = LOCALES[lang]["welcome"].get(mode, LOCALES[lang]["welcome"]["red_flag"])
    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_keyboard(lang))


@dp.message_handler(commands=['invite'])
async def cmd_invite(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code or "en"
    lang = "ru" if "ru" in user_lang else "en"
    
    if not get_user(user_id):
        create_user(user_id, message.from_user.username or "", message.from_user.first_name or "User")
    
    stats = get_referral_stats(user_id)
    bot_username = (await bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    if lang == "ru":
        text = f"🎁 **РЕФЕРАЛЬНАЯ ПРОГРАММА**\n\nПриглашай друзей и получай **бесплатные прогоны**!\n\n📊 **Твоя статистика:**\n• Приглашено: {stats['referrals']}\n• Кредиты: {stats['credits']} 🎫\n\n🔗 **Твоя ссылка:**\n`{ref_link}`\n\n💡 **За каждые 3 реферала = 1 кредит.**"
    else:
        text = f"🎁 **REFERRAL PROGRAM**\n\nInvite friends and get **free analyses**!\n\n📊 **Your stats:**\n• Invited: {stats['referrals']}\n• Credits: {stats['credits']} 🎫\n\n🔗 **Your link:**\n`{ref_link}`\n\n💡 **Every 3 referrals = 1 credit.**"
    
    await message.answer(text, parse_mode="Markdown")


@dp.message_handler(commands=['history'])
async def cmd_history(message: types.Message):
    user_id = message.from_user.id
    history = get_user_history(user_id)
    
    if not history:
        await message.answer("🗓 Ваша история пока пуста.")
        return
        
    text = "🗓 **Ваша история анализов:**\n\n"
    for item in history:
        date = item["date"].split("T")[0] if "T" in item["date"] else item["date"]
        text += f"🔹 **{item['mode'].upper()}** ({date})\n   *Вход:* {item['content']}...\n   *Итог:* {item['result']}...\n\n"
        
    await message.answer(text, parse_mode="Markdown")


@dp.message_handler(content_types=['text', 'photo', 'document', 'voice'])
async def handle_content(message: types.Message):
    user_id = message.from_user.id
    mode = get_user_mode(user_id)

    streak, reward = update_streak(user_id)
    streak_text = f" 🔥 {streak} дня!" if streak > 1 else ""
    status_msg = await message.answer(f"⏳ **Очередь обработки: {mode}**{streak_text}...")
    if reward: await message.answer("🎁 **БОНУС!** Вы с нами неделю! +1 Кредит на счет.")
    
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1.0)
    await status_msg.edit_text("🧠 **Подключение к нейросети (Gemini 3 PRO)...**")
    
    text_content = ""
    media_content = None
    mime_type = None

    try:
        if message.text:
            text_content = message.text
        elif message.photo:
            file_id = message.photo[-1].file_id
            media_content = reader.download_file(file_id, API_TOKEN)
            mime_type = "image/jpeg"
            text_content = message.caption or ""
        elif message.document:
            if message.document.mime_type in ["application/pdf", "image/jpeg", "image/png"]:
                media_content = reader.download_file(message.document.file_id, API_TOKEN)
                text_content = message.caption or ""
                mime_type = message.document.mime_type
            else:
                await status_msg.edit_text("❌ Формат не поддерживается.")
                return
        elif message.voice:
             media_content = reader.download_file(message.voice.file_id, API_TOKEN)
             mime_type = "audio/ogg"
             text_content = "Распознай голосовое сообщение"

        # CALL GEMINI
        result = await reader.analyze_content(text_content, media_content, mime_type, mode)
        raw_response = result.get("raw_text", "Ошибка генерации.")
        
        final_text = raw_response + "\n\n░░░░░░░░░░ [80% Готово]\n🔒 **Полный прогноз скрыт.**"

        input_preview = text_content[:50] if text_content else "Media file"
        add_to_history(user_id, mode, input_preview, raw_response[:80])

        # VOICE
        try:
            lang = "ru" if "ru" in (message.from_user.language_code or "en") else "en"
            voice_text = raw_response.split("\n")[0]
            if len(voice_text) < 50: voice_text = raw_response[:200]
            voice_text_clean = voice_text.replace("*", "").replace("#", "").replace("🚩", "")
            
            await bot.send_chat_action(message.chat.id, "record_voice")
            intro = LOCALES[lang]["voice_intro"]
            voice_path = await generate_voice(f"{intro}... {voice_text_clean}", folder="assets")
            await message.answer_voice(types.InputFile(voice_path), caption="🎙 **AI Summary**")
        except Exception as e:
            print(f"Voice Error: {e}")

        # BUTTON
        btn_key = f"buy_{mode}"
        btn_text = LOCALES[lang]["buttons"].get(btn_key, LOCALES[lang]["buttons"]["buy_red_flag"]) 
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=btn_text, callback_data=f"buy_{mode}")]])

        await status_msg.edit_text(final_text, parse_mode="Markdown", reply_markup=keyboard)

    except Exception as e:
        await status_msg.edit_text(f"⚠️ Ошибка: {str(e)}")


# --- PAYMENT HANDLERS ---

@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def send_invoice(callback: types.CallbackQuery):
    mode = callback.data.split("_")[1]
    user_id = callback.from_user.id
    stats = get_referral_stats(user_id)
    
    if stats["credits"] > 0:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎫 Использувать кредит (FREE)", callback_data=f"credit_{mode}")],
            [InlineKeyboardButton(text="💳 Оплатить Stars", callback_data=f"pay_{mode}")]
        ])
        await callback.message.answer(f"💎 **У тебя {stats['credits']} кредит(ов)!**", reply_markup=keyboard)
        await callback.answer()
        return

    await process_payment(callback, mode)

@dp.callback_query_handler(lambda c: c.data.startswith("credit_"))
async def use_credit_callback(callback: types.CallbackQuery):
    mode = callback.data.split("_")[1]
    if use_credit(callback.from_user.id):
        set_user_mode(callback.from_user.id, f"{mode}_premium")
        await callback.message.answer("🔓 **PREMIUM АКТИВИРОВАН**\nПерешлите сообщение еще раз.")
    else:
        await callback.message.answer("⚠️ Недостаточно кредитов.")
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data.startswith("pay_"))
async def pay_with_stars(callback: types.CallbackQuery):
    mode = callback.data.split("_")[1]
    await process_payment(callback, mode)

async def process_payment(callback: types.CallbackQuery, mode: str):
    prices = {"red_flag": 50, "dream": 25, "med": 100, "paper": 250, "psycho": 70, 
              "prompts": 30, "market": 150, "dome": 190, "alex_sales": 300, 
              "avito": 50, "angry": 50, "ex": 50, "boss": 50, "toast": 50}
    
    titles = {"red_flag": "🚩 Red Flag: Full Profile"} # Simplified for brevity, add others if needed or rely on default
    title = titles.get(mode, "Premium Report")
    
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=title,
        description="Полный отчет + прогноз.",
        payload=mode,
        provider_token="",
        currency="XTR",
        prices=[types.LabeledPrice(label="Premium Access", amount=prices.get(mode, 50))],
        start_parameter="premium-buy"
    )
    await callback.answer()

@dp.pre_checkout_query_handler(lambda q: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    mode = message.successful_payment.invoice_payload
    set_user_mode(message.from_user.id, f"{mode}_premium")
    await message.answer("✅ **Оплата принята!**\n🔓 **PREMIUM АКТИВИРОВАН**\nПерешлите сообщение еще раз для полного анализа.")


if __name__ == '__main__':
    print("🚩 RED FLAG BOT (Aiogram 2.x) STARTED")
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        print(f"Bot Error: {e}")
