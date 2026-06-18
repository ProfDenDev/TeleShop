from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    ForeignKey,
    DateTime,
    String,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class NotifySubscription(Base):
    """
    Подписки пользователя на уведомления.
    """

    __tablename__ = "notify_subscriptions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    # PRICE_DROP
    # SIMILAR
    # BACK_IN_STOCK
    subscription_type: Mapped[str] = mapped_column(
        String(50)
    )

    last_notified_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "product_id",
            "subscription_type",
            name="uq_notify_subscription"
        ),
    )


