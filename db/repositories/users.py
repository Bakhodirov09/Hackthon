from db import repository as repo
from db.repository import BaseRepository
from db.schemas import UsersTable, ContactsTable
from db.utils.hash import hash_password

from sqlalchemy import select
from sqlalchemy.orm import Session


class ContactsTableRepository(BaseRepository):
    table = ContactsTable

    async def get_user(self, user_id: int, session: Session) -> table:
        user = self.get(attribute="user_id", value=user_id, session=session)

        return user

    async def create_user(self, user_id: int, username: str | None, full_name: str,
                          session: Session, update: bool = False):
        user = await self.get_user(user_id=user_id, session=session)

        if not user:
            self.create(params={
                "user_id": user_id,
                "name": full_name,
                "username": username
            }, session=session)
            
        if update:
            self.edit(conditions={"user_id": user_id}, edits={
                "username": username,
                "name": full_name
            }, session=session)

        return None


class UsersTableRepository(BaseRepository):
    table = UsersTable

    async def create_user(self, full_name: str, phone_number: str, password: str, session: Session):
        self.create(params={
            "full_name": full_name,
            "phone_number": phone_number,
            "password": hash_password(password)
        }, session=session)

        return None
    
    async def get_phone_numbers(self, session: Session):
        phone_numbers = (session.execute(select(self.table.phone_number))).mappings().all()

        return phone_numbers
    
    async def get_user(self, phone_number: str, session: Session) -> table:
        user = self.get(attribute="phone_number", value=phone_number, session=session)

        return user
    
    async def login_with_telegram(self, tg_id: int, phone_number: str, session: Session):
        contact = await repo.ContactsTableRepository().get_user(user_id=tg_id, session=session)

        self.edit(conditions={"phone_number": phone_number}, 
                  edits={"contact_id": contact.id}, session=session)
        repo.ContactsTableRepository().edit(
            conditions={"user_id": tg_id}, edits={"is_registered": True}, session=session)
    
    async def get_user_by_tg_id(self, tg_id: int, session: Session):
        contact = await repo.ContactsTableRepository().get_user(user_id=tg_id, session=session)

        user = (session.execute(
            select(self.table).where(self.table.contact_id == contact.id)
        )).scalar_one_or_none()

        return user