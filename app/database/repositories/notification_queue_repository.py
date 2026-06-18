from datetime import datetime

from sqlalchemy import (
    select,
    delete
)

from app.database.models.notification_queue import (
    NotificationQueue
)

from app.database.repositories.base_repository import (
    BaseRepository
)

from app.constants.notification_types import (
    NotificationType
)

from app.utils.datetime_utils import (
    utc_now
)


class NotificationQueueRepository(
    BaseRepository
):
    """
    Репозиторий очереди уведомлений.
    """

    model = NotificationQueue

    async def add_notification(
        self,
        user_id: int,
        notification_type: NotificationType,
        payload_json: str | None = None,
        scheduled_at: datetime | None = None
    ):
        """
        Добавить уведомление в очередь.
        """

        notification = (
            NotificationQueue(
                user_id=user_id,
                notification_type=notification_type,
                payload_json=payload_json,
                scheduled_at=scheduled_at
            )
        )

        self.session.add(
            notification
        )

        await self.session.flush()

        return notification

    async def get_pending_notifications(
        self,
        limit: int = 100
    ):
        """
        Получить уведомления ожидающие отправки.
        """

        stmt = (
            select(NotificationQueue)
            .where(
                NotificationQueue.sent_at.is_(None)
            )
            .limit(limit)
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalars().all()

    async def get_ready_notifications(
        self,
        limit: int = 100
    ):
        """
        Получить уведомления готовые к отправке.
        """

        now = utc_now()

        stmt = (
            select(NotificationQueue)
            .where(
                NotificationQueue.sent_at.is_(None),
                NotificationQueue.scheduled_at.is_not(None),
                NotificationQueue.scheduled_at <= now
            )
            .limit(limit)
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalars().all()

    async def mark_sent(
        self,
        notification_id: int
    ) -> bool:
        """
        Пометить уведомление отправленным.
        """

        notification = await self.get_by_id(
            notification_id
        )

        if not notification:
            return False

        notification.sent_at = (
            utc_now()
        )

        await self.session.flush()

        return True

    async def delete_sent_notifications(
        self
    ) -> int:
        """
        Очистить отправленные уведомления.
        """

        stmt = delete(
            NotificationQueue
        ).where(
            NotificationQueue.sent_at.is_not(None)
        )

        result = await self.session.execute(
            stmt
        )

        return result.rowcount

    async def get_user_notifications(
        self,
        user_id: int
    ):
        """
        Уведомления пользователя.
        """

        stmt = select(
            NotificationQueue
        ).where(
            NotificationQueue.user_id
            == user_id
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalars().all()