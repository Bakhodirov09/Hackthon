from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def button(location: bool = False, phone_number: bool = False):
    return ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text = "📞 Telefon raqam yuborish", request_contact = True)
            ]
        ] if phone_number else [
            [
                KeyboardButton(text = "📍 Joylashuv yuborish", request_location = True)
            ]
        ],
        resize_keyboard = True
    )