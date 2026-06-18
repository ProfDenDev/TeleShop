
from app.utils.datetime_utils import utc_now
from app.constants.shop_constants import (
    MIN_ORDER_AMOUNT
)

from sqlalchemy import select
# from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.order import Order
from app.database.repositories.base_repository import BaseRepository

from app.constants.order_constants import (
    ORDER_PREFIX,
    FIRST_ORDER_NUMBER,
    ORDER_NUMBER_PADDING
)


from app.database.models.cart_item import CartItem
from app.database.models.product_price import ProductPrice

from app.database.models.promo_code import PromoCode



class OrderRepository(BaseRepository):
    """
    Репозиторий заказов.
    """

    model = Order

    def __init__(
                self,
                session: AsyncSession
        ):
            super().__init__(session)

    async def generate_order_number(self) -> str:
        """
        Генерация номера заказа.

        Пример:

        ORD-26-001001
        ORD-26-001002
        """

        year_short = utc_now().strftime("%y")

        prefix = (
            f"{ORDER_PREFIX}-"
            f"{year_short}-"
        )

        stmt = (
            select(Order)
            .where(
                Order.order_number.like(
                    f"{prefix}%"
                )
            )
            .order_by(
                Order.order_number.desc()
            )
        )

        result = await self.session.execute(
            stmt
        )

        last_order = (
            result.scalar_one_or_none()
        )

        if not last_order:

            next_number = (
                FIRST_ORDER_NUMBER
            )

        else:

            try:

                next_number = (
                        int(
                            last_order.order_number
                            .split("-")[-1]
                        )
                        + 1
                )

            except (
                    ValueError,
                    IndexError
            ):

                next_number = (
                    FIRST_ORDER_NUMBER
                )

        return (
            f"{ORDER_PREFIX}-"
            f"{year_short}-"
            f"{next_number:0{ORDER_NUMBER_PADDING}d}"
        )
    async def calculate_order_total(
        self,
        user_id: int
    ) -> int:
        """
        Рассчитать сумму заказа.

        Берутся только товары:

        quantity > 0

        В будущем:
        is_selected = True
        """

        stmt = (
            select(CartItem)
            .where(
                CartItem.user_id == user_id
            )
            .where(
                CartItem.quantity > 0
            )
        )

        result = await self.session.execute(
            stmt
        )

        cart_items = result.scalars().all()

        total = 0

        for item in cart_items:

            price_stmt = (select(
                ProductPrice).where
                (
                ProductPrice.product_id
                == item.product_id
            ))

            price_result = (
                await self.session.execute(
                    price_stmt
                )
            )

            price = (
                price_result.scalar_one_or_none()
            )

            if not price:
                continue

            if not price.price_uah_cached:
                continue

            total += (
                    price.price_uah_cached
                    * item.quantity
            )

        if total < MIN_ORDER_AMOUNT:
            raise ValueError(
                "MIN_ORDER_AMOUNT"
            )

        return total


    async def apply_promo_code(
        self,
        total: int,
        promo_code: str | None
    ):
        """
        Применение промокода.

        Возвращает:

        success
        total
        error
        """

        if not promo_code:

            return {
                "success": True,
                "total": total,
                "promo_code": None
            }

        stmt = select(PromoCode).where(
            PromoCode.code == promo_code
        )

        result = await self.session.execute(
            stmt
        )

        promo = result.scalar_one_or_none()

        if not promo:

            return {
                "success": False,
                "total": total,
                "error": "PROMO_NOT_FOUND"
            }

        if (
                promo.minimum_order_amount
                and total
                < promo.minimum_order_amount
        ):
            return {
                "success": False,
                "total": total,
                "error": "PROMO_MIN_ORDER"
            }

        if not promo.is_active:

            return {
                "success": False,
                "total": total,
                "error": "PROMO_DISABLED"
            }

        if (promo.start_at
                and promo.start_at > utc_now()
        ):
            return {
                "success": False,
                "total": total,
                "error": "PROMO_NOT_STARTED"
            }


        if (promo.end_at
            and promo.end_at < utc_now()
        ):
            return {
                "success": False,
                "total": total,
                "error": "PROMO_EXPIRED"
            }

        if (
            promo.max_uses
            and promo.used_count >= promo.max_uses
        ):
            return {
                "success": False,
                "total": total,
                "error": "PROMO_LIMIT_REACHED"
            }

        final_total = total

        if promo.discount_type == "PERCENT":
            final_total = (
                total *
                (100 - promo.discount_value)
            ) // 100


        elif promo.discount_type == "FIXED":

            final_total = (
                    total
                    - promo.discount_value
            )

        final_total = max(
            final_total,
            1
        )

        return {
            "success": True,
            "total": final_total,
            "promo_code": promo.code
        }

