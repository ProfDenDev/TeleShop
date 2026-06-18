from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class OrderItem(Base):
    """
    Все денежные значения хранятся в копейках.

    19999 = 199.99 грн
    """

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id"),
        nullable=True
    )

    sku: Mapped[str] = mapped_column(String(50))

    product_title: Mapped[str] = mapped_column(
        String(500)
    )

    quantity: Mapped[int] = mapped_column(
        Integer
    )

    # Цена за единицу в копейках
    price_value: Mapped[int] = mapped_column(
        Integer
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="UAH"
    )

    # Цена в гривне (копейки)
    price_uah_cached: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # quantity * price_value
    subtotal: Mapped[int] = mapped_column(
        Integer
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )
