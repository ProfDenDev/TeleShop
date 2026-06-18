from datetime import datetime
from app.utils.datetime_utils import utc_now

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CartItem(Base):
    """
    Корзина пользователя.

    Сейчас количество товара обычно = 1,
    но поле quantity оставляем на будущее.

    Один товар может присутствовать в корзине
    пользователя только один раз.
    """

    __tablename__ = "cart_items"

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

    # Количество товара
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    # Когда товар добавили в корзину
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now
    )

    # Когда последний раз меняли количество
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        onupdate=utc_now
    )

    __table_args__ = (
        # Один товар может быть в корзине
        # пользователя только один раз
        UniqueConstraint(
            "user_id",
            "product_id",
            name="uq_cart_user_product"
        ),
    )