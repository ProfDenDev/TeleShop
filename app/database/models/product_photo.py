# app/database/models/product_photo.py

from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    Integer,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base

from app.utils.datetime_utils import utc_now

from app.constants.db_lengths import (
    PHOTO_TELEGRAM_FILE_ID_MAX_LENGTH,
    PHOTO_FILENAME_MAX_LENGTH,
    PHOTO_RELATIVE_PATH_MAX_LENGTH,
)


class ProductPhoto(Base):
    __tablename__ = "product_photos"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    telegram_file_id: Mapped[str | None] = mapped_column(
        String(PHOTO_TELEGRAM_FILE_ID_MAX_LENGTH),
        nullable=True,
    )

    original_filename: Mapped[str | None] = mapped_column(
        String(PHOTO_FILENAME_MAX_LENGTH),
        nullable=True,
    )

    telegram_media_group_id: Mapped[str | None] = mapped_column(
        String(PHOTO_RELATIVE_PATH_MAX_LENGTH),
        nullable=True,
    )

    # Главное фото товара имеет position = 0.
    # Далее:
    # 1, 2, 3, 4 ...
    position: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    )
