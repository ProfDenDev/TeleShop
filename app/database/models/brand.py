from datetime import datetime

from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    String,
    DateTime,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base

from app.constants.db_lengths import (
    BRAND_NAME_MAX_LENGTH,
    BRAND_SLUG_MAX_LENGTH,
    BRAND_WEBSITE_MAX_LENGTH,
    BRAND_DESCRIPTION_MAX_LENGTH,
)


class Brand(Base):
    __tablename__ = "brands"

    # Идентификатор бренда
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # Название бренда
    name: Mapped[str] = mapped_column(
        String(BRAND_NAME_MAX_LENGTH),
        unique=True,
        index=True,
        nullable=False,
    )

    # SEO URL бренда
    slug: Mapped[str] = mapped_column(
        String(BRAND_SLUG_MAX_LENGTH),
        unique=True,
        index=True,
        nullable=False,
    )

    # Сайт производителя
    website: Mapped[str | None] = mapped_column(
        String(BRAND_WEBSITE_MAX_LENGTH),
        nullable=True,
    )

    # Описание бренда
    description: Mapped[str | None] = mapped_column(
        String(BRAND_DESCRIPTION_MAX_LENGTH),
        nullable=True,
    )

    # Дата создания
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    # Дата обновления
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )