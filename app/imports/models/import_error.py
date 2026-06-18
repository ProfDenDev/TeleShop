# app/imports/models/import_error.py

from dataclasses import dataclass


@dataclass
class ImportError:
    """
        Ошибка импорта одной строки.
    """
    row_number: int

    sku: str | None

    field_name: str

    message: str



