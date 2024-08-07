from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def button():
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "✏️ Parolni o'zgartirish", callback_data = 'change_password')
            ]
        ]
    )