from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.base import BaseMixin


class Donation(BaseMixin, Base):
    """Модель «Пожертвование»."""

    comment: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
