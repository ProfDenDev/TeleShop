# run_olx_import.py
# ver 1.0
# created: 2026-06-16 01:20 UTC+3
# ver 2.0
# created: 2026-06-16 02:00 UTC+3

import asyncio

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

from app.services.product_service import (
    ProductService,
)

from app.services.product_price_service import (
    ProductPriceService,
)

from app.services.product_photo_service import (
    ProductPhotoService,
)

from app.services.sku_service import (
    SkuService,
)

from app.imports.services.olx_json_import_service import (
    OlxJsonImportService,
)


async def main():

    async with SessionLocal() as session:

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

        product_photo_service = (
            ProductPhotoService(
                product_photo_repository
            )
        )

        sku_service = (
            SkuService(
                product_repository
            )
        )

        olx_import_service = (
            OlxJsonImportService(
                product_service=product_service,
                product_price_service=product_price_service,
                product_photo_service=product_photo_service,
                sku_service=sku_service,
            )
        )

        result = await (
            olx_import_service
            .import_json(
                "storage/imports/products_detailed_260615-1702.json"
            )
        )

        print()
        print("=" * 50)
        print("IMPORT RESULT")
        print("=" * 50)
        print(result)
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(
        main()
    )


# import asyncio
#
# from app.database.session import (
#     SessionLocal,
# )
#
# from app.database.repositories.product_repository import (
#     ProductRepository,
# )
#
# from app.database.repositories.product_price_repository import (
#     ProductPriceRepository,
# )
#
# from app.database.repositories.product_photo_repository import (
#     ProductPhotoRepository,
# )
#
# from app.services.product_service import (
#     ProductService,
# )
#
# from app.services.product_price_service import (
#     ProductPriceService,
# )
#
# from app.services.product_photo_service import (
#     ProductPhotoService,
# )
#
# from app.services.sku_service import (
#     SkuService,
# )
#
# from app.imports.services.olx_json_import_service import (
#     OlxJsonImportService,
# )
#
#
# async def main():
#
#     async with SessionLocal() as session:
#
#         product_repository = (
#             ProductRepository(session)
#         )
#
#         price_repository = (
#             ProductPriceRepository(session)
#         )
#
#         photo_repository = (
#             ProductPhotoRepository(session)
#         )
#
#         product_service = (
#             ProductService(
#                 product_repository
#             )
#         )
#
#         product_price_service = (
#             ProductPriceService(
#                 price_repository
#             )
#         )
#
#         product_photo_service = (
#             ProductPhotoService(
#                 photo_repository
#             )
#         )
#
#         sku_service = (
#             SkuService(
#                 product_repository
#             )
#         )
#
#         import_service = (
#             OlxJsonImportService(
#                 product_service=product_service,
#                 product_price_service=product_price_service,
#                 product_photo_service=product_photo_service,
#                 sku_service=sku_service,
#             )
#         )
#
#         result = await (
#             import_service.import_json(
#                 "storage/imports/products_detailed_260615-1654.json"
#             )
#         )
#
#         print()
#         print("=" * 50)
#         print("IMPORT RESULT")
#         print("=" * 50)
#         print(result)
#         print("=" * 50)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
