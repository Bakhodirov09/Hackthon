from aiogram.filters import Filter
from aiogram.types import TelegramObject
from sqlalchemy.orm import Session

from bot.decorators import create_session
from apps.general.choices import RolesChoices

from db import repository as repo


class Permission(Filter):
    USER = RolesChoices.user
    STAFF = RolesChoices.staff
    MANAGER = RolesChoices.manager
    ADMIN = RolesChoices.admin
    CEO = RolesChoices.ceo

    def __init__(self, permission_classes: list):
        self.permission_classes = [self.CEO]
        self.permission_classes.extend(permission_classes)
        
    @create_session
    async def __call__(self, event: TelegramObject, session: Session, *args, **kwargs) -> bool:
        event_data = event.dict()
        user_id = event_data['from_user']['id']

        ...

        return None
    
    