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
        comment_preview = f'"{self.comment[:15]}"' if self.comment else 'None'
        return (
            f'Donation comment={comment_preview} | Data: {super().__repr__()}'
        )
