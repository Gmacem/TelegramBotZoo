from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, null

from en_collector.database import Base


class Clients(Base):
    __tablename__: str = 'clients'
    chat_id: Column[str] = Column('chat_id', String, primary_key=True)


class Words(Base):
    __tablename__: str = 'words'

    id: Column[int] = Column('id', int, primary_key=True)
    word: Column[str] = Column('word', String, unique=True, nullable=False)
    transcription: Column[str] = Column('transcription', String)
    translations: Column[str] = Column('default_translation', String)


class Guesses(Base):
    __tablename__: str = 'guesses'

    id: Column[int] = Column('id', int, primary_key=True)
    word_id: Column[int] = Column('word_id', ForeignKey('words.id'))
    success_count: Column[int] = Column('success_count', Integer, nullable=False, default=0)
    failure_count: Column[int] = Column('failure_count', Integer, nullable=False, default=0)
    last_try_at: Column[datetime] = Column('last_try_at', DateTime)
    user_translation: Column[str] = Column('user_translation', String)