# app/imports/services/category_import_service.py
# ver 2.0
# updated: 2026-06-15 19:15 UTC+3

from app.database.repositories.category_repository import (
    CategoryRepository,
)


DEFAULT_CATEGORY_SLUG = "other"


class CategoryImportService:
    """
    Сервис категорий для импорта.

    Новая версия работает через slug.

    Примеры:

        medicine

        microscopes

        electronics
    """

    def __init__(
        self,
        category_repository: CategoryRepository,
    ):
        self.category_repository = (
            category_repository
        )

    async def get_by_slug(
        self,
        slug: str,
    ):
        """
        Получить категорию по slug.
        """

        return await (
            self.category_repository
            .get_by_slug(slug)
        )

    async def category_exists(
        self,
        slug: str | None,
    ) -> bool:

        if not slug:
            return False

        category = await (
            self.category_repository
            .get_by_slug(slug)
        )

        return category is not None

    async def get_default_category(
        self,
    ):
        """
        Категория по умолчанию.

        other
        """

        return await (
            self.category_repository
            .get_by_slug(
                DEFAULT_CATEGORY_SLUG
            )
        )
# from app.database.repositories.category_repository import (
#     CategoryRepository,
# )
#
#
# class CategoryImportService:
#     """
#     Сервис работы с категориями во время импорта.
#
#     Основная задача:
#     найти category_id по category_path.
#
#     Пример:
#
#     Медицина/Микроскопы
#         ↓
#     25
#
#     Телефоны/Смартфоны
#         ↓
#     41
#     """
#
#     def __init__(
#         self,
#         category_repository: CategoryRepository,
#     ):
#         self.category_repository = (
#             category_repository
#         )
#
#     async def get_category_map(
#         self,
#     ) -> dict[str, int]:
#         """
#         Возвращает словарь:
#
#         {
#             "Медицина": 1,
#             "Медицина/Микроскопы": 2,
#             "Телефоны": 10,
#             "Телефоны/Смартфоны": 11,
#         }
#         """
#
#         categories = (
#             await self.category_repository.get_all()
#         )
#
#         category_map: dict[str, int] = {}
#
#         category_by_id = {
#             category.id: category
#             for category in categories
#         }
#
#         for category in categories:
#
#             path_parts = [
#                 category.name_ru
#             ]
#
#             parent_id = category.parent_id
#
#             while parent_id:
#
#                 parent = category_by_id.get(
#                     parent_id
#                 )
#
#                 if not parent:
#                     break
#
#                 path_parts.insert(
#                     0,
#                     parent.name_ru,
#                 )
#
#                 parent_id = parent.parent_id
#
#             category_path = "/".join(
#                 path_parts
#             )
#
#             category_map[
#                 category_path
#             ] = category.id
#
#         return category_map
#
#     async def get_category_id(
#         self,
#         category_path: str,
#     ) -> int | None:
#         """
#         Возвращает id категории по пути.
#
#         Пример:
#
#         Медицина/Микроскопы
#             ↓
#         25
#
#         Если категория не найдена:
#
#             ↓
#         None
#         """
#
#         category_map = (
#             await self.get_category_map()
#         )
#
#         return category_map.get(
#             category_path.strip()
#         )
#
#     async def category_exists(
#         self,
#         category_path: str,
#     ) -> bool:
#         """
#         Проверка существования категории.
#         """
#
#         category_id = (
#             await self.get_category_id(
#                 category_path
#             )
#         )
#
#         return category_id is not None