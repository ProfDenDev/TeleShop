from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    String,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Tag(Base):
    """
    Справочник тегов.

    Примеры:

    leica
    microscope
    dental
    camera
    resin
    anycubic

    Теги используются для:
    - поиска
    - рекомендаций
    - похожих товаров
    - SEO
    """

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # Название тега
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
    )

    # Когда создан тег
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )

