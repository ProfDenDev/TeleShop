# app/imports/models/import_preview_result.py

from dataclasses import dataclass, field

from app.imports.models.import_preview_item import (
    ImportPreviewItem,
)


@dataclass
class ImportPreviewResult:
    """
    Результат предварительного анализа импорта.

    Используется для формирования таблицы
    перед подтверждением импорта.
    """

    items: list[ImportPreviewItem] = field(
        default_factory=list
    )

    create_count: int = 0

    update_count: int = 0

    skip_count: int = 0

    error_count: int = 0