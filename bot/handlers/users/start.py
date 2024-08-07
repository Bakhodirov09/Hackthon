from aiogram import types, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.routers import users
from bot.keyboards.default import start, menu
from bot.filters import Chat
from bot.states.auth import LoginOrRegisterState
from db import repository as repo


@users.message(Chat().is_private(), CommandStart())
@create_session
async def start_handler(message: types.Message, state: FSMContext, session: Session):
    user = await repo.ContactsTableRepository().get_user(
        user_id=message.from_user.id, session=session)
    
    if not user.is_registered:
        await state.set_state(LoginOrRegisterState.command)
        await message.answer(text = (
            html.bold(f"Salom {message.from_user.first_name}") + "\n\n" +
            html.italic(f"Kerakli bo'limni tanlang 👇")
        ), reply_markup = await start.button())
    else:
        await message.answer(html.bold("Kerakli bo'limni tanlang 👇"), 
                             reply_markup = await menu.button())