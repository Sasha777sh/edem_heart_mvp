
# 🎛 BOT MENU ARCHITECTURE

GOAL: Allow users to switch modes without deep links.

## 1. REPLY KEYBOARD (Persistent)
Buttons:
[ 🌙 Dream ] [ 🩸 Med ]
[ 🚩 RedFlag ] [ 📝 Paper ]
[ 🎬 Reels ]

## 2. COMMANDS
`/menu` -> Shows inline keyboard with descriptions.
`/start` -> Shows localized welcome + Reply Keyboard.

## 3. IMPLEMENTATION in `run_bot.py`
- Import `ReplyKeyboardMarkup`, `KeyboardButton`.
- In `cmd_start`, send `reply_markup=main_menu`.
- Add handler `@dp.message(F.text == "🌙 Dream")` to switch mode.
