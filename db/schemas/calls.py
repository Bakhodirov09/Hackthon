from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.config import BaseModel

class CallsTable(BaseModel):
    __tablename__ = 'calls_call'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users_user.id'))
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()

    user: Mapped["UsersTable"] = relationship(back_populates="calls")
    files: Mapped[list["CallFilesTable"]] = relationship(back_populates="call")


class CallFilesTable(BaseModel):
    __tablename__ = 'calls_callfile'

    call_id: Mapped[int] = mapped_column(ForeignKey('calls_call.id'))
    file: Mapped[str] = mapped_column()

    call: Mapped["CallsTable"] = relationship(back_populates="files")
