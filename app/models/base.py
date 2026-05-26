from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Integer, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import CommonBase


class Base(CommonBase):
    """Базовый абстрактный класс для проектов и пожертвований."""

    __abstract__ = True

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            '0 <= invested_amount AND invested_amount <= full_amount',
            name='check_invested_amount_not_negative'
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
        if self.full_amount == self.invested_amount:
            self.fully_invested = True
            self.close_date = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        """Отладочный метод."""
        base_repr = super().__repr__()
        additional_fields = (
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}'
            f'create_date={self.create_date}, '
            f'close_date={self.close_date}'
        )
        return base_repr.replace(')>', f', {additional_fields})>')
