from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.config import BaseModel


class NewsTable(BaseModel):
    __tablename__ = 'news_news'

    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    file: Mapped[str] = mapped_column()
    