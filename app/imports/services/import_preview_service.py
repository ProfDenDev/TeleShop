# app/imports/services/import_preview_service.py
# ver 2.0
# updated: 2026-06-15 19:20 UTC+3

from app.database.repositories.product_repository import (
    ProductRepository,
)

from app.imports.dto.product_import_dto import (
    ProductImportDTO,
)

from app.imports.models.import_preview_item import (
    ImportPreviewItem,
)

from app.imports.models.import_preview_result import (
    ImportPreviewResult,
)

from app.imports.services.category_import_service import (
    CategoryImportService,
)


class ImportPreviewService:

    def __init__(
        self,
        product_repository: ProductRepository,
        category_service: CategoryImportService,
    ):
        self.product_repository = (
            product_repository
        )

        self.category_service = (
            category_service
        )

    async def build_preview(
        self,
        products: list[ProductImportDTO],
    ) -> ImportPreviewResult:

        result = ImportPreviewResult()

        for dto in products:

            preview_item = (
                await self._analyze_product(
                    dto
                )
            )

            result.items.append(
                preview_item
            )

            if preview_item.action == "CREATE":
                result.create_count += 1

            elif preview_item.action == "UPDATE":
                result.update_count += 1

            elif preview_item.action == "SKIP":
                result.skip_count += 1

            elif preview_item.action == "ERROR":
                result.error_count += 1

        return result

    async def _analyze_product(
        self,
        dto: ProductImportDTO,
    ) -> ImportPreviewItem:

        category_exists = (
            await self.category_service
            .category_exists(
                dto.category_slug
            )
        )

        if not category_exists:

            return ImportPreviewItem(
                sku=dto.sku,
                title=dto.title,
                action="ERROR",
                dto=dto,
                errors=[
                    (
                        "Категория не найдена: "
                        f"{dto.category_slug}"
                    )
                ],
            )

        product = (
            await self.product_repository
            .get_by_sku(
                dto.sku
            )
        )

        if not product:

            photo_count = 0

            if dto.photo_files:

                photo_count = len(
                    dto.photo_files.split("|")
                )

            return ImportPreviewItem(
                sku=dto.sku,
                title=dto.title,
                action="CREATE",
                dto=dto,
                changes=[
                    "Новый товар"
                ],
                photo_count=photo_count,
            )

        changes: list[str] = []

        if product.title != dto.title:
            changes.append("Название")

        if (
            product.short_description
            != dto.short_description
        ):
            changes.append(
                "Краткое описание"
            )

        if (
            product.full_description
            != dto.full_description
        ):
            changes.append(
                "Полное описание"
            )

        if (
            product.quantity
            != dto.quantity
        ):
            changes.append(
                "Количество"
            )

        if (
            product.weight_g
            != (
                dto.weight_g or 0
            )
        ):
            changes.append(
                "Вес"
            )

        if (
            product.dimensions
            != dto.dimensions
        ):
            changes.append(
                "Размеры"
            )

        if (
            product.condition
            != dto.condition
        ):
            changes.append(
                "Состояние"
            )

        photo_count = 0

        if dto.photo_files:

            photo_count = len(
                dto.photo_files.split("|")
            )

        if not changes:

            return ImportPreviewItem(
                sku=dto.sku,
                title=dto.title,
                dto=dto,
                action="SKIP",
                changes=[
                    "Без изменений"
                ],
                photo_count=photo_count,
            )

        return ImportPreviewItem(
            sku=dto.sku,
            title=dto.title,
            action="UPDATE",
            dto=dto,
            changes=changes,
            photo_count=photo_count,
        )


# from app.database.repositories.product_repository import (
#     ProductRepository,
# )
#
# from app.imports.dto.product_import_dto import (
#     ProductImportDTO,
# )
#
# from app.imports.models.import_preview_item import (
#     ImportPreviewItem,
# )
#
# from app.imports.models.import_preview_result import (
#     ImportPreviewResult,
# )
#
# from app.imports.services.category_import_service import (
#     CategoryImportService,
# )
#
# from app.imports.services.photo_import_service import (
#     PhotoImportService,
# )
#
#
# class ImportPreviewService:
#     """
#     Предварительный анализ импорта.
#
#     Ничего не записывает в БД.
#
#     Задачи:
#
#     - определить новые товары;
#     - определить обновления;
#     - определить товары без изменений;
#     - найти ошибки;
#     - сформировать таблицу анализа.
#     """
#
#     def __init__(
#         self,
#         product_repository: ProductRepository,
#         category_service: CategoryImportService,
#         photo_service: PhotoImportService,
#     ):
#         self.product_repository = (
#             product_repository
#         )
#
#         self.category_service = (
#             category_service
#         )
#
#         self.photo_service = (
#             photo_service
#         )
#
#     async def build_preview(
#         self,
#         products: list[ProductImportDTO],
#     ) -> ImportPreviewResult:
#
#         result = ImportPreviewResult()
#
#         for dto in products:
#
#             preview_item = (
#                 await self._analyze_product(
#                     dto
#                 )
#             )
#
#             result.items.append(
#                 preview_item
#             )
#
#             if preview_item.action == "CREATE":
#                 result.create_count += 1
#
#             elif preview_item.action == "UPDATE":
#                 result.update_count += 1
#
#             elif preview_item.action == "SKIP":
#                 result.skip_count += 1
#
#             elif preview_item.action == "ERROR":
#                 result.error_count += 1
#
#         return result
#
#     async def _analyze_product(
#         self,
#         dto: ProductImportDTO,
#     ) -> ImportPreviewItem:
#
#         # ==========================================
#         # Проверяем категорию
#         # ==========================================
#
#         category_exists = (
#             await self.category_service
#             .category_exists(
#                 dto.category_path
#             )
#         )
#
#         if not category_exists:
#
#             return ImportPreviewItem(
#                 sku=dto.sku,
#                 title=dto.title,
#                 action="ERROR",
#                 errors=[
#                     (
#                         "Категория не найдена: "
#                         f"{dto.category_path}"
#                     )
#                 ],
#             )
#
#         # ==========================================
#         # Ищем товар по SKU
#         # ==========================================
#
#         product = (
#             await self.product_repository
#             .get_by_sku(
#                 dto.sku
#             )
#         )
#
#         # ==========================================
#         # Новый товар
#         # ==========================================
#
#         if not product:
#
#             photo_info = (
#                 self.photo_service
#                 .get_photo_analysis(
#                     dto.photos
#                 )
#             )
#
#             return ImportPreviewItem(
#                 sku=dto.sku,
#                 title=dto.title,
#                 action="CREATE",
#                 changes=[
#                     "Новый товар"
#                 ],
#                 photo_count=photo_info[
#                     "found"
#                 ],
#             )
#
#         # ==========================================
#         # Сравнение данных
#         # ==========================================
#
#         changes: list[str] = []
#
#         if product.title != dto.title:
#             changes.append(
#                 "Название"
#             )
#
#         if (
#             product.price_value
#             != dto.price_value
#         ):
#             changes.append(
#                 "Цена"
#             )
#
#         if (
#             product.quantity
#             != dto.quantity
#         ):
#             changes.append(
#                 "Количество"
#             )
#
#         if (
#             product.sort_priority
#             != dto.sort_priority
#         ):
#             changes.append(
#                 "Продвижение"
#             )
#
#         if (
#             product.short_description
#             != dto.short_description
#         ):
#             changes.append(
#                 "Краткое описание"
#             )
#
#         if (
#             product.full_description
#             != dto.full_description
#         ):
#             changes.append(
#                 "Полное описание"
#             )
#
#         photo_info = (
#             self.photo_service
#             .get_photo_analysis(
#                 dto.photos
#             )
#         )
#
#         # ==========================================
#         # Без изменений
#         # ==========================================
#
#         if not changes:
#
#             return ImportPreviewItem(
#                 sku=dto.sku,
#                 title=dto.title,
#                 action="SKIP",
#                 changes=[
#                     "Без изменений"
#                 ],
#                 photo_count=photo_info[
#                     "found"
#                 ],
#             )
#
#         # ==========================================
#         # Есть изменения
#         # ==========================================
#
#         return ImportPreviewItem(
#             sku=dto.sku,
#             title=dto.title,
#             action="UPDATE",
#             changes=changes,
#             photo_count=photo_info[
#                 "found"
#             ],
#         )