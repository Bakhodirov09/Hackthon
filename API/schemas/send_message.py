from API.schemas.base import BaseSchema
from pydantic import Field


class SendMessageSchema(BaseSchema):
    text: str = Field(..., title="text")
    chat_id: int = Field(..., title="chat_id")