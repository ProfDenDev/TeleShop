from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    name_ru: Mapped[str] = mapped_column(
        String(255)
    )

    name_uk: Mapped[str] = mapped_column(
        String(255)
    )

    name_en: Mapped[str] = mapped_column(
        String(255)
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    seo_title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    seo_description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    is_service: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    show_in_main_menu: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        onupdate=utc_now
    )