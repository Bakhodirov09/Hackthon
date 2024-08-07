from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def button(skip: bool = False):
    return ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "➡️ O'tkazib yuborish")],
            [KeyboardButton(text = "⬅️ Orqaga")]
        ] if skip else [[KeyboardButton(text = "⬅️ Orqaga")]],
        resize_keyboard = True
    )