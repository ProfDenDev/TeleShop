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


class CurrencyRate(Base):
    """
    Курс хранится в тысячных долях гривны.

    Примеры:

    41523 = 41.523 грн
    47210 = 47.210 грн
    """

    __tablename__ = "currency_rates"

    id: Mapped[int] = mapped_column(primary_key=True)

    currency: Mapped[str] = mapped_column(
        String(10),
        index=True
    )

    rate_to_uah: Mapped[int] = mapped_column(
        Integer
    )

    created_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )
