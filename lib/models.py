from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class TelegramMessageEntities(BaseModel):
    offset: int
    length: int
    type: str


class TelegramMessageChat(BaseModel):
    id: int
    first_name: str
    username: str
    type: str


class TelegramMessageFrom(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: Optional[str] = None


class TelegramMessageLocation(BaseModel):
    latitude: float
    longitude: float


class TelegramMessage(BaseModel):
    message_id: int
    from_: TelegramMessageFrom = Field(alias='from')
    chat: TelegramMessageChat
    date: datetime
    location: Optional[TelegramMessageLocation] = None
    text: Optional[str] = None
    entities: Optional[List[TelegramMessageEntities]] = None


class TelegramResult(BaseModel):
    update_id: int
    message: TelegramMessage


class TelegramUpdateResponse(BaseModel):
    ok: bool
    result: List[TelegramResult]
