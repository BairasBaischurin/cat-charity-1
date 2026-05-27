from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestmentModel
from app.constants import MAXIMUM_SYMBOL_NAME_LIMIT


class CharityProject(InvestmentModel):
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
<<<<<<< HEAD
        return (
            f'CharityProject('
            f'id={self.id}, '
            f'name="{self.name}", '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date}, '
            f'close_date={self.close_date})'
        )
=======
        return f'Project name="{self.name}"'
>>>>>>> c5ba1e07413c7d51442824b51dabc5f158de6a40
