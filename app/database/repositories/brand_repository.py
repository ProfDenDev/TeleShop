from sqlalchemy import select

from app.database.models.brand import Brand
from app.database.repositories.base_repository import BaseRepository


class BrandRepository(BaseRepository):
    """
    Репозиторий производителей.
    """

    model = Brand

    async def get_by_name(self, name: str):
        """
        Найти производителя по названию.
        """

        stmt = select(Brand).where(
            Brand.name == name
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str):
        """
        Найти производителя по slug.
        """

        stmt = select(Brand).where(
            Brand.slug == slug
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def list_all(self):
        """
        Получить список производителей.
        """

        stmt = select(Brand).order_by(
            Brand.name
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()

