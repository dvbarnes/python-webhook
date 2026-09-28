"""
Database setup: engine + session factory.

DATABASE_URL is read from the environment so local dev, CI, and
prod can each point at their own Postgres instance without code
changes. Falls back to a local dev default if unset.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
load_dotenv()
TEST_DB_URL = os.environ.get("DATABASE_URL")

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    TEST_DB_URL
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass
