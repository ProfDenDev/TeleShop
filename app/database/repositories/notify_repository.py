from sqlalchemy import (
    select, delete)

from app.database.models.notify_subscription import (
    NotifySubscription)

from app.database.repositories.base_repository import (
    BaseRepository)

from app.constants.notification_types import (
    NotificationType)

class NotifyRepository(BaseRepository):
    """
    Репозиторий подписок на уведомления.
    """

    model = NotifySubscription

    async def subscribe(self, user_id: int,
        product_id: int,
        subscription_type: NotificationType = (
            NotificationType.BACK_IN_STOCK
            )
    ):
        """
        Подписать пользователя.
        """

        existing = await (
            self.get_subscription(
                user_id=user_id,
                product_id=product_id,
                subscription_type=subscription_type
            )
        )

        if existing:
            return existing

        subscription = (
            NotifySubscription(
                user_id=user_id,
                product_id=product_id,
                subscription_type=(
                    subscription_type
                )
            )
        )

        self.session.add(
            subscription
        )

        await self.session.flush()

        return subscription

    async def unsubscribe(
        self,
        user_id: int,
        product_id: int,
        subscription_type: str = (
            "BACK_IN_STOCK"
        )
    ) -> bool:
        """
        Отписать пользователя.
        """

        stmt = delete(
            NotifySubscription
        ).where(
            NotifySubscription.user_id
            == user_id,
            NotifySubscription.product_id
            == product_id,
            NotifySubscription.subscription_type
            == subscription_type
        )

        result = await self.session.execute(
            stmt
        )

        return (
            result.rowcount > 0
        )

    async def get_subscription(
        self,
        user_id: int,
        product_id: int,
        subscription_type: str = (
            "BACK_IN_STOCK"
        )
    ):
        """
        Получить подписку.
        """

        stmt = select(
            NotifySubscription
        ).where(
            NotifySubscription.user_id
            == user_id,
            NotifySubscription.product_id
            == product_id,
            NotifySubscription.subscription_type
            == subscription_type
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def is_subscribed(
        self,
        user_id: int,
        product_id: int,
        subscription_type: str = (
            "BACK_IN_STOCK"
        )
    ) -> bool:
        """
        Проверить подписку.
        """

        subscription = (
            await self.get_subscription(
                user_id=user_id,
                product_id=product_id,
                subscription_type=subscription_type
            )
        )

        return (
            subscription is not None
        )

    async def get_product_subscribers(
        self,
        product_id: int,
        subscription_type: str = (
            "BACK_IN_STOCK"
        )
    ):
        """
        Подписчики товара.
        """

        stmt = select(
            NotifySubscription
        ).where(
            NotifySubscription.product_id
            == product_id,
            NotifySubscription.subscription_type
            == subscription_type
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalars().all()

    async def get_user_subscriptions(
        self,
        user_id: int
    ):
        """
        Подписки пользователя.
        """

        stmt = select(
            NotifySubscription
        ).where(
            NotifySubscription.user_id
            == user_id
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalars().all()

    async def delete_product_subscriptions(
        self,
        product_id: int
    ) -> int:
        """
        Удалить все подписки товара.
        """

        stmt = delete(
            NotifySubscription
        ).where(
            NotifySubscription.product_id
            == product_id
        )

        result = await self.session.execute(
            stmt
        )

        return result.rowcount