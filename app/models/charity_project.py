from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base as ProjectDonationBase
from app.constants import MAXIMUM_SYMBOL_NAME_LIMIT


class CharityProject(ProjectDonationBase):
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

    def __repr__(self) -> str:
        """Отладочный метод с опорой на базовый класс."""
        return f'Project name="{self.name}"'
