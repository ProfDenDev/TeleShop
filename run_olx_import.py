# run_olx_import.py
# ver 3.0 created: 2026-06-16 01:20 UTC+3
# ver 3.0 updated: 2026-06-18 23:15 UTC+3
#
# Импорт товаров OLX.
#
# Выполняет:
# - создание товаров
# - создание цен
# - загрузку фото в Telegram
# - получение telegram_file_id
# - получение telegram_media_group_id
# - создание ProductPhoto

import asyncio

from aiogram import Bot

from app.config import (
    BOT_TOKEN,
)

from app.database.session import (
    SessionLocal,
)

from app.database.repositories.product_repository import (
    ProductRepository,
)

from app.database.repositories.product_price_repository import (
    ProductPriceRepository,
)

from app.database.repositories.product_photo_repository import (
    ProductPhotoRepository,
)

from app.database.repositories.brand_repository import (
    BrandRepository,
)

from app.database.repositories.category_repository import (
    CategoryRepository,
)

from app.imports.services.brand_import_service import (
    BrandImportService,
)

from app.imports.services.category_import_service import (
    CategoryImportService,
)

from app.imports.services.olx_json_import_service import (
    OlxJsonImportService,
)

from app.services.product_service import (
    ProductService,
)

from app.services.product_price_service import (
    ProductPriceService,
)

from app.services.sku_service import (
    SkuService,
)

from app.services.telegram_album_service import (
    TelegramAlbumService,
)


async def main():

    async with SessionLocal() as session:

        # =====================================
        # Repositories
        # =====================================

        product_repository = (
            ProductRepository(
                session
            )
        )

        product_price_repository = (
            ProductPriceRepository(
                session
            )
        )

        product_photo_repository = (
            ProductPhotoRepository(
                session
            )
        )

        brand_repository = (
            BrandRepository(
                session
            )
        )

        category_repository = (
            CategoryRepository(
                session
            )
        )

        # =====================================
        # Import services
        # =====================================

        brand_service = (
            BrandImportService(
                brand_repository
            )
        )

        category_service = (
            CategoryImportService(
                category_repository
            )
        )

        # =====================================
        # Main services
        # =====================================

        product_service = (
            ProductService(
                product_repository,
                brand_service,
                category_service,
            )
        )

        product_price_service = (
            ProductPriceService(
                product_price_repository
            )
        )

        sku_service = (
            SkuService(
                product_repository
            )
        )

        # =====================================
        # Telegram
        # =====================================

        bot = Bot(
            token=BOT_TOKEN
        )

        telegram_album_service = (
            TelegramAlbumService(
                bot=bot
            )
        )

        # =====================================
        # Import service
        # =====================================

        olx_import_service = (
            OlxJsonImportService(
                product_service=product_service,

                product_price_service=(
                    product_price_service
                ),

                product_photo_repository=(
                    product_photo_repository
                ),

                telegram_album_service=(
                    telegram_album_service
                ),

                sku_service=sku_service,
            )
        )

        result = await (
            olx_import_service
            .import_json(
                "storage/imports/products_detailed_260615-1721.json"
            )
        )

        print()
        print("=" * 50)
        print("IMPORT RESULT")
        print("=" * 50)
        print(result)
        print("=" * 50)

        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(
        main()
    )
