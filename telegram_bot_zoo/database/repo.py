from datetime import datetime
from sqlalchemy import text
from loguru import logger
from telegram_bot_zoo.database.models.word_info import GuessInfo
from sqlalchemy.ext.asyncio import AsyncSession


class Repo:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def add_chat(self, chat_id: int, user_id: int) -> None:
        logger.info("Add client with chat_id: {}", chat_id)
        await self.session.execute(
            text(
                "INSERT INTO clients (chat_id, user_id) "
                f"VALUES ({chat_id}, {user_id})"
            )
        )

    async def get_or_add_word(
        self, word: str, translation: str, transcription: str
    ) -> int:
        found = await self.session.execute(
            text("SELECT id FROM words " f"WHERE word like '{word}';")
        )
        found = found.all()
        if len(found) == 0:
            result = await self.session.execute(
                text(
                    "INSERT INTO words (word, translation, transcription) "
                    f"VALUES ('{word}', '{translation}', '{transcription}') "
                    "RETURNING id;"
                )
            )

            return result.scalar()
        return found[0][0]

    async def get_or_add_guess(self, word_id: int, chat_id: int) -> int:
        result = await self.session.execute(
            text(
                "INSERT INTO guesses (word_id, chat_id, success_count, failure_count) "
                f"VALUES ({word_id}, {chat_id}, 0, 0) "
                "RETURNING id;"
            )
        )

        return result.scalar()

    async def random_guess(self, chat_id: int) -> GuessInfo | None:
        result = await self.session.execute(
            text(
                "SELECT guesses.id AS guess_id, words.word, words.id AS word_id, chat_id, "
                "transcription, translation, -LOG(random()) AS priority "
                "FROM guesses "
                "JOIN words on guesses.word_id=words.id "
                f"WHERE chat_id={chat_id} "
                "ORDER BY priority LIMIT 1;"
            )
        )
        result = result.all()
        if len(result) == 0:
            return None
        return GuessInfo.parse_obj(result[0]._mapping)

    async def get_guess_by_id(self, word_id: int) -> GuessInfo:
        result = await self.session.execute(
            text(
                "SELECT guesses.id AS guess_id, words.id AS word_id, word, chat_id, "
                "transcription, translation, -LOG(random()) AS priority "
                "FROM guesses "
                "JOIN words on guesses.word_id=words.id "
                f"WHERE word_id={word_id} "
                "ORDER BY priority LIMIT 1;"
            )
        )
        result = result.one()
        return GuessInfo.parse_obj(result._mapping)

    async def add_event(self, data: str) -> str:
        id = await self.session.execute(
            text(f"INSERT INTO events (data) VALUES ('{data}')" "RETURNING id;")
        )
        return id.scalar()

    async def get_event_data(self, id: int) -> str:
        result = await self.session.execute(
            text(f"SELECT (data) FROM events " f"WHERE id={id};")
        )
        return result.scalar()

    async def add_log(
        self,
        source: str,
        bot_name: str | None,
        created_at: datetime,
        level: int,
        filename: str,
        message: str,
    ) -> None:
        if bot_name is None:
            bot_name = "null"
        else:
            bot_name = f"'{bot_name}'"

        await self.session.execute(
            text(
                "INSERT INTO logs (source, bot_name, created_at, level, filename, message) "
                f"VALUES ('{source}', {bot_name}, '{created_at}', '{level}', '{filename}', '{message}');"
            )
        )
