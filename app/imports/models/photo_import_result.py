# app/imports/models/photo_import_result.py
# ver 1.0
# created: 2026-06-15 21:20 UTC+3

from dataclasses import dataclass


@dataclass
class PhotoImportResult:
    """
    Результат импорта фотографий.
    """

    total_files: int = 0

    imported: int = 0

    already_uploaded: int = 0

    not_found_in_db: int = 0

    errors: int = 0