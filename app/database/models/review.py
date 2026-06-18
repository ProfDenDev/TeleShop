from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    String,
    Boolean,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Review(Base):
    """
    Отзывы о товаре.

    Отзыв может оставить только покупатель.
    """

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    # Оценка от 1 до 5
    rating: Mapped[int] = mapped_column(
        Integer
    )

    # Текст отзыва
    text: Mapped[str | None] = mapped_column(
        String(3000),
        nullable=True
    )

    # Одобрен администратором
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "user_id",
            name="uq_review_product_user"
        ),
    )


