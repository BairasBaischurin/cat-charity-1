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


class CommonBase(Base):
    """Базовый класс с предустановленным полем ID."""
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    def __repr__(self) -> str:
        """Текстовое представление объекта для отладки и логов."""
        return f'<{self.__class__.__name__}(id={self.id})>'


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    """Генератор сессии для FastAPI."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
