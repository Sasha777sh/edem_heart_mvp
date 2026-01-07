# Add this after the menu handlers, before payment handlers

@dp.message(Command("invite"))
async def cmd_invite(message: types.Message):
    """
    Show user their referral link and stats.
    """
    user_id = message.from_user.id
    user_lang = message.from_user.language_code or "en"
    lang = "ru" if "ru" in user_lang else "en"
    
    # Ensure user exists
    if not get_user(user_id):
        create_user(user_id, message.from_user.username or "", message.from_user.first_name or "User")
    
    stats = get_referral_stats(user_id)
    refs = stats["referrals"]
    credits = stats["credits"]
    
    # Generate referral link
    bot_username = (await bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    if lang == "ru":
        text = f"""
🎁 **РЕФЕРАЛЬНАЯ ПРОГРАММА**

Приглашай друзей и получай **бесплатные прогоны**!

📊 **Твоя статистика:**
• Приглашено: {refs}
• Кредиты: {credits} 🎫

🔗 **Твоя ссылка:**
`{ref_link}`

💡 **Как работает:**
• Приглашай друзей через свою ссылку
• За каждые 3 реферала = 1 кредит
• 1 кредит = 1 бесплатный Deep-анализ

Используй /premium для прогона за кредиты.
        """
    else:
        text = f"""
🎁 **REFERRAL PROGRAM**

Invite friends and get **free analyses**!

📊 **Your stats:**
• Invited: {refs}
• Credits: {credits} 🎫

🔗 **Your link:**
`{ref_link}`

💡 **How it works:**
• Invite friends via your link
• Every 3 referrals = 1 credit
• 1 credit = 1 free Deep analysis

Use /premium to redeem credits.
        """
    
    await message.answer(text, parse_mode="Markdown")
