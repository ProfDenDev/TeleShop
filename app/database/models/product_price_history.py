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


class ProductPriceHistory(Base):
    """
    История изменения цены товара.

    Все цены хранятся в копейках.
    """

    __tablename__ = "product_price_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    old_price_from: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    old_price_to: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    new_price_from: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    new_price_to: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    old_currency: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    new_currency: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    old_price_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    new_price_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    changed_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )
