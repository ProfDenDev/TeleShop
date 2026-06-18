from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    Integer
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ProductPrice(Base):
    """
    Все денежные значения хранятся в копейках.

    19999 = 199.99 грн
    """

    __tablename__ = "product_prices"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        unique=True
    )

    price_type: Mapped[str] = mapped_column(
        String(50)
    )

    price_from_value: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    price_to_value: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="UAH"
    )

    price_uah_cached: Mapped[int | None] = mapped_column(
        Integer,
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
