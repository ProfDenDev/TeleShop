from sqlalchemy import (
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ProductTag(Base):
    """
    Связь товара и тега.

    Один товар может иметь много тегов.
    Один тег может использоваться у многих товаров.
    """

    __tablename__ = "product_tags"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id")
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "tag_id",
            name="uq_product_tag"
        ),
    )

