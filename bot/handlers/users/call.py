import geopy

from aiogram import types, html
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.routers import users
from bot.utils.address import get_address
from bot.filters import Chat, Text, ContentType

from bot.keyboards.inline import change_password
from bot.keyboards.default import call, back, send

from bot.states.call import CallState
from bot.states.auth import LoginState, LoginOrRegisterState

from db import repository as repo


CALL_TYPES = {
    "🚮 Chiqindi to'plangan joy": "waste",
    "🚫 Qoidabuzarlik": "fine",
    "🚒 Yong'in": "fire",
    "🚓 Politsiya": "police",
    "🚑 Tez yordam": "ambulance",
    "↩️ Boshqa": "other"
}


@users.message(Chat().is_private(), ContentType(['text']), StateFilter(CallState.type), 
               lambda message: str(message.text) in CALL_TYPES)
@create_session
async def call_type_handler(message: types.Message, state: FSMContext, session: Session):
    category = message.text

    await state.update_data(type=category)
    await state.set_state(CallState.title)
    await message.answer(html.bold("Sarvlavha kiriting 👇"), 
                         reply_markup = await back.button())


@users.message(Chat().is_private(), ContentType(['text']), StateFilter(CallState.title))
@create_session
async def call_title_handler(message: types.Message, state: FSMContext, session: Session):
    title = message.text

    if len(title) <= 255:
        await state.update_data(title=title)
        await state.set_state(CallState.description)
        await message.answer(html.bold("Holat haqida to'liqroq malumot (описание) kiriting 👇"),
                             reply_markup = await back.button(skip=True))
    else:
        await message.answer(html.bold("Sarvlavha 255 ta belgidan kam bo'lishi kerak ❌"))


@users.message(Chat().is_private(), ContentType(['text']), StateFilter(CallState.description))
@create_session
async def call_description_handler(message: types.Message, state: FSMContext, session: Session):
    description = message.text

    await state.update_data(description = (
        description if not description == "➡️ O'tkazib yuborish" else None))
    await state.set_state(CallState.file)
    await message.answer(html.bold("Holat bo'yicha rasm yoki video yuboring (1-6 tagacha) 👇"))


@users.message(Chat().is_private(), ContentType(['text']), 
               Text(text = "➡️ O'tkazib yuborish"), StateFilter(CallState.file))
@create_session
async def call_file_handler(message: types.Message, state: FSMContext, session: Session):
    skip = message.text

    await state.update_data(file=None)
    await state.set_state(CallState.location)
    await message.answer(html.bold("Joylashuv yuboring 📍"), 
                         reply_markup = await send.button(location=True))
    

@users.message(Chat().is_private(), ContentType([ContentType.LOCATION]), 
               StateFilter(CallState.location))
@create_session
async def call_location_handler(message: types.Message, state: FSMContext, session: Session):
    location = message.location
    address = await get_address(latitude=location.latitude, longitude=location.longitude)
    await message.answer(f"{address}")