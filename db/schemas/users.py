from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.config import BaseModel
from db.utils.hash import check_password
from apps.general.choices import RolesChoices


class ContactsTable(BaseModel):
    __tablename__ = 'users_contact'
    
    user_id: Mapped[int] = mapped_column(nullable=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column()
    is_blocked_bot: Mapped[bool] = mapped_column(default=False)
    is_registered: Mapped[bool] = mapped_column(default=False)

    users: Mapped[list["UsersTable"]] = relationship(back_populates="contact")


class UsersTable(BaseModel):
    __tablename__ = 'users_user'

    full_name: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey('users_contact.id'))
    points: Mapped[int] = mapped_column(default=0)
    role: Mapped[str] = mapped_column(default=RolesChoices.user)
    password: Mapped[str] = mapped_column(nullable=True)

    contact: Mapped["ContactsTable"] = relationship(back_populates="users")

    def check_password(self, password: str) -> bool:
        return check_password(password, self.password)