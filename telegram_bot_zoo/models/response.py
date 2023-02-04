from telegram_bot_zoo.models.base_model import TelegramBaseModel


class BotResponse(TelegramBaseModel):
    message: str
