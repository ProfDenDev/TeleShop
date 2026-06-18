# app/imports/services/olx_json_import_service.py
# ver 1.0 created: 2026-06-16 00:05 UTC+3
# ver 1.1 created: 2026-06-16 00:05 UTC+3
# updated: 2026-06-16 00:30 UTC+3

import json
from pathlib import Path

from app.constants.price_types import (
    FIXED,
)

from app.constants.currencies import (
    UAH,
)

from app.imports.dto.product_import_dto import (
    ProductImportDTO,
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


class OlxJsonImportService:
    """
    Импорт товаров из OLX JSON.
    """

    def __init__(
        self,
        product_service: ProductService,
        product_price_service: ProductPriceService,
        product_photo_service: ProductPhotoService,
        sku_service: SkuService,
    ):
        self.product_service = (
            product_service
        )

        self.product_price_service = (
            product_price_service
        )

        self.product_photo_service = (
            product_photo_service
        )

        self.sku_service = (
            sku_service
        )

    async def import_json(
        self,
        json_path: str,
    ) -> dict:
        """
        Импортировать JSON файл.
        """

        result = {
            "created": 0,
            "errors": 0,
        }

        path = Path(
            json_path
        )

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            products = json.load(
                file
            )

        # =====================================
        # Получаем стартовый SKU один раз
        # =====================================

        first_sku = await (
            self.sku_service
            .generate_next_sku()
        )

        start_number = int(
            first_sku[2:]
        )

        for index, item in enumerate(
            products
        ):

            try:

                sku = (
                    f"DA{start_number + index:04d}"
                )

                title = (
                    item.get(
                        "title",
                        "",
                    )
                    .strip()
                )

                full_description = (
                    item.get(
                        "description",
                        "",
                    )
                    .strip()
                )

                short_description = (
                    full_description[:200]
                )

                category_slug = (
                    self._get_category_slug(
                        item
                    )
                )

                dto = ProductImportDTO(
                    sku=sku,

                    title=title,

                    short_description=(
                        short_description
                    ),

                    full_description=(
                        full_description
                    ),

                    category_slug=(
                        category_slug
                    ),

                    quantity=1,
                )

                product = await (
                    self.product_service
                    .create_product(
                        dto
                    )
                )

                price = int(
                    float(
                        item.get(
                            "price",
                            0,
                        )
                    )
                    * 100
                )

                await (
                    self.product_price_service
                    .create_or_update_price(
                        product_id=(
                            product.id
                        ),

                        price_type=FIXED,

                        currency=UAH,

                        price_from_value=(
                            price
                        ),

                        price_to_value=None,
                    )
                )

                images = item.get(
                    "images",
                    [],
                )

                if images:

                    photo_string = (
                        "|".join(
                            images
                        )
                    )

                    await (
                        self.product_photo_service
                        .replace_photos(
                            product_id=(
                                product.id
                            ),

                            photo_files=(
                                photo_string
                            ),
                        )
                    )

                result[
                    "created"
                ] += 1

            except Exception as e:

                print(
                    f"OLX import error: {e}"
                )

                result[
                    "errors"
                ] += 1

        return result

    def _get_category_slug(
        self,
        item: dict,
    ) -> str:
        """
        Преобразование OLX категорий
        в категории TELESHOP.
        """

        categories = item.get(
            "categories",
            [],
        )

        names = [
            c.get(
                "name_uk",
                "",
            )
            for c in categories
        ]

        if (
            "Інструменти"
            in names
        ):
            return "tools"

        if (
            "Комп'ютери та комплектуючі"
            in names
        ):
            return "computers"

        if (
            "Телефони та аксесуари"
            in names
        ):
            return "phones"

        if (
            "Антикваріат / колекції"
            in names
        ):
            return "collectibles"

        if (
            "Хобі, відпочинок і спорт"
            in names
        ):
            return "hobby"

        if (
            "Дім і сад"
            in names
        ):
            return "home-garden"

        if (
            "Електроніка"
            in names
        ):
            return "electronics"

        return "other"



# # Назначение:
# # Импорт товаров из JSON,
# # полученного от OLX scraper.
# #
# # Поддерживает:
# #
# # - создание Product
# # - создание ProductPrice
# # - создание ProductPhoto
# # - автоматическую генерацию SKU
# #
# # Формат:
# #
# # products_detailed_xxxxx.json
# # images_detailed_xxxxx/
# #
# # Все цены:
# #
# # FIXED
# # UAH
# # в копейках
# #
# # Фото:
# #
# # сохраняются как ProductPhoto
# # telegram_file_id = NULL
# #
# # далее загружаются через
# # PhotoFolderImportService
#
# import json
# from pathlib import Path
#
# from app.constants.price_types import (
#     FIXED,
# )
#
# from app.constants.currencies import (
#     UAH,
# )
#
# from app.imports.dto.product_import_dto import (
#     ProductImportDTO,
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
#
# class OlxJsonImportService:
#     """
#     Импорт товаров из OLX JSON.
#     """
#
#     def __init__(
#         self,
#         product_service: ProductService,
#         product_price_service: ProductPriceService,
#         product_photo_service: ProductPhotoService,
#         sku_service: SkuService,
#     ):
#         self.product_service = (
#             product_service
#         )
#
#         self.product_price_service = (
#             product_price_service
#         )
#
#         self.product_photo_service = (
#             product_photo_service
#         )
#
#         self.sku_service = (
#             sku_service
#         )
#
#     async def import_json(
#         self,
#         json_path: str,
#     ) -> dict:
#         """
#         Импортировать JSON файл.
#         """
#
#         result = {
#             "created": 0,
#             "updated": 0,
#             "errors": 0,
#         }
#
#         path = Path(
#             json_path
#         )
#
#         with open(
#             path,
#             "r",
#             encoding="utf-8",
#         ) as file:
#
#             products = json.load(
#                 file
#             )
#
#         for item in products:
#
#             try:
#
#                 # =====================
#                 # SKU
#                 # =====================
#
#                 sku = await (
#                     self.sku_service
#                     .generate_next_sku()
#                 )
#
#                 # =====================
#                 # TITLE
#                 # =====================
#
#                 title = (
#                     item.get(
#                         "title",
#                         "",
#                     )
#                     .strip()
#                 )
#
#                 # =====================
#                 # DESCRIPTION
#                 # =====================
#
#                 full_description = (
#                     item.get(
#                         "description",
#                         "",
#                     )
#                     .strip()
#                 )
#
#                 short_description = (
#                     full_description[:200]
#                 )
#
#                 # =====================
#                 # CATEGORY
#                 # =====================
#
#                 category_slug = (
#                     self._get_category_slug(
#                         item
#                     )
#                 )
#
#                 # =====================
#                 # DTO
#                 # =====================
#
#                 dto = (
#                     ProductImportDTO(
#                         sku=sku,
#
#                         title=title,
#
#                         short_description=(
#                             short_description
#                         ),
#
#                         full_description=(
#                             full_description
#                         ),
#
#                         category_slug=(
#                             category_slug
#                         ),
#
#                         quantity=1,
#
#                         photo_files=(
#                             item.get(
#                                 "images",
#                                 [],
#                             )
#                         ),
#                     )
#                 )
#
#                 # =====================
#                 # PRODUCT
#                 # =====================
#
#                 product = await (
#                     self.product_service
#                     .create_product(
#                         dto
#                     )
#                 )
#
#                 # =====================
#                 # PRICE
#                 # =====================
#
#                 price = int(
#                     float(
#                         item.get(
#                             "price",
#                             0,
#                         )
#                     )
#                     * 100
#                 )
#
#                 await (
#                     self.product_price_service
#                     .create_or_update_price(
#                         product_id=(
#                             product.id
#                         ),
#
#                         price_type=FIXED,
#
#                         currency=UAH,
#
#                         price_from_value=(
#                             price
#                         ),
#
#                         price_to_value=(
#                             None
#                         ),
#                     )
#                 )
#
#                 # =====================
#                 # PHOTO
#                 # =====================
#
#                 images = item.get(
#                     "images",
#                     [],
#                 )
#
#                 if images:
#
#                     await (
#                         self.product_photo_service
#                         .replace_photos(
#                             product_id=(
#                                 product.id
#                             ),
#
#                             photo_files=(
#                                 images
#                             ),
#                         )
#                     )
#
#                 result[
#                     "created"
#                 ] += 1
#
#             except Exception as e:
#
#                 print(
#                     f"OLX import error: {e}"
#                 )
#
#                 result[
#                     "errors"
#                 ] += 1
#
#         return result
#
#     def _get_category_slug(
#         self,
#         item: dict,
#     ) -> str:
#         """
#         Преобразование OLX категорий
#         в категории TELESHOP.
#         """
#
#         categories = (
#             item.get(
#                 "categories",
#                 [],
#             )
#         )
#
#         names = [
#             c.get(
#                 "name_uk",
#                 "",
#             )
#             for c in categories
#         ]
#
#         if (
#             "Інструменти"
#             in names
#         ):
#             return (
#                 "tools"
#             )
#
#         if (
#             "Комп'ютери та комплектуючі"
#             in names
#         ):
#             return (
#                 "computers"
#             )
#
#         if (
#             "Телефони та аксесуари"
#             in names
#         ):
#             return (
#                 "phones"
#             )
#
#         if (
#             "Книги / журнали"
#             in names
#         ):
#             return (
#                 "books"
#             )
#
#         if (
#             "Антикваріат / колекції"
#             in names
#         ):
#             return (
#                 "collectibles"
#             )
#
#         if (
#             "Мода і стиль"
#             in names
#         ):
#             return (
#                 "fashion"
#             )
#
#         if (
#             "Хобі, відпочинок і спорт"
#             in names
#         ):
#             return (
#                 "hobby"
#             )
#
#         if (
#             "Дім і сад"
#             in names
#         ):
#             return (
#                 "home-garden"
#             )
#
#         if (
#             "Електроніка"
#             in names
#         ):
#             return (
#                 "electronics"
#             )
#
#         return (
#             "other"
#         )