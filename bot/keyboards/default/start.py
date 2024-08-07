from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def button():
    return ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text = "➡️ Login"),
                KeyboardButton(text = "➡️ Ro'yxatdan o'tish")
            ]
        ],
        resize_keyboard = True
    )