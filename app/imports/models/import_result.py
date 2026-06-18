# app/imports/models/import_result.py

from dataclasses import dataclass


@dataclass
class ImportResult:

    total_rows: int = 0

    created_rows: int = 0

    updated_rows: int = 0

    skipped_rows: int = 0

    failed_rows: int = 0

    missing_photos: int = 0