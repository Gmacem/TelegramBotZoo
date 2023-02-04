from fastapi import FastAPI

from telegram_bot_zoo.models.base_model import TelegramResponse

fastapi_app: FastAPI = FastAPI()


@fastapi_app.get("/health", status_code=200)
async def helath() -> TelegramResponse:
    return TelegramResponse(message="ok")
