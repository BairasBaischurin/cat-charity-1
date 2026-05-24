from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.base import BaseMixin
from app.constants import MAXIMUM_SYMBOL_NAME_LIMIT


class CharityProject(BaseMixin, Base):
    """Модель «Проект»."""

    name: Mapped[str] = mapped_column(
        String(MAXIMUM_SYMBOL_NAME_LIMIT),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
