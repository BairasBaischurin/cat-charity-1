from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, ConfigDict, Field,
    PositiveInt, field_serializer
)


class DonationCreate(BaseModel):
    """Схема для пожертвований."""

    model_config = ConfigDict(
        extra='forbid',
    )
    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')
    comment: Optional[str] = Field(None, title='Комментарий')


class DonationDB(DonationCreate):
    """Ответ пользователю после пожертвования."""

    model_config = ConfigDict(
        extra='forbid',
        from_attributes=True
    )
    id: int = Field(..., title='Первичный ключ')
    create_date: datetime = Field(..., title='Дата создания')
    close_date: Optional[datetime] = Field(None, title='Дата закрытия')

    @field_serializer('create_date', 'close_date', check_fields=False)
    def serialize_dt(self, dt: datetime, _info):
        if dt is None:
            return None
        return dt.isoformat().replace('+00:00', '').replace('Z', '')


class DonationFullInfoDB(DonationDB):
    """Ответ администратору после пожертвовния."""

    invested_amount: int = Field(..., title='Собранная сумма')
    fully_invested: bool = Field(..., title='Проект полностью инвестирован')
    close_date: Optional[datetime] = Field(title='Дата закрытия')
