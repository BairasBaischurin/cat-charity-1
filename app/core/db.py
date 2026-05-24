from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, declared_attr
)

from app.core.config import settings


class Base(DeclarativeBase):
    """Автоматически выдаем имена таблицам."""

    __table_args__ = {'extend_existing': True}

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class CommonMixin:
    """Миксин для колонки id."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    """Генератор сессии для FastAPI."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
