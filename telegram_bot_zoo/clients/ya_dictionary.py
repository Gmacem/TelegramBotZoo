from aiohttp import ClientSession
from telegram_bot_zoo.clients.client import Client
from yarl import URL
from telegram_bot_zoo.models.base_model import TelegramBaseModel
from pydantic import Field


class YaDictionaryTranslateItem(TelegramBaseModel):
    text: str


class YaDictionaryDefItem(TelegramBaseModel):
    text: str
    transcription: str = Field(alias="ts")
    pos: str
    ts: str | None
    tr: list[YaDictionaryTranslateItem]


class YaDictionaryResponse(TelegramBaseModel):
    items: list[YaDictionaryDefItem] = Field(alias="def")


class TranslateWithTranscription(TelegramBaseModel):
    text: str
    translations: list[str] = Field(default_factory=list)
    transcription: str


class YaDictionaryClient(Client):
    def __init__(
        self, session: ClientSession, base_url: URL | str, api_key: str
    ) -> None:
        super().__init__(session, base_url)
        self.api_key: str = api_key

    async def translate(self, text: str) -> TranslateWithTranscription:
        url: URL = self.base_url.with_path("api/v1/dicservice.json/lookup").with_query(
            key=self.api_key, lang="en-ru", text=text
        )

        async with self.session.get(url) as resp:
            data: YaDictionaryResponse = YaDictionaryResponse.parse_obj(
                await resp.json()
            )
            result: TranslateWithTranscription = TranslateWithTranscription(
                text=text,
                translations=[],
                transcription=data.items[0].ts,
            )
            for item in data.items:
                if len(item.tr) > 0:
                    result.translations.append(item.tr[0].text)
            return result
