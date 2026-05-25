from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base as ProjectDonationBase


class Donation(ProjectDonationBase):
    """Модель «Пожертвование»."""

    comment: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    def __repr__(self) -> str:
        """Отладочный метод с опорой на базовый класс."""
        base_repr = super().__repr__()

        short_comment = (
            f'"{self.comment[:15]}..."'
            if self.comment and len(self.comment) > 15
            else f'"{self.comment}"'
        )

        return base_repr.replace(
            f'<{self.__class__.__name__}(',
            f'<{self.__class__.__name__}(comment={short_comment}, '
        )
