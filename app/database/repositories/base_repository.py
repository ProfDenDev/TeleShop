# app/database/repositories/base_repository.py
# ver 1.1
#
# Назначение:
# Базовый репозиторий проекта.
#
# Отвечает за:
# - получение записи по ID;
# - создание записи;
# - обновление записи;
# - удаление записи;
# - сохранение изменений.
#
# Все остальные репозитории наследуются
# от данного класса.

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """
    Базовый репозиторий.

    Все остальные репозитории наследуются от него.
    """

    model = None

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_by_id(
        self,
        item_id: int,
    ):
        """
        Получить запись по ID.
        """

        stmt = select(self.model).where(
            self.model.id == item_id
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        **kwargs,
    ):
        """
        Создать запись.
        """

        obj = self.model(
            **kwargs
        )

        self.session.add(obj)

        await self.session.commit()

        await self.session.refresh(obj)

        return obj

    async def update(
        self,
        obj,
    ):
        """
        Сохранить изменённый объект.

        Используется после изменения полей
        существующей записи.
        """

        await self.session.commit()

        await self.session.refresh(obj)

        return obj

    async def save(
        self,
    ):
        """
        Просто сохранить изменения.
        """

        await self.session.commit()

    async def delete(
        self,
        obj,
    ):
        """
        Удалить запись.
        """

        await self.session.delete(obj)

        await self.session.commit()
