from sqlalchemy import select

from app.database.models.product_price import ProductPrice
from app.database.repositories.base_repository import (
    BaseRepository
)


class ProductPriceRepository(BaseRepository):
    """
    Репозиторий цен товаров.
    """

    model = ProductPrice

    async def get_by_product_id(self, product_id: int):
        """
        Получить цену товара.
        """

        stmt = select(ProductPrice).where(
            ProductPrice.product_id == product_id
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_price_uah(
            self,
            product_id: int
    ) -> int | None:
        """
        Получить цену товара в копейках.
        """

        price = await self.get_by_product_id(
            product_id
        )

        if not price:
            return None

        return price.price_uah_cached

    async def has_price(
            self,
            product_id: int
    ) -> bool:
        """
        Проверить наличие цены.
        """

        price = await self.get_by_product_id(product_id)

        if not price: return False
        return (price.price_uah_cached
                is not None)

    async def update_cached_price(self, product_id: int, price_uah: int):
        """
        Обновить цену в гривне.
        """

        price = await self.get_by_product_id(product_id)

        if not price:return None

        price.price_uah_cached = (price_uah)

        await self.session.flush()

        return price

    async def update_cached_price(self, product_id: int, price_uah: int):
        """
        Обновить цену в гривне.
        """

        price = await self.get_by_product_id(product_id)
        if not price: return None

        price.price_uah_cached = (price_uah)

        await self.session.flush()
        return price

    async def get_products_without_price(self):
        """
        Найти товары без цены.
        """
        stmt = (select(ProductPrice)
                .where(ProductPrice.price_uah_cached.is_(None)))

        result = await self.session.execute(stmt)
        return result.scalars().all()



