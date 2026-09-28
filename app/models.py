"""
SQLAlchemy ORM models. Alembic autogenerate diffs against Base.metadata,
so every table you want tracked needs to inherit from Base and be
imported somewhere env.py can see it (see alembic/env.py).
"""
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(datetime.timezone.utc))

    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class Post(Base):
    """Added after the initial migration — run `alembic revision --autogenerate`
    again and it picks this up as a new table automatically."""
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(datetime.timezone.utc))

    author: Mapped["User"] = relationship(back_populates="posts")
