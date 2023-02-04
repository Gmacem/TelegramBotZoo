from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean

from telegram_bot_zoo.database import Base


class Clients(Base):
    __tablename__: str = "clients"
    chat_id: Column[int] = Column("chat_id", Integer, primary_key=True)
    user_id: Column[int] = Column("user_id", Integer)


class Words(Base):
    __tablename__: str = "words"

    id: Column[int] = Column("id", Integer, primary_key=True, autoincrement=True)
    word: Column[str] = Column("word", String(500), unique=True, nullable=False)
    transcription: Column[str] = Column("transcription", String)
    translation: Column[str] = Column("translation", String)


class Guesses(Base):
    __tablename__: str = "guesses"

    id: Column[int] = Column("id", Integer, primary_key=True, autoincrement=True)
    chat_id: Column[int] = Column("chat_id", ForeignKey("clients.chat_id"))
    word_id: Column[int] = Column("word_id", ForeignKey("words.id"))
    success_count: Column[int] = Column(
        "success_count", Integer, nullable=False, default=0
    )
    failure_count: Column[int] = Column(
        "failure_count", Integer, nullable=False, default=0
    )
    last_query_at: Column[datetime] = Column("last_query_at", DateTime)
    last_reply_at: Column[datetime] = Column("last_reply_at", DateTime)
    is_success_last_time: Column[bool] = Column("is_success_last_time", Boolean)
    user_translation: Column[str] = Column("user_translation", String)


class Event(Base):
    __tablename__: str = "events"

    id: Column[int] = Column("id", Integer, primary_key=True, autoincrement=True)
    data: Column[String] = Column("data", String)
