# run_seed_categories.py
# ver 1.0
# created: 2026-06-16 02:00 UTC+3

import asyncio

from app.database.session import (
    SessionLocal,
)

from app.database.repositories.category_repository import (
    CategoryRepository,
)

from app.seeds.default_categories_seed import (
    DefaultCategoriesSeed,
)


async def main():

    async with SessionLocal() as session:

        category_repository = (
            CategoryRepository(
                session
            )
        )

        seed = (
            DefaultCategoriesSeed(
                category_repository
            )
        )

        await seed.run()

        print()
        print("=" * 50)
        print("CATEGORIES SEEDED")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(
        main()
    )
