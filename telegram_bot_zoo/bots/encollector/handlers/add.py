from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.ext import MessageHandler, filters

from telegram_bot_zoo.bots.encollector.context import EnCollectorContext
from telegram_bot_zoo.clients.ya_dictionary import (
    TranslateWithTranscription,
    YaDictionaryClient,
)
from telegram_bot_zoo.clients.ya_translator import YaTranslatorClient
from telegram_bot_zoo.containers import Container
from telegram_bot_zoo.database.repo import Repo
from loguru import logger


@inject
async def add(
    update: Update,
    context: EnCollectorContext,
    repo: Repo = Provide[Container.repo],
    ya_dictionary: YaDictionaryClient = Provide[Container.ya_dictionary_client],
    ya_translator: YaTranslatorClient = Provide[Container.ya_translator_client],
) -> None:
    try:
        user_says: str = update.message.text
        if " " in user_says:
            await update.message.reply_text("Sentence translation isn't implemented")
            # word: str = await ya_translator.translate(user_says)
        else:
            tr: TranslateWithTranscription = await ya_dictionary.translate(user_says)
            translations: str | None = None
            if len(tr.translations) > 0:
                translations: str = ",".join(tr.translations).lower()
            id: int = await repo.get_or_add_word(
                user_says, translations, tr.transcription
            )

            await repo.get_or_add_guess(
                id,
                context._chat_id,
            )
            await update.message.reply_text(
                f"Translation: {translations}\nTranscription: {tr.transcription}\n"
            )
    except Exception as ex:
        logger.exception(ex)
        await update.message.reply_text("I don't know that word")


add_handlers: list = [MessageHandler(filters.TEXT & ~filters.COMMAND, add)]
