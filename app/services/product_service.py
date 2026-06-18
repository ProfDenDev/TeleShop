# app/services/product_service.py
# ver 2.0
# ver 4.0

from slugify import slugify

from app.database.models.product import Product

from app.database.repositories.product_repository import (
    ProductRepository,
)

from app.imports.dto.product_import_dto import (
    ProductImportDTO,
)

from app.imports.services.brand_import_service import (
    BrandImportService,
)

from app.imports.services.category_import_service import (
    CategoryImportService,
)


DEFAULT_CATEGORY_SLUG = "other"


class ProductService:
    """
    Основной сервис работы с товарами.

    Используется:

        XLSX импорт
        ZIP фото импорт
        Telegram Bot
        Mini App
    """

    def __init__(
        self,
        product_repository: ProductRepository,
        brand_service: BrandImportService,
        category_service: CategoryImportService,
    ):
        self.product_repository = (
            product_repository
        )

        self.brand_service = (
            brand_service
        )

        self.category_service = (
            category_service
        )

    async def get_by_sku(
        self,
        sku: str,
    ) -> Product | None:

        return await (
            self.product_repository
            .get_by_sku(sku)
        )

    async def create_product(
        self,
        dto: ProductImportDTO,
    ) -> Product:

        # ==========================
        # Категория
        # ==========================

        category = None

        if dto.category_slug:

            category = await (
                self.category_service
                .get_by_slug(
                    dto.category_slug
                )
            )

        if not category:

            category = await (
                self.category_service
                .get_by_slug(
                    DEFAULT_CATEGORY_SLUG
                )
            )

        # ==========================
        # Бренд
        # ==========================

        brand = None

        if dto.brand_name:

            brand = await (
                self.brand_service
                .get_or_create_brand(
                    dto.brand_name
                )
            )

        # ==========================
        # Slug
        # ==========================

        slug = self._generate_slug(
            dto.title,
            dto.sku,
        )

        # ==========================
        # Создание товара
        # ==========================

        return await (
            self.product_repository
            .create(
                category_id=category.id,

                brand_id=(
                    brand.id
                    if brand
                    else None
                ),

                sku=dto.sku,

                title=dto.title,

                slug=slug,

                short_description=(
                    dto.short_description
                ),

                full_description=(
                    dto.full_description
                ),

                content_language=(
                    dto.content_language
                ),

                manufacturer_name=(
                    dto.manufacturer_name
                ),

                manufacturer_sku=(
                    dto.manufacturer_sku
                ),

                barcode=(
                    dto.barcode
                ),

                serial_number=(
                    dto.serial_number
                ),

                condition=(
                    dto.condition
                ),

                quantity=(
                    dto.quantity
                ),

                weight_g=(
                    dto.weight_g
                    or 0
                ),

                dimensions=(
                    dto.dimensions
                ),

                location_area=(
                    dto.location_area
                ),

                video_url=(
                    dto.video_url
                ),

                attributes_json=(
                    dto.attributes_json
                ),
            )
        )

    async def update_product(
        self,
        product: Product,
        dto: ProductImportDTO,
    ) -> Product:

        # ==========================
        # Категория
        # ==========================

        if dto.category_slug:

            category = await (
                self.category_service
                .get_by_slug(
                    dto.category_slug
                )
            )

            if category:

                product.category_id = (
                    category.id
                )

        # ==========================
        # Бренд
        # ==========================

        if dto.brand_name:

            brand = await (
                self.brand_service
                .get_or_create_brand(
                    dto.brand_name
                )
            )

            if brand:

                product.brand_id = (
                    brand.id
                )

        # ==========================
        # Основные поля
        # ==========================

        product.title = dto.title

        product.slug = (
            self._generate_slug(
                dto.title,
                dto.sku,
            )
        )

        product.short_description = (
            dto.short_description
        )

        product.full_description = (
            dto.full_description
        )

        product.content_language = (
            dto.content_language
        )

        product.manufacturer_name = (
            dto.manufacturer_name
        )

        product.manufacturer_sku = (
            dto.manufacturer_sku
        )

        product.barcode = (
            dto.barcode
        )

        product.serial_number = (
            dto.serial_number
        )

        product.condition = (
            dto.condition
        )

        product.quantity = (
            dto.quantity
        )

        product.weight_g = (
            dto.weight_g
            or 0
        )

        product.dimensions = (
            dto.dimensions
        )

        product.location_area = (
            dto.location_area
        )

        product.video_url = (
            dto.video_url
        )

        product.attributes_json = (
            dto.attributes_json
        )

        return await (
            self.product_repository
            .update(product)
        )

    @staticmethod
    def _generate_slug(
        title: str,
        sku: str,
    ) -> str:
        """
        Формат:

            leica-m500-da0001

            anycubic-mono-4-ultra-db0002
        """

        return (
            f"{slugify(title)}-"
            f"{sku.lower()}"
        )


# Назначение:
# Центральный сервис работы с товарами TELESHOP.
#
# Используется:
# - XLSX импорт
# - ZIP фото импорт
# - Telegram Bot
# - Mini App
#
# Важно:
# - SKU обязателен
# - Title обязателен
# - Категория может отсутствовать
# - Бренд может отсутствовать
# - Slug формируется:
#       title + sku
# - Если категория не указана:
#       используется "other"

# from slugify import slugify
#
# from app.database.models.product import Product
#
# from app.database.repositories.product_repository import (
#     ProductRepository,
# )
#
# from app.imports.dto.product_import_dto import (
#     ProductImportDTO,
# )
#
# from app.imports.services.brand_import_service import (
#     BrandImportService,
# )
#
# from app.imports.services.category_import_service import (
#     CategoryImportService,
# )
#
#
# DEFAULT_CATEGORY_SLUG = "other"
#
#
# class ProductService:
#
#     def __init__(
#         self,
#         product_repository: ProductRepository,
#         brand_service: BrandImportService,
#         category_service: CategoryImportService,
#     ):
#         self.product_repository = (
#             product_repository
#         )
#
#         self.brand_service = (
#             brand_service
#         )
#
#         self.category_service = (
#             category_service
#         )
#
#     async def get_by_sku(
#         self,
#         sku: str,
#     ) -> Product | None:
#
#         return await (
#             self.product_repository
#             .get_by_sku(sku)
#         )
#
#     async def create_product(
#         self,
#         dto: ProductImportDTO,
#     ) -> Product:
#
#         # ==========================
#         # Категория
#         # ==========================
#
#         category = None
#
#         if dto.category_slug:
#
#             category = await (
#                 self.category_service
#                 .get_by_slug(
#                     dto.category_slug
#                 )
#             )
#
#         if not category:
#
#             category = await (
#                 self.category_service
#                 .get_by_slug(
#                     DEFAULT_CATEGORY_SLUG
#                 )
#             )
#
#         # ==========================
#         # Бренд
#         # ==========================
#
#         brand = None
#
#         if dto.brand_name:
#
#             brand = await (
#                 self.brand_service
#                 .get_or_create_brand(
#                     dto.brand_name
#                 )
#             )
#
#         # ==========================
#         # Slug
#         # ==========================
#
#         slug = await (
#             self._generate_slug(
#                 dto.title,
#                 dto.sku,
#             )
#         )
#
#         # ==========================
#         # Создание товара
#         # ==========================
#
#         return await (
#             self.product_repository
#             .create(
#                 category_id=category.id,
#
#                 brand_id=(
#                     brand.id
#                     if brand
#                     else None
#                 ),
#
#                 sku=dto.sku,
#
#                 title=dto.title,
#
#                 slug=slug,
#
#                 short_description=(
#                     dto.short_description
#                 ),
#
#                 full_description=(
#                     dto.full_description
#                 ),
#
#                 quantity=(
#                     dto.quantity
#                     or 1
#                 ),
#
#                 weight_g=(
#                     dto.weight_g
#                     or 0
#                 ),
#
#                 dimensions=(
#                     dto.dimensions
#                 ),
#             )
#         )
#
#     async def update_product(
#         self,
#         product: Product,
#         dto: ProductImportDTO,
#     ) -> Product:
#
#         # ==========================
#         # Категория
#         # ==========================
#
#         if dto.category_slug:
#
#             category = await (
#                 self.category_service
#                 .get_by_slug(
#                     dto.category_slug
#                 )
#             )
#
#             if category:
#
#                 product.category_id = (
#                     category.id
#                 )
#
#         # ==========================
#         # Бренд
#         # ==========================
#
#         if dto.brand_name:
#
#             brand = await (
#                 self.brand_service
#                 .get_or_create_brand(
#                     dto.brand_name
#                 )
#             )
#
#             product.brand_id = (
#                 brand.id
#                 if brand
#                 else None
#             )
#
#         # ==========================
#         # Основные поля
#         # ==========================
#
#         product.title = dto.title
#
#         product.slug = await (
#             self._generate_slug(
#                 dto.title,
#                 dto.sku,
#             )
#         )
#
#         product.short_description = (
#             dto.short_description
#         )
#
#         product.full_description = (
#             dto.full_description
#         )
#
#         product.quantity = (
#             dto.quantity
#             or 1
#         )
#
#         product.weight_g = (
#             dto.weight_g
#             or 0
#         )
#
#         product.dimensions = (
#             dto.dimensions
#         )
#
#         return await (
#             self.product_repository
#             .update(product)
#         )
#
#     async def set_status(
#         self,
#         product: Product,
#         status: str,
#     ) -> Product:
#
#         product.status = status
#
#         return await (
#             self.product_repository
#             .update(product)
#         )
#
#     async def _generate_slug(
#         self,
#         title: str,
#         sku: str,
#     ) -> str:
#         """
#         Формат:
#
#         leica-m500-da0001
#         anycubic-mono-4-ultra-db0002
#         """
#
#         return (
#             f"{slugify(title)}-"
#             f"{sku.lower()}"
#         )