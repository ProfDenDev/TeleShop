from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    ForeignKey,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Favorite(Base):
    """
    Избранное пользователя.

    Один пользователь может добавить товар в избранное
    только один раз.

    Ограничение в 30 товаров будет проверяться
    на уровне бизнес-логики, а не БД.
    """

    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # Пользователь
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    # Товар
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    # Когда добавили в избранное
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )

    __table_args__ = (
        # Запрещаем добавить один и тот же товар дважды
        UniqueConstraint(
            "user_id",
            "product_id",
            name="uq_favorites_user_product"
        ),
    )


