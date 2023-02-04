from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from telegram_bot_zoo.database import Base


class Logs(Base):
    __tablename__: str = "logs"

    id: Column[int] = Column("id", Integer, primary_key=True, autoincrement=True)
    source: Column[str] = Column("source", String)
    bot_name: Column[str] = Column("bot_name", String)
    created_at: Column[datetime] = Column("created_at", DateTime, nullable=False)
    level: Column[str] = Column("level", String, nullable=False)
    filename: Column[str] = Column("filename", String, nullable=False)
    message: Column[str] = Column("message", String)
