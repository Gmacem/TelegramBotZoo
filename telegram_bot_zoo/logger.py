from loguru import logger
from dependency_injector.wiring import Provide, inject
from telegram_bot_zoo.containers import Container
from telegram_bot_zoo.database.repo import Repo
from telegram_bot_zoo.env import SOURCE
from typing import Any


@inject
async def write_log_db(message, repo: Repo = Provide[Container.repo]):
    record: dict[str, Any] = message.record
    filename: str = f"{record['file']}:{record['function']}:{record['line']}"
    await repo.add_log(
        source=SOURCE,
        bot_name=record.get("bot_name", None),
        created_at=record["time"],
        level=record["level"].name,
        filename=filename,
        message=record["message"],
    )


logger.add(write_log_db)
