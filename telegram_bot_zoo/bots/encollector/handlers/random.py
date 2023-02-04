from dependency_injector.wiring import Provide, inject
from telegram import CallbackQuery, InlineKeyboardMarkup, Update, InlineKeyboardButton
from loguru import logger
import json

from telegram.ext import CommandHandler, CallbackQueryHandler

from telegram_bot_zoo.bots.encollector.context import EnCollectorContext
from telegram_bot_zoo.bots.encollector.handlers.models import EventType, UserEvent
from telegram_bot_zoo.containers import Container
from telegram_bot_zoo.database.models.word_info import GuessInfo
from telegram_bot_zoo.database.repo import Repo


def get_query_message(word: str) -> str:
    return f"Do you remember word: {word}?"


@inject
async def random_word(
    update: Update, context: EnCollectorContext, repo: Repo = Provide[Container.repo]
) -> None:
    guess_info: GuessInfo | None = await repo.random_guess(context._chat_id)
    if guess_info is None:
        await context.bot.send_message(
            context._chat_id, "You haven't any word in your dictionary"
        )
        return

    event_yes: UserEvent = UserEvent(
        type=EventType.CHECK, details=f"yes,{guess_info.guess_id}"
    )
    event_no: UserEvent = UserEvent(
        type=EventType.CHECK, details=f"no,{guess_info.guess_id}"
    )

    event_id_yes: int = await repo.add_event(event_yes.json())
    event_id_no: int = await repo.add_event(event_no.json())

    logger.info(f'Send "{guess_info.word}" in chat_id: {context._chat_id}')

    keyboard: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton("Yes", callback_data=f"yes {event_id_yes}"),
            InlineKeyboardButton("No", callback_data=f"no {event_id_no}"),
        ],
    ]

    reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        context._chat_id, get_query_message(guess_info.word), reply_markup=reply_markup
    )


async def construct_more_markup(repo: Repo, chat_id: str) -> InlineKeyboardMarkup:
    event_more: UserEvent = UserEvent(type=EventType.REPEAT, details="more")
    event_enough: UserEvent = UserEvent(type=EventType.REPEAT, details="enough")
    event_id_more: int = await repo.add_event(event_more.json())
    event_id_enough: int = await repo.add_event(event_enough.json())

    keyboard: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton("More", callback_data=f"more {event_id_more}"),
            InlineKeyboardButton("Enough", callback_data=f"enough {event_id_enough}"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


@inject
async def check_query(
    update: Update, context: EnCollectorContext, repo: Repo = Provide[Container.repo]
) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query: CallbackQuery = update.callback_query
    await query.answer()

    event_id: str = query.data.split(" ")[1]
    event_raw: str = await repo.get_event_data(event_id)
    event: UserEvent = UserEvent.parse_obj(json.loads(event_raw))
    ans, guess_id = event.details.split(",")
    guess_info: GuessInfo = await repo.get_guess_by_id(int(guess_id))
    await query.edit_message_text(text=get_query_message(guess_info.word))

    if ans == "yes":
        await context.bot.send_message(context._chat_id, text="Nice work!")
    else:
        await context.bot.send_message(
            context._chat_id,
            text=f"Translation: {guess_info.translation}\n"
            f"Transcription: {guess_info.transcription}\n",
        )

    markup: InlineKeyboardMarkup = await construct_more_markup(repo, context._chat_id)
    await context.bot.send_message(
        context._chat_id, text="Want more?", reply_markup=markup
    )


@inject
async def repeat_query(
    update: Update, context: EnCollectorContext, repo: Repo = Provide[Container.repo]
) -> None:
    query: CallbackQuery = update.callback_query
    event_id: str = query.data.split(" ")[1]
    event_raw: str = await repo.get_event_data(event_id)
    event: UserEvent = UserEvent.parse_obj(json.loads(event_raw))
    await query.edit_message_text(text="Want more?")

    if event.details == "more":
        await random_word(update, context, repo=repo)
    else:
        await query.answer()


random_word_handlers: list = [
    CommandHandler("random", random_word),
    CallbackQueryHandler(check_query, pattern="^(yes|no)"),
    CallbackQueryHandler(repeat_query, pattern="^(more|enough)"),
]
