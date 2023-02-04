from typing import Any
from aiohttp import ClientSession
from yarl import URL
from telegram_bot_zoo.clients.client import Client

from telegram_bot_zoo.models.base_model import TelegramBaseModel
from pydantic import Field


class TranslateRequest(TelegramBaseModel):
    folder_id: str = Field(alias="folderId")
    texts: list[str]
    target_language_code: str = Field("ru", alias="targetLanguageCode")
    source_language_code: str = Field("en", alias="sourceLanguageCode")


class YaTranslatorClient(Client):
    def __init__(
        self,
        session: ClientSession,
        base_url: URL | str,
        folder_id: str,
        iam_token: str,
    ) -> None:
        super().__init__(session, base_url)
        self.folder_id: str = folder_id
        self.base_headers: dict[str, str] = {"Authorization": f"Bearer {iam_token}"}

    async def translate(self, sentence: str) -> str:
        url: URL = self.base_url.with_path("translate/v2/translate")
        body: dict[str, Any] = TranslateRequest(
            folder_id=self.folder_id,
            texts=[sentence],
        ).dict(by_alias=True)

        async with self.session.post(url, headers=self.base_headers, json=body) as resp:
            data = await resp.json()
            return data["translations"][0]["text"]
