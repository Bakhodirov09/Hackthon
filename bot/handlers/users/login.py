from aiogram import types, html
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.routers import users
from bot.keyboards.default import send
from bot.keyboards.default import menu
from bot.filters import Chat, Text, ContentType
from bot.states.auth import LoginState, LoginOrRegisterState

from db import repository as repo
from db.utils.hash import check_password


@users.message(Chat().is_private(), Text(text = "➡️ Login"), StateFilter(LoginOrRegisterState.command))
@create_session
async def login_handler(message: types.Message, state: FSMContext, session: Session):
    await state.clear()

    user = await repo.ContactsTableRepository().get_user(
        user_id=message.from_user.id, session=session)

    await state.set_state(LoginState.phone_number)
    await message.answer(
        text = (
            html.bold(f"Telfon raqamingizni yuboring") + "\n\n" +
            html.italic('Masalan: +998xxxxxxx yoki "📞Telefon raqam yuborish" tugmasini bosing')
        ),
        reply_markup = await send.button(phone_number=True)
    )


@users.message(Chat().is_private(),
               ContentType([ContentType.CONTACT]),
               StateFilter(LoginState.phone_number))
@create_session
async def phone_number_login_handler(message: types.Message, state: FSMContext, session: Session):
    phone_numbers = await repo.UsersTableRepository().get_phone_numbers(session=session)
    phone_numbers = [data['phone_number'] for data in phone_numbers]

    user_phone_number = ((message.contact.phone_number) 
                         if str(message.contact.phone_number).startswith("+") else
                         f"+{message.contact.phone_number}")

    if user_phone_number in phone_numbers:
        await state.update_data(phone_number = user_phone_number, tries = 5)
        await state.set_state(LoginState.password)
        await message.answer(
            text = html.bold("Parol yuboring 🔐"), reply_markup = types.ReplyKeyboardRemove())
    else:
        await message.answer(html.bold("Telefon raqam topilmadi ❌"))


@users.message(Chat().is_private(),
               ContentType([ContentType.TEXT]), 
               StateFilter(LoginState.phone_number))
@create_session
async def phone_number_text_login_handler(message: types.Message, state: FSMContext, session: Session):
    phone_numbers = await repo.UsersTableRepository().get_phone_numbers(session=session)
    phone_numbers = [data['phone_number'] for data in phone_numbers]

    if message.text.startswith("+") and len(message.text.split()) == 1 and not " " in message.text:
        try:
            phone_number = int(message.text[1:])

            if message.text.startswith("+998"):
                if len(message.text) == 13:
                    phone_number = message.text
                else: 
                    await message.answer(html.bold("Siz noto'g'ri raqam kiritdingiz ❌"))
                    return
            else:
                await message.answer(html.bold("Telefon raqam +998 bilan boshlanishi kerak ❌"))
                return
        except ValueError:
            await message.answer(html.bold("Siz noto'g'ri formatda raqam kiritdingiz ❌"))
            return
    else:
        await message.answer(html.bold("Siz noto'g'ri formatda raqam kiritdingiz ❌"))
        return


    if phone_number in phone_numbers:
        await state.update_data(phone_number = phone_number, tries = 5)
        await state.set_state(LoginState.password)

        await message.answer(
            text = html.bold("Parol yuboring 🔐"), reply_markup = types.ReplyKeyboardRemove())
    else:
        await message.answer(html.bold("Telefon raqam topilmadi ❌"))


@users.message(Chat().is_private(),
               ContentType(ContentType.TEXT),
               StateFilter(LoginState.password))
@create_session
async def password_login_hanlder(message: types.Message, state: FSMContext, session: Session):
    password = message.text
    data = await state.get_data()

    phone_number = data['phone_number']
    user = await repo.UsersTableRepository().get_user(phone_number=phone_number, session=session)


    if user.check_password(password):
        await repo.UsersTableRepository().login_with_telegram(
            tg_id=message.from_user.id, phone_number=phone_number, session=session)

        await state.clear()
        await message.answer(html.bold("Siz muvafaqiyatli hisobingizga kirdingiz ✅"), 
                             reply_markup = await menu.button())
    else:
        if data['tries'] - 1 == 0:
            await message.answer(html.bold("Juda ko'p xarakat qildingiz, keyinroq urinib koring 😔"))
            return

        await state.update_data(tries = data['tries'] - 1)
        await message.answer(text = (
            html.bold("Siz noto'g'ri parol kiritdingiz ❌") + "\n\n" +
            html.italic(f"🔄 Qolgan urinishlar soni: {data['tries'] - 1}")
        ))

