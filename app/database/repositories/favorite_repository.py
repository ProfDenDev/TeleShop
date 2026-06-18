from sqlalchemy import select, func


from app.database.repositories.base_repository import BaseRepository

from app.database.models.favorite import Favorite
from app.database.models.product import Product
from app.database.models.category import Category


class FavoriteRepository(BaseRepository):
    """
    Репозиторий избранного.
    """

    model = Favorite

    async def is_favorite(
        self,
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Проверить находится ли товар в избранном.
        """

        stmt = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.product_id == product_id
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none() is not None

    async def get_user_favorites(
        self,
        user_id: int
    ):
        """
        Получить список избранного пользователя.
        """

        stmt = select(Favorite).where(
            Favorite.user_id == user_id
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def remove_favorite(
        self,
        user_id: int,
        product_id: int
    ):
        """
        Удалить товар из избранного.
        """

        stmt = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.product_id == product_id
        )

        result = await self.session.execute(stmt)

        favorite = result.scalar_one_or_none()

        if favorite:

            await self.session.delete(
                favorite
            )

            await self.session.commit()

    async def get_favorites_count(
        self,
        user_id: int
    ) -> int:
        """
        Посчитать количество товаров
        (услуги не считаются).
        """

        stmt = (
            select(
                func.count(Favorite.id)
            )
            .join(
                Product,
                Favorite.product_id == Product.id
            )
            .join(
                Category,
                Product.category_id == Category.id
            )
            .where(
                Favorite.user_id == user_id,
                Category.is_service.is_(False)
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar() or 0

    async def add_favorite(
        self,
        user_id: int,
        product_id: int
    ):
        """
        Добавить товар в избранное.

        Ограничения:

        - один товар нельзя добавить дважды
        - максимум 30 товаров
        - услуги не учитываются в лимите
        """

        # Проверяем есть ли уже товар
        if await self.is_favorite(
            user_id=user_id,
            product_id=product_id
        ):
            return None

        # Получаем товар
        stmt = (
            select(Product)
            .where(Product.id == product_id)
        )

        result = await self.session.execute(stmt)

        product = result.scalar_one_or_none()

        if not product:
            return None

        # Проверяем категорию
        stmt = (
            select(Category)
            .where(
                Category.id == product.category_id
            )
        )

        result = await self.session.execute(stmt)

        category = result.scalar_one_or_none()

        # Если это не услуга —
        # проверяем лимит 30 товаров
        if (
            category
            and not category.is_service
        ):

            favorites_count = (
                await self.get_favorites_count(
                    user_id
                )
            )

            if favorites_count >= 30:
                raise ValueError(
                    "Favorite limit exceeded"
                )

        favorite = Favorite(
            user_id=user_id,
            product_id=product_id
        )

        self.session.add(favorite)

        await self.session.commit()

        await self.session.refresh(
            favorite
        )

        return favorite


