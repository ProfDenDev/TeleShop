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


class Order(Base):
    """
    Все денежные значения хранятся в копейках.

    19999 = 199.99 грн
    """

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING"
    )

    customer_name: Mapped[str] = mapped_column(String(255))
    customer_phone: Mapped[str] = mapped_column(String(50))

    customer_comment: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )

    admin_comment: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )

    delivery_method: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    delivery_details: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    promo_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    discount_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    discount_value: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    discount_amount: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    total_before_discount: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    total_after_discount: Mapped[int] = mapped_column(
        Integer,
        default=0
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

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
