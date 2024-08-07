from aiogram import Dispatcher

from bot.middlewares.create import CreateUserMiddleware

from bot.filters.chat_type import Chat
from bot.filters.content_type import ContentType
from bot.filters.text import Text
from bot.filters.permission import Permission


async def setup_middlewares(dispatcher: Dispatcher):
    dispatcher.message.middleware(CreateUserMiddleware())

async def setup_filters(dispatcher: Dispatcher):
    dispatcher.message.filter(Chat)
    dispatcher.message.filter(Text)
    dispatcher.message.filter(ContentType)
    dispatcher.message.filter(Permission)
