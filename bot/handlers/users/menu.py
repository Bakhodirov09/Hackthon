from aiogram import types, html
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.routers import users
from bot.keyboards.inline import change_password
from bot.keyboards.default import call
from bot.filters import Chat, Text, ContentType
from bot.states.auth import LoginState, LoginOrRegisterState
from bot.states.call import CallState

from db import repository as repo
from db.utils.hash import check_password


@users.message(Chat().is_private(), ContentType(['text']), Text(text = "👤 Mening akkauntim"))
@create_session
async def my_account_handler(message: types.Message, state: FSMContext, session: Session):
    contact = await repo.ContactsTableRepository().get_user(
        user_id=message.from_user.id, session=session)

    if contact.is_registered:
        user = await repo.UsersTableRepository().get_user_by_tg_id(
            tg_id=message.from_user.id, session=session)

        await message.answer(
            text = (html.bold(f"Sizning hisobingiz haqida malumotlar 👇") + "\n\n" +
                f"""{html.bold("📞 Telefon raqamingiz: ")} {html.italic(user.phone_number)}
{html.bold("👤 F.I.Sh: ")} {html.italic(user.full_name)}
{html.bold("💰 Ballaringiz: ")} {html.italic(user.points)} {html.italic("ball")}
{html.bold("🔐 Parolingiz: ")} {html.italic("********")}"""),
            reply_markup = await change_password.button())
        

@users.message(Chat().is_private(), ContentType(['text']), Text(text = "📞 Murojaat"))
@create_session
async def call_handler(message: types.Message, state: FSMContext, session: Session):
    contact = await repo.ContactsTableRepository().get_user(
        user_id=message.from_user.id, session=session)

    if contact.is_registered:
        user = await repo.UsersTableRepository().get_user_by_tg_id(
            tg_id=message.from_user.id, session=session)

        await state.set_state(CallState.type)
        await message.answer(
            text = html.bold(f"Kerakli bo'limni tanlang 👇"),
            reply_markup = await call.button())