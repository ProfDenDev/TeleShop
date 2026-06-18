from sqlalchemy import select

from app.database.models.cart_item import CartItem

from app.database.repositories.base_repository import BaseRepository


class CartRepository(BaseRepository):
    """
    Репозиторий корзины.
    """

    model = CartItem

    async def get_user_cart(
        self,
        user_id: int
    ):
        """
        Получить корзину пользователя.
        """

        stmt = select(CartItem).where(
            CartItem.user_id == user_id
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_cart_item(
        self,
        user_id: int,
        product_id: int
    ):
        """
        Получить товар из корзины.
        """

        stmt = select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def remove_item(
        self,
        user_id: int,
        product_id: int
    ):
        """
        Удалить товар из корзины.
        """

        item = await self.get_cart_item(
            user_id,
            product_id
        )

        if not item:
            return

        await self.session.delete(item)

        await self.session.commit()

    async def clear_cart(
        self,
        user_id: int
    ):
        """
        Полностью очистить корзину.
        """

        items = await self.get_user_cart(
            user_id
        )

        for item in items:
            await self.session.delete(item)

        await self.session.commit()

    async def add_to_cart(
        self,
        user_id: int,
        product_id: int,
        quantity: int = 1
    ):
        """
        Добавить товар в корзину.

        Если товар уже есть —
        увеличиваем количество.
        """

        item = await self.get_cart_item(
            user_id=user_id,
            product_id=product_id
        )

        if item:

            item.quantity += quantity

            await self.session.commit()

            await self.session.refresh(item)

            return item

        item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )

        self.session.add(item)

        await self.session.commit()

        await self.session.refresh(item)

        return item
    async def update_quantity(
        self,
        user_id: int,
        product_id: int,
        quantity: int
    ):
        """
        Изменить количество товара.

        Если quantity <= 0,
        товар удаляется из корзины.
        """

        item = await self.get_cart_item(
            user_id=user_id,
            product_id=product_id
        )

        if not item:
            return None

        if quantity <= 0:

            await self.session.delete(item)

            await self.session.commit()

            return None

        item.quantity = quantity

        await self.session.commit()

        await self.session.refresh(item)

        return item