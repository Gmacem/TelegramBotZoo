from typing import Generator
from aiohttp import ClientSession
from dependency_injector import containers, providers
from dependency_injector.providers import Configuration, Factory
from telegram_bot_zoo.database import async_session

from telegram_bot_zoo.clients.ya_translator import YaTranslatorClient
from telegram_bot_zoo.clients.ya_dictionary import YaDictionaryClient
from telegram_bot_zoo.database.repo import Repo
from telegram_bot_zoo.env import (
    CLIENTS_YA_DICTIONARY_API_KEY,
    CLIENTS_YA_DICTIONARY_BASE_URL,
    CLIENTS_YA_TRANSLATOR_BASE_URL,
    CLIENTS_YA_TRANSLATOR_FOLDER_ID,
    CLIENTS_YA_TRANSLATOR_IAM_TOKEN,
)


async def init_client_session() -> Generator:
    async with ClientSession() as session:
        yield session


async def init_repo_session() -> Generator:
    async with async_session() as session:
        yield session


class Container(containers.DeclarativeContainer):
    config: Configuration = providers.Configuration()

    cli_session: providers.Resource = providers.Resource(
        init_client_session,
    )

    repo_session: providers.Resource = providers.Resource(
        init_repo_session,
    )

    ya_translator_client: Factory[YaTranslatorClient] = providers.Factory(
        YaTranslatorClient,
        cli_session,
        CLIENTS_YA_TRANSLATOR_BASE_URL,
        CLIENTS_YA_TRANSLATOR_FOLDER_ID,
        CLIENTS_YA_TRANSLATOR_IAM_TOKEN,
    )

    ya_dictionary_client: Factory[YaDictionaryClient] = providers.Factory(
        YaDictionaryClient,
        cli_session,
        CLIENTS_YA_DICTIONARY_BASE_URL,
        CLIENTS_YA_DICTIONARY_API_KEY,
    )

    repo: Factory[Repo] = providers.Factory(
        Repo,
        repo_session,
    )
