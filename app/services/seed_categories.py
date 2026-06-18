# app/services/seed_categories.py

"""
Первичное заполнение таблицы categories.

Назначение:
    Создать стартовый набор категорий TELESHOP
    при первом запуске проекта.

Важно:
    - Выполняется только если таблица categories пустая.
    - Повторный запуск безопасен.
    - Не изменяет существующие категории.
    - Использует данные из:
        default_categories.py
        default_subcategories.py

Используется:
    При первоначальной инициализации БД.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.category import Category

from app.constants.default_categories import DEFAULT_CATEGORIES
from app.constants.default_subcategories import DEFAULT_SUBCATEGORIES


async def seed_categories(session: AsyncSession) -> None:
    """
    Создать стартовые категории.

    Аргументы:
        session:
            Активная SQLAlchemy AsyncSession.

    Логика:
        1. Проверяем есть ли хотя бы одна категория.
        2. Если есть — выходим.
        3. Создаем корневые категории.
        4. Создаем подкатегории.
        5. Выполняем commit.
    """

    # Проверяем наличие категорий в базе.
    result = await session.execute(
        select(Category.id).limit(1)
    )

    existing_category = result.scalar_one_or_none()

    # Если категории уже существуют —
    # повторное заполнение не требуется.
    if existing_category:
        return

    # Хранилище созданных корневых категорий.
    #
    # Ключ:
    #     slug категории
    #
    # Значение:
    #     объект Category
    #
    # Нужно для быстрого поиска родителя
    # при создании подкатегорий.
    parent_categories: dict[str, Category] = {}

    # Создание корневых категорий.
    for item in DEFAULT_CATEGORIES:

        category = Category(
            parent_id=None,

            name_ru=item["name_ru"],
            name_uk=item["name_uk"],
            name_en=None,

            slug=item["slug"],

            seo_title=None,
            seo_description=None,

            sort_order=item["sort_order"],

            is_service=item["is_service"],
            show_in_main_menu=True,
        )

        session.add(category)

        parent_categories[item["slug"]] = category

    # Получаем ID созданных категорий
    # до выполнения commit.
    await session.flush()

    # Создание подкатегорий.
    for parent_slug, children in DEFAULT_SUBCATEGORIES.items():

        parent = parent_categories.get(parent_slug)

        # Если родитель не найден —
        # пропускаем группу.
        if not parent:
            continue

        sort_order = 100

        for child in children:

            category = Category(
                parent_id=parent.id,

                name_ru=child["name_ru"],
                name_uk=child["name_uk"],
                name_en=None,

                slug=child["slug"],

                seo_title=None,
                seo_description=None,

                sort_order=sort_order,

                is_service=parent.is_service,
                show_in_main_menu=False,
            )

            session.add(category)

            sort_order += 100

    await session.commit()