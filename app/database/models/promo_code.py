from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PromoCode(Base):
    """
    Денежные значения хранятся в копейках.

    Для PERCENT:
        discount_value = 10

    Для FIXED:
        discount_value = 10000 (100 грн)
    """

    __tablename__ = "promo_codes"

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    name: Mapped[str] = mapped_column(String(255))

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    discount_type: Mapped[str] = mapped_column(
        String(20)
    )

    discount_value: Mapped[int] = mapped_column(
        Integer
    )

    minimum_order_amount: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    max_uses: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    used_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    max_uses_per_user: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    start_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    end_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )
