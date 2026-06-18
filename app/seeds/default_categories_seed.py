# app/seeds/default_categories_seed.py
# ver 1.0
# created: 2026-06-16 01:45 UTC+3
#
# Назначение:
# Первичное заполнение категорий и подкатегорий.
#
# Источники:
# - default_categories.py
# - default_subcategories.py

from app.constants.default_categories import (
    DEFAULT_CATEGORIES,
)

from app.constants.default_subcategories import (
    DEFAULT_SUBCATEGORIES,
)

from app.database.repositories.category_repository import (
    CategoryRepository,
)


class DefaultCategoriesSeed:

    def __init__(
        self,
        category_repository: CategoryRepository,
    ):
        self.category_repository = (
            category_repository
        )

    async def run(self):
        """
        Заполнить категории.
        """

        # =====================
        # ROOT CATEGORIES
        # =====================

        category_map = {}

        for item in DEFAULT_CATEGORIES:

            existing = await (
                self.category_repository
                .get_by_slug(
                    item["slug"]
                )
            )

            if existing:

                category_map[
                    item["slug"]
                ] = existing

                continue

            category = await (
                self.category_repository
                .create(
                    parent_id=None,

                    name_ru=item[
                        "name_ru"
                    ],

                    name_uk=item[
                        "name_uk"
                    ],

                    name_en=item[
                        "name_ru"
                    ],

                    slug=item[
                        "slug"
                    ],

                    sort_order=item[
                        "sort_order"
                    ],

                    is_service=item[
                        "is_service"
                    ],
                )
            )

            category_map[
                item["slug"]
            ] = category

        # =====================
        # SUBCATEGORIES
        # =====================

        for (
            parent_slug,
            subcategories
        ) in (
            DEFAULT_SUBCATEGORIES
            .items()
        ):

            parent = (
                category_map.get(
                    parent_slug
                )
            )

            if not parent:
                continue

            for sub in subcategories:

                existing = await (
                    self.category_repository
                    .get_by_slug(
                        sub["slug"]
                    )
                )

                if existing:
                    continue

                await (
                    self.category_repository
                    .create(
                        parent_id=parent.id,

                        name_ru=sub[
                            "name_ru"
                        ],

                        name_uk=sub[
                            "name_uk"
                        ],

                        name_en=sub[
                            "name_ru"
                        ],

                        slug=sub[
                            "slug"
                        ],

                        sort_order=0,

                        is_service=False,
                    )
                )
