from enum import Enum

from telegram_bot_zoo.models.base_model import TelegramBaseModel


class EventType(str, Enum):
    CHECK: str = "CHECK"
    REPEAT: str = "REPEAT"


class UserEvent(TelegramBaseModel):
    type: EventType
    details: str | None
