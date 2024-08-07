from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

async def button():
    return ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text = "🚮 Chiqindi to'plangan joy"),
                KeyboardButton(text = "🚫 Qoidabuzarlik")
            ],
            [
                KeyboardButton(text = "🚒 Yong'in"),
                KeyboardButton(text = "🚓 Politsiya")
            ],
            [
                KeyboardButton(text = "🚑 Tez yordam"),
                KeyboardButton(text = "↩️ Boshqa")
            ],
            [
                KeyboardButton(text = "⬅️ Orqaga")
            ]
        ],
        resize_keyboard = True
    )