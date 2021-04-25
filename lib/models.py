from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union


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
    live_period: Optional[float] = None
    heading: Optional[float] = None
    horizontal_accuracy: Optional[float] = None


class TelegramPhoto(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    width: int
    height: int


class TelegramPhotoPathResponseResult(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    file_path: str


class TelegramPhotoPathResponse(BaseModel):
    ok: bool
    result: Optional[TelegramPhotoPathResponseResult] = None


class TelegramMessage(BaseModel):
    message_id: int
    from_: TelegramMessageFrom = Field(alias='from')
    chat: TelegramMessageChat
    photo: Optional[List[TelegramPhoto]] = None
    date: datetime
    location: Optional[TelegramMessageLocation] = None
    text: Optional[str] = None
    entities: Optional[List[TelegramMessageEntities]] = None


class TelegramEditedMessage(BaseModel):
    message_id: int
    from_: TelegramMessageFrom = Field(alias='from')
    chat: TelegramMessageChat
    photo: Optional[List[TelegramPhoto]] = None
    date: datetime
    location: Optional[TelegramMessageLocation] = None
    text: Optional[str] = None
    entities: Optional[List[TelegramMessageEntities]] = None


class TelegramCallbackQuery(BaseModel):
    id: int
    from_: TelegramMessageFrom = Field(alias='from')
    message: Optional[TelegramMessage] = None
    chat_instance: str
    data: str


class TelegramMessageResult(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None
    edited_message: Optional[TelegramEditedMessage] = None
    callback_query: Optional[TelegramCallbackQuery] = None


class TelegramUpdateResponse(BaseModel):
    ok: bool
    result: List[TelegramMessageResult]
