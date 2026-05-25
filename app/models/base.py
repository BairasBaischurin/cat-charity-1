from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Integer, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base as DeclarativeBase, CommonMixin


class Base(CommonMixin, DeclarativeBase):
    """Базовый абстрактный класс для проектов и пожертвований."""

    __abstract__ = True

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            'invested_amount >= 0',
            name='check_invested_amount_not_negative'
        ),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_amount_limit'
        ),
    )

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    def close(self) -> None:
        """Переводит объект в статус полностью проинвестированного."""
        self.fully_invested = True
        self.close_date = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        """Отладочный метод."""
        return (
            f'<{self.__class__.__name__}(id={self.id}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested})>'
        )
