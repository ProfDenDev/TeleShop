from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class OrderNote(Base):
    """
    История заказа.

    Используется для хранения:

    - комментариев
    - серийных номеров
    - гарантийных пломб
    - ТТН
    - сервисных заметок
    """

    __tablename__ = "order_notes"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # Заказ
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    # Кто создал запись
    created_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    # Тип записи
    #
    # COMMENT
    # SERIAL_NUMBER
    # WARRANTY_SEAL
    # TRACKING_NUMBER
    # PAYMENT_NOTE
    # SERVICE_NOTE
    note_type: Mapped[str] = mapped_column(
        String(50)
    )

    # Текст записи
    note_text: Mapped[str] = mapped_column(
        String(4000)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )

