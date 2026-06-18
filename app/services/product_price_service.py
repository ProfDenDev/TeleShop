# app/services/product_price_service.py
# ver 3.0
from app.database.models.product_price import (
    ProductPrice,
)

from app.database.repositories.product_price_repository import (
    ProductPriceRepository,
)


class ProductPriceService:
    """
    Сервис работы с ценами товаров.

    Все цены в БД хранятся
    в минимальных единицах валюты:

        UAH -> копейки
        USD -> центы
        EUR -> евроценты
    """

    def __init__(
        self,
        price_repository: ProductPriceRepository,
    ):
        self.price_repository = (
            price_repository
        )

    async def get_by_product_id(
        self,
        product_id: int,
    ) -> ProductPrice | None:

        return await (
            self.price_repository
            .get_by_product_id(
                product_id
            )
        )

    async def create_price(
        self,
        product_id: int,
        price_type: str,
        currency: str,
        price_from_value: int | None,
        price_to_value: int | None,
    ) -> ProductPrice:

        return await (
            self.price_repository
            .create(
                product_id=product_id,

                price_type=price_type,

                currency=currency,

                price_from_value=(
                    price_from_value
                ),

                price_to_value=(
                    price_to_value
                ),
            )
        )

    async def update_price(
        self,
        price: ProductPrice,
        price_type: str,
        currency: str,
        price_from_value: int | None,
        price_to_value: int | None,
    ) -> ProductPrice:

        price.price_type = (
            price_type
        )

        price.currency = (
            currency
        )

        price.price_from_value = (
            price_from_value
        )

        price.price_to_value = (
            price_to_value
        )

        return await (
            self.price_repository
            .update(price)
        )

    async def create_or_update_price(
        self,
        product_id: int,
        price_type: str,
        currency: str,
        price_from_value: int | None,
        price_to_value: int | None,
    ) -> ProductPrice:

        existing_price = await (
            self.price_repository
            .get_by_product_id(
                product_id
            )
        )

        if not existing_price:

            return await (
                self.create_price(
                    product_id=product_id,

                    price_type=price_type,

                    currency=currency,

                    price_from_value=(
                        price_from_value
                    ),

                    price_to_value=(
                        price_to_value
                    ),
                )
            )

        return await (
            self.update_price(
                price=existing_price,

                price_type=price_type,

                currency=currency,

                price_from_value=(
                    price_from_value
                ),

                price_to_value=(
                    price_to_value
                ),
            )
        )