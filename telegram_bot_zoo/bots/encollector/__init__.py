from fastapi import APIRouter, Request
from loguru import logger
from pydantic import BaseModel
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from dependency_injector.wiring import Provide, inject

from yarl import URL
from telegram_bot_zoo.bots.encollector.context import EnCollectorContext
from telegram_bot_zoo.containers import Container
from telegram_bot_zoo.database.repo import Repo

from telegram_bot_zoo.env import ADMIN_CHAT_ID, BASE_URL, BOTS_ENCOLLECTOR_TOKEN
from telegram_bot_zoo.models.response import BotResponse
from telegram_bot_zoo.bots.encollector.handlers.add import add_handlers
from telegram_bot_zoo.bots.encollector.handlers.random import random_word_handlers


encollector_router: APIRouter = APIRouter(
    prefix="/api/en_collector",
    tags=["EnCollector"],
)

application: Application = None


@encollector_router.post("/telegram")
async def telegram(request: Request) -> BotResponse:
    await application.update_queue.put(
        Update.de_json(data=await request.json(), bot=application.bot)
    )
    return BotResponse(message="ok")


class WebhookUpdate(BaseModel):
    user_id: int
    payload: str


async def do_nothing(update: Update, context: EnCollectorContext) -> None:
    await update.message.reply_text(text="I don't understand you")


@inject
async def start(
    update: Update, context: EnCollectorContext, repo: Repo = Provide[Container.repo]
) -> None:
    text: str = (
        "Commands:\n\n"
        "<code>/add {{word}}</code> - add word in a personal dictionary\n"
        "<code>/random</code> - get a random word\n"
    )
    await repo.add_chat(context._chat_id, context._user_id)
    await update.message.reply_html(text=text)


async def setup_encollector() -> Application:
    url: URL = URL(BASE_URL)
    admin_chat_id: str = ADMIN_CHAT_ID

    context_types = ContextTypes(context=EnCollectorContext)

    global application

    application = (
        Application.builder()
        .token(BOTS_ENCOLLECTOR_TOKEN)
        .updater(None)
        .context_types(context_types)
        .build()
    )

    application.bot_data["url"] = url
    application.bot_data["admin_chat_id"] = admin_chat_id

    application.add_handlers(add_handlers)
    application.add_handler(CommandHandler("start", start))
    application.add_handlers(random_word_handlers)
    webhook_url: URL = url.with_path("/api/en_collector/telegram")

    logger.info("Webhook url: {}", webhook_url)

    await application.bot.set_webhook(
        url=str(webhook_url)
    )  # certificate=CERTIFICATE_PATH)

    return application
