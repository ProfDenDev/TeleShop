# app/imports/services/import_service.py
# ver 2.0
# updated: 2026-06-15 19:45 UTC+3

from app.imports.models.import_result import (
    ImportResult,
)

from app.imports.models.import_preview_result import (
    ImportPreviewResult,
)

from app.imports.parsers.xlsx_parser import (
    XlsxParser,
)

from app.imports.services.import_preview_service import (
    ImportPreviewService,
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

class ImportService:
    """
    Главный сервис импорта TELESHOP.
    """

    def __init__(
        self,
        preview_service: ImportPreviewService,
        product_service: ProductService,
        product_price_service: ProductPriceService,
        product_photo_service: ProductPhotoService,
    ):
        self.preview_service = (
            preview_service
        )

        self.product_service = (
            product_service
        )

        self.product_price_service = (
            product_price_service
        )

        self.product_photo_service = (
            product_photo_service
        )

    async def build_preview(
        self,
        xlsx_file_path: str,
    ) -> ImportPreviewResult:

        parser = XlsxParser(
            file_path=xlsx_file_path,
        )

        products = parser.parse()

        return await (
            self.preview_service
            .build_preview(
                products
            )
        )

    async def execute_import(
        self,
        preview_result: ImportPreviewResult,
        selected_sku: list[str],
    ) -> ImportResult:

        result = ImportResult()

        for item in preview_result.items:

            if item.sku not in selected_sku:
                continue

            try:

                dto = item.dto

                if not dto:

                    result.failed_rows += 1
                    continue

                # ==========================
                # CREATE
                # ==========================

                if item.action == "CREATE":

                    product = await (
                        self.product_service
                        .create_product(
                            dto
                        )
                    )

                    await (
                        self.product_photo_service
                        .create_photos_from_import(
                            product_id=product.id,
                            photo_files=dto.photo_files,
                        )
                    )

                    await (
                        self.product_price_service
                        .create_or_update_price(
                            product_id=product.id,

                            price_type=(
                                dto.price_type
                            ),

                            currency=(
                                dto.currency
                            ),

                            price_from_value=(
                                dto.price_from_value
                            ),

                            price_to_value=(
                                dto.price_to_value
                            ),
                        )
                    )

                    result.created_rows += 1

                # ==========================
                # UPDATE
                # ==========================

                elif item.action == "UPDATE":

                    product = await (
                        self.product_service
                        .get_by_sku(
                            dto.sku
                        )
                    )

                    if not product:
                        result.failed_rows += 1
                        continue

                    await (
                        self.product_photo_service
                        .replace_photos(
                            product_id=product.id,
                            photo_files=dto.photo_files,
                        )
                    )

                    await (
                        self.product_service
                        .update_product(
                            product,
                            dto,
                        )
                    )

                    await (
                        self.product_price_service
                        .create_or_update_price(
                            product_id=product.id,

                            price_type=(
                                dto.price_type),

                            currency=(
                                dto.currency),

                            price_from_value=(
                                dto.price_from_value
                            ),

                            price_to_value=(
                                dto.price_to_value
                            ),
                        )
                    )

                    result.updated_rows += 1

                # ==========================
                # SKIP
                # ==========================

                elif item.action == "SKIP":

                    result.skipped_rows += 1

                # ==========================
                # ERROR
                # ==========================

                elif item.action == "ERROR":

                    result.failed_rows += 1

            except Exception:

                result.failed_rows += 1

        result.total_rows = (
            result.created_rows
            + result.updated_rows
            + result.skipped_rows
            + result.failed_rows
        )

        return result

