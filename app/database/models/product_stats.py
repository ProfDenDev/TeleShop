from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    Numeric
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ProductStats(Base):
    """
    Статистика товара.

    Отдельная таблица нужна для того, чтобы часто изменяемые данные
    (просмотры, рейтинг, избранное) не лежали в основной таблице Product.

    Это ускоряет работу каталога.
    """

    __tablename__ = "product_stats"

    # Один товар = одна запись статистики.
    # Поэтому product_id используется как PRIMARY KEY.
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        primary_key=True
    )

    # Все просмотры товара.
    # Учитываются абсолютно все открытия карточки.
    views_total: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # Уникальные просмотры.
    # Один пользователь считается один раз за сутки.
    views_unique: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # Сколько пользователей добавили товар в избранное.
    favorites_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # Сколько раз товар был заказан.
    orders_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # Средний рейтинг товара.
    # Например: 4.85
    rating_avg: Mapped[float] = mapped_column(
        Numeric(3, 2),
        default=0
    )

    # Количество оценок.
    rating_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # Последний просмотр карточки.
    last_view_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

