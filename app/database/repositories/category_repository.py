from sqlalchemy import select

from collections import defaultdict
from sqlalchemy import select

from app.database.models.category import Category
from app.database.repositories.base_repository import BaseRepository

class CategoryRepository(BaseRepository):
    """
    Репозиторий категорий.

    Работа с деревом категорий.
    """

    model = Category

    async def get_root_categories(self):
        """
        Получить категории верхнего уровня.
        """

        stmt = (
            select(Category)
            .where(Category.parent_id.is_(None))
            .order_by(Category.sort_order)
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_children(self, parent_id: int):
        """
        Получить подкатегории категории.
        """

        stmt = (
            select(Category)
            .where(Category.parent_id == parent_id)
            .order_by(Category.sort_order)
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_by_slug(self, slug: str):
        """
        Получить категорию по slug.
        """

        stmt = select(Category).where(
            Category.slug == slug
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_services_category(self):
        """
        Получить категорию услуг.
        """

        stmt = select(Category).where(
            Category.is_service.is_(True)
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_category_tree(self):
        """
        Получить всё дерево категорий одним запросом.

        Возвращает:

        [
            {
                "category": root_category,
                "children": [...]
            }
        ]
        """

        stmt = (
            select(Category)
            .order_by(
                Category.sort_order,
                Category.name_ru
            )
        )

        result = await self.session.execute(stmt)

        categories = result.scalars().all()

        root_categories = []
        children_map = defaultdict(list)

        for category in categories:

            if category.parent_id is None:
                root_categories.append(category)
            else:
                children_map[
                    category.parent_id
                ].append(category)

        tree = []

        for root in root_categories:

            tree.append(
                {
                    "category": root,
                    "children": children_map.get(
                        root.id,
                        []
                    )
                }
            )

        return tree


