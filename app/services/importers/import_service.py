# app/imports/services/import_service.py

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


class ImportService:
    """
    Главный сервис импорта TELESHOP.

    Отвечает за:

    - чтение XLSX;
    - запуск предварительного анализа;
    - запуск импорта;
    - формирование итогового отчета.

    Важно:

    Этот сервис управляет процессом,
    но сам не работает напрямую с БД.
    """

    def __init__(
        self,
        preview_service: ImportPreviewService,
    ):
        self.preview_service = (
            preview_service
        )

    async def build_preview(
        self,
        xlsx_file_path: str,
    ) -> ImportPreviewResult:
        """
        Выполняет предварительный анализ.

        Ничего не изменяет в БД.
        """

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
        """
        Выполнить импорт выбранных товаров.

        Пока реализована только заготовка.

        Реальная запись в БД будет
        добавлена после создания:

        - ProductService
        - ProductPhotoService
        - TelegramPhotoService
        """

        result = ImportResult()

        for item in preview_result.items:

            if item.sku not in selected_sku:
                continue

            # ==================================
            # CREATE
            # ==================================

            if item.action == "CREATE":

                # TODO:
                # ProductService.create()

                result.created_rows += 1

            # ==================================
            # UPDATE
            # ==================================

            elif item.action == "UPDATE":

                # TODO:
                # ProductService.update()

                result.updated_rows += 1

            # ==================================
            # ERROR
            # ==================================

            elif item.action == "ERROR":

                result.failed_rows += 1

            # ==================================
            # SKIP
            # ==================================

            elif item.action == "SKIP":

                result.skipped_rows += 1

        result.total_rows = (
            result.created_rows
            + result.updated_rows
            + result.skipped_rows
            + result.failed_rows
        )

        return result