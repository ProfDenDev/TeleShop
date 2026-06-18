from sqlalchemy import select, or_

from app.constants.shop_constants import (
SEARCH_RESULTS_LIMIT
)

from app.database.models.product import Product
from app.database.repositories.base_repository import (BaseRepository)

class ProductRepository(BaseRepository):
    """    Репозиторий товаров.
    Здесь находится вся работа с таблицей products.
    """

    model = Product
    """
    Репозиторий товаров.
    Вся работа с каталогом товаров:
    - поиск
    - получение карточки
    - выборки по категориям
    - выборки по брендам
    """

    async def get_by_id(self, product_id: int):
        """       Получить товар по ID. """
        stmt = select(Product).where(
            Product.id == product_id
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_sku(self, sku: str):
        """Поиск товара по внутреннему артикулу.
        Пример:   DA-1234
        """
        stmt = select(Product).where(
            Product.sku == sku
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_slug(self, slug: str):
        """  Поиск товара по SEO ссылке.
        """

        stmt = select(Product).where(
            Product.slug == slug
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_uuid(self, uuid: str):
        """ Поиск товара по UUID.
        """

        stmt = select(Product).where(
            Product.uuid == uuid)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_featured(self):
        """        Получить рекомендуемые товары.        """
        stmt = select(Product).where(
            Product.is_featured.is_(True)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def get_by_category(self, category_id: int):
        """        Получить товары категории."""

        stmt = select(Product).where(
            Product.category_id == category_id
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def get_by_brand(self, brand_id: int):
        """        Получить товары бренда."""

        stmt = select(Product).where(
            Product.brand_id == brand_id
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def search(self, query: str, limit: int = SEARCH_RESULTS_LIMIT):
        """        Поиск товаров.
        Поиск выполняется по:
        - названию
        - SKU
        """

        stmt = (select(Product)
            .where(
                or_(Product.title.ilike(f"%{query}%"),
                    Product.sku.ilike(f"%{query}%")
                )
            )
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def get_active(self):
        """
        Активные товары каталога.
        """

        stmt = select(Product).where(
            Product.status == "ACTIVE",
            Product.is_hidden.is_(False),
            Product.deleted_at.is_(None)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def get_hidden(self):
        """
        Скрытые товары.
        """

        stmt = select(Product).where(
            Product.is_hidden.is_(True)
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()


    async def get_deleted(self):
        """
        Удалённые товары.
        """

        stmt = select(Product).where(
            Product.deleted_at.is_not(None)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def can_be_added_to_cart(self, product_id: int) -> bool:
        """
        Можно ли добавить товар в корзину.
        """

        product = await self.get_by_id(product_id)

        if not product: return False
        if product.deleted_at:return False
        if product.is_hidden: return False
        if product.status != "ACTIVE": return False
        return True


    async def get_related_products(self, product_id: int, limit: int = 10):
        """
        Похожие товары из той же категории.
        """

        product = await self.get_by_id(product_id)

        if not product: return []

        stmt = (select(Product)
            .where(Product.category_id
                == product.category_id,
                Product.id != product.id)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_last_sku_by_prefix(
        self,
        prefix: str,
    ) -> str | None:
        """
        Получить последний SKU по префиксу.

        Примеры:

            DA0001
            DA0002
            DA0105

        Вернёт:

            DA0105
        """

        stmt = (
            select(Product)
            .where(
                Product.sku.like(
                    f"{prefix}%"
                )
            )
            .order_by(
                Product.sku.desc()
            )
            .limit(1)
        )

        result = await self.session.execute(
            stmt
        )

        product = (
            result.scalar_one_or_none()
        )

        if not product:
            return None

        return product.sku









