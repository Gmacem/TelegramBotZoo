from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from en_collector.env import CONNECTION_STRING

engine = create_engine(CONNECTION_STRING)
Base = declarative_base()
