from telegram_bot_zoo.models.base_model import TelegramBaseModel


class GuessInfo(TelegramBaseModel):
    guess_id: int
    word_id: int
    chat_id: str
    word: str
    translation: str | None
    transcription: str | None
