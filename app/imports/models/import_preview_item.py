# app/imports/models/import_preview_item.py
# ver 2.0
# updated: 2026-06-15 19:35 UTC+3

from dataclasses import dataclass
from dataclasses import field

from app.imports.dto.product_import_dto import (
    ProductImportDTO,
)


@dataclass
class ImportPreviewItem:
    """
    Одна строка предварительного анализа импорта.

    Используется:

        Preview таблица
        ImportService

    Важно:

    Хранит исходный DTO.

    Благодаря этому после подтверждения
    импорта не нужно повторно читать XLSX.
    """

    sku: str

    title: str

    action: str
    """
    CREATE
    UPDATE
    SKIP
    ERROR
    """

    dto: ProductImportDTO | None = None

    changes: list[str] = field(
        default_factory=list
    )

    photo_count: int = 0

    errors: list[str] = field(
        default_factory=list
    )
# from dataclasses import dataclass, field
#
#
# @dataclass
# class ImportPreviewItem:
#     """
#     Одна строка предварительного анализа импорта.
#
#     Используется для отображения таблицы
#     перед запуском импорта.
#     """
#
#     sku: str
#
#     title: str
#
#     action: str
#     # CREATE
#     # UPDATE
#     # SKIP
#     # ERROR
#
#     changes: list[str] = field(
#         default_factory=list
#     )
#
#     photo_count: int = 0
#
#     errors: list[str] = field(
#         default_factory=list
#     )