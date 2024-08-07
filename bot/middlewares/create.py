from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.enums import ChatType

from sqlalchemy.orm import Session
from db import repository as repo
from bot.decorators import create_session


class CreateUserMiddleware(BaseMiddleware):
    @create_session
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
                       event: TelegramObject, data: Dict[str, Any], session: Session) -> Any:
        event_data = event.dict()

        if event_data['chat']['type'] == ChatType.PRIVATE:
            await repo.ContactsTableRepository().create_user(
                user_id = event_data['from_user']['id'],
                username = event_data['from_user']['username'],
                full_name = (event_data['from_user']['first_name'] +
                        (" " + event_data['from_user']['last_name'] 
                        if event_data['from_user']['last_name'] else "")),
                session = session, update = True
            )
        
        return await handler(event, data)