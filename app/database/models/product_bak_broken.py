from datetime import datetime

from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base

from app.constants.db_lengths import (
    CATEGORY_NAME_MAX_LENGTH,
    CATEGORY_SLUG_MAX_LENGTH,
    SEO_TITLE_MAX_LENGTH,
    SEO_DESCRIPTION_MAX_LENGTH,
)


class Category(Base):
    __tablename__ = "categories"

    # Внутренний идентификатор
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # Родительская категория
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
        index=True,
    )

    # Название категории (русский)
    name_ru: Mapped[str] = mapped_column(
        String(CATEGORY_NAME_MAX_LENGTH),
        nullable=False,
    )

    # Название категории (украинский)
    name_uk: Mapped[str] = mapped_column(
        String(CATEGORY_NAME_MAX_LENGTH),
        nullable=False,
    )

    # Название категории (английский)
    name_en: Mapped[str | None] = mapped_column(
        String(CATEGORY_NAME_MAX_LENGTH),
        nullable=True,
    )

    # SEO URL
    slug: Mapped[str] = mapped_column(
        String(CATEGORY_SLUG_MAX_LENGTH),
        unique=True,
        index=True,
        nullable=False,
    )

    # SEO заголовок
    seo_title: Mapped[str | None] = mapped_column(
        String(SEO_TITLE_MAX_LENGTH),
        nullable=True,
    )

    # SEO описание
    seo_description: Mapped[str | None] = mapped_column(
        String(SEO_DESCRIPTION_MAX_LENGTH),
        nullable=True,
    )

    # Порядок сортировки
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # Категория услуг
    is_service: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Показывать в главном меню
    show_in_main_menu: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Активна ли категория
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
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