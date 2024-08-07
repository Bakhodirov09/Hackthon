from fastapi import Depends, Body

from bot.misc import bot
from API.schemas.send_message import SendMessageSchema
from API.views.send_message.router import router
from API.config import create_session

@router.post('/')
async def send_message(data: SendMessageSchema = Body()):
    await bot.send_message(chat_id=data.chat_id, text=data.text)