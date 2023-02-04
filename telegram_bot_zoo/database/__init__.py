from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from telegram_bot_zoo.env import CONNECTION_STRING
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

async_engine = create_async_engine(
    CONNECTION_STRING, echo=True, isolation_level="AUTOCOMMIT"
)
Base = declarative_base()
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    async_engine, expire_on_commit=False
)
