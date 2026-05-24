from datetime import datetime
from typing import Optional, Annotated

from pydantic import (
    BaseModel, ConfigDict, Field,
    PositiveInt, StringConstraints,
    field_serializer
)

from app.constants import (
    MINIMUM_SYMBOL_NAME_LIMIT,
    MAXIMUM_SYMBOL_NAME_LIMIT,
    MINIMUM_SYMBOL_DESCRIPTION_LIMIT
)

ProjectName = Annotated[
    str,
    StringConstraints(
        min_length=MINIMUM_SYMBOL_NAME_LIMIT,
        max_length=MAXIMUM_SYMBOL_NAME_LIMIT
    )
]
ProjectDescription = Annotated[
    str,
    StringConstraints(
        min_length=MINIMUM_SYMBOL_DESCRIPTION_LIMIT
    )
]


class CharityProjectCreate(BaseModel):
    """Схема для создания проекта."""

    model_config = ConfigDict(extra='forbid')
    name: ProjectName = Field(..., title='Имя проекта')
    description: ProjectDescription = Field(..., title='Описание')
    full_amount: PositiveInt = Field(..., title='Требуемая сумма')


class CharityProjectDB(CharityProjectCreate):
    """Схема для отображения проекта из базы данных."""

    model_config = ConfigDict(
        extra='forbid',
        from_attributes=True
    )

    id: int = Field(..., title='Первичный ключ')
    invested_amount: int = Field(..., title='Собранная сумма')
    fully_invested: bool = Field(..., title='Проект полностью инвестирован')
    create_date: datetime = Field(..., title='Дата создания проекта')
    close_date: Optional[datetime] = Field(title='Дата закрытия проекта')

    @field_serializer('create_date', 'close_date', check_fields=False)
    def serialize_dt(self, dt: datetime, _info):
        if dt is None:
            return None
        return dt.isoformat().replace('+00:00', '').replace('Z', '')


class CharityProjectUpdate(BaseModel):
    """Схема для обновдления проекта."""

    model_config = ConfigDict(
        extra='forbid',
    )
    name: Optional[ProjectName] = Field(None, title='Имя проекта')
    description: Optional[ProjectDescription] = Field(None, title='Описание')
    full_amount: Optional[PositiveInt] = Field(None, title='Требуемая сумма')
