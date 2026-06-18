# app/imports/services/olx_json_import_service.py
# ver 1.0 created: 2026-06-16 00:05 UTC+3
# ver 1.1 created: 2026-06-16 00:05 UTC+3
# updated: 2026-06-16 00:30 UTC+3
# ver 2.0 created: 2026-06-16 00:05 UTC+3
# ver 2.0 updated: 2026-06-18 22:45 UTC+3
#
# Назначение:
# Импорт товаров из OLX JSON.
#
# Возможности:
# - создание Product
# - создание ProductPrice
# - загрузка фото в Telegram
# - получение telegram_file_id
# - получение telegram_media_group_id
# - создание ProductPhoto
#
# Формат:
# products_detailed_xxxxx.json
# images_detailed_xxxxx/

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

from app.services.telegram_album_service import (
    TelegramAlbumService,
)

from app.database.repositories.product_photo_repository import (
    ProductPhotoRepository,
)

from app.services.product_price_service import (
    ProductPriceService,
)

from app.services.sku_service import (
    SkuService,
)


class OlxJsonImportService:
    """
    Импорт товаров из OLX JSON.
    """

    # ==========================================
    # Constructor
    # ==========================================

    def __init__(
            self,
            product_service: ProductService,
            product_price_service: ProductPriceService,
            product_photo_repository: ProductPhotoRepository,
            telegram_album_service: TelegramAlbumService,
            sku_service: SkuService,
    ):
        self.product_service = (
            product_service
        )

        self.product_price_service = (
            product_price_service
        )

        self.product_photo_repository = (
            product_photo_repository
        )

        self.telegram_album_service = (
            telegram_album_service
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

                # =====================================
                # Фото товара
                #
                # Загружаются сразу в Telegram.
                # Получаем:
                #
                # - telegram_file_id
                # - telegram_media_group_id
                # =====================================

                images = item.get(
                    "images",
                    [],
                )

                if images:

                    json_file_name = (
                        path.stem
                    )

                    images_folder = (
                        json_file_name
                        .replace(
                            "products",
                            "images",
                        )
                    )

                    image_paths = []

                    for image_name in images:
                        # =====================================
                        # Проверка существования файла
                        # =====================================

                        full_path = (
                                Path(
                                    "storage/imports"
                                )
                                / images_folder
                                / image_name
                        )

                        if not full_path.exists():
                            print(
                                f"PHOTO NOT FOUND: {full_path}"
                            )

                            continue

                        image_paths.append(
                            str(full_path)
                        )

                    if not image_paths:
                        continue

                    album = await (
                        self.telegram_album_service
                        .upload_photos(
                            image_paths
                        )
                    )

                    for position, photo in enumerate(
                            album["photos"]
                    ):
                        relative_path = (
                            str(
                                Path(
                                    images_folder
                                )
                                / Path(
                                    photo["path"]
                                ).name
                            )
                        )

                        await (
                            self.product_photo_repository
                            .create(
                                product_id=(
                                    product.id
                                ),

                                telegram_file_id=(
                                    photo["file_id"]
                                ),

                                telegram_media_group_id=(
                                    album.get("media_group_id")
                                ),

                                original_filename=(
                                    relative_path
                                ),

                                position=position,
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
