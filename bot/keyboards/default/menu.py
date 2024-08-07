from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def button():
    return ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text = "👤 Mening akkauntim")
            ],
            [
                KeyboardButton(text = "📞 Murojaat")
            ]
        ],
        resize_keyboard = True
    )