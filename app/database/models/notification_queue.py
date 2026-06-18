from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    ForeignKey,
    DateTime,
    String,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class NotificationQueue(Base):
    """
    Очередь уведомлений.

    Используется чтобы не отправлять сообщения ночью.

    Разрешённое окно:
    09:00 - 20:00
    """

    __tablename__ = "notification_queue"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    # PRICE_DROP
    # SIMILAR
    # ORDER_STATUS_CHANGED
    notification_type: Mapped[str] = mapped_column(
        String(50)
    )

    # Данные уведомления в JSON
    payload_json: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )

    # Когда можно отправить
    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    # Когда реально отправлено
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


