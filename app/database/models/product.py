from datetime import datetime
from app.utils.datetime_utils import utc_now
from uuid import uuid4

from app.constants.db_lengths import (
    CATEGORY_NAME_MAX_LENGTH,
    CATEGORY_SLUG_MAX_LENGTH,
    SEO_TITLE_MAX_LENGTH,
    SEO_DESCRIPTION_MAX_LENGTH,
)

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    uuid: Mapped[str] = mapped_column(
        String(36),
        default=lambda: str(uuid4()),
        unique=True,
        index=True
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    brand_id: Mapped[int | None] = mapped_column(
        ForeignKey("brands.id"),
        nullable=True
    )

    created_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    updated_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    manufacturer_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    manufacturer_sku: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    barcode: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    serial_number: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    title: Mapped[str] = mapped_column(
        String(500)
    )

    slug: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        index=True
    )

    short_description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    full_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    content_language: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    attributes_json: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    search_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    search_text_normalized: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    condition: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE"
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    warranty_days: Mapped[int | None] = mapped_column(
        nullable=True
    )

    weight_g: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    dimensions: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    location_area: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    video_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    sort_priority: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    photo_status: Mapped[str] = mapped_column(
        String(50),
        default="NO_PHOTO"
    )

    discount_excluded: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    featured_until: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    hidden_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    seo_title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    seo_description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
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

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

