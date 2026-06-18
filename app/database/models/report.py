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


class Report(Base):
    """
    Жалобы пользователей.

    Жалобу может оставить только покупатель.
    """

    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    # Причина жалобы
    reason: Mapped[str] = mapped_column(
        String(2000)
    )

    # PENDING
    # APPROVED
    # REJECTED
    status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "user_id",
            name="uq_report_product_user"
        ),
    )


