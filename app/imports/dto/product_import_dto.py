# app/imports/dto/product_import_dto.py
# ver 2.0
# ver 3.0

from dataclasses import dataclass

from app.constants.currencies import UAH
from app.constants.price_types import FIXED


@dataclass
class ProductImportDTO:
    """
    DTO импорта товара.

    XLSX
        ↓
    XlsxParser
        ↓
    ProductImportDTO
        ↓
    ImportService
        ↓
    ProductService

    Важно:

    Для импорта используются:

        category_slug
        subcategory_slug
        brand_name

    Все цены после парсинга
    хранятся в минимальных единицах валюты:

        UAH -> копейки
        USD -> центы
        EUR -> евроценты
    """

    # ==================================================
    # ОБЯЗАТЕЛЬНЫЕ ПОЛЯ
    # ==================================================

    sku: str
    """
    Внутренний артикул.

    Примеры:

        DA0001
        DA0002
        DB0001
    """

    title: str
    """
    Название товара.
    """

    # ==================================================
    # ОПИСАНИЕ
    # ==================================================

    short_description: str | None = None

    full_description: str | None = None

    content_language: str | None = None

    # ==================================================
    # КАТЕГОРИИ
    # ==================================================

    category_slug: str | None = None

    subcategory_slug: str | None = None

    # ==================================================
    # БРЕНД
    # ==================================================

    brand_name: str | None = None

    # ==================================================
    # ПРОИЗВОДИТЕЛЬ
    # ==================================================

    manufacturer_name: str | None = None

    manufacturer_sku: str | None = None

    barcode: str | None = None

    serial_number: str | None = None

    # ==================================================
    # СОСТОЯНИЕ
    # ==================================================

    condition: str | None = None
    """
    NEW
    LIKE_NEW
    USED
    FOR_PARTS
    SERVICE
    """

    # ==================================================
    # ЦЕНА
    # ==================================================

    price_type: str = FIXED
    """
    FIXED
    FROM
    TO
    RANGE
    FREE
    ON_REQUEST
    NEGOTIABLE
    """

    currency: str = UAH
    """
    UAH
    USD
    EUR
    """

    price_from_value: int | None = None
    """
    Цена в копейках/центах.
    """

    price_to_value: int | None = None
    """
    Верхняя граница диапазона цены.
    """

    # ==================================================
    # СКЛАД
    # ==================================================

    quantity: int = 1

    # ==================================================
    # ФИЗИЧЕСКИЕ ПАРАМЕТРЫ
    # ==================================================

    weight_g: int | None = None

    dimensions: str | None = None

    # ==================================================
    # ДОПОЛНИТЕЛЬНО
    # ==================================================

    location_area: str | None = None

    video_url: str | None = None

    attributes_json: str | None = None

    # ==================================================
    # ФОТО
    # ==================================================

    photo_files: str | None = None
    """
    Формат:

    IMG_001.jpg

    или

    IMG_001.jpg|IMG_002.jpg

    или

    IMG_001.jpg|IMG_002.jpg|IMG_003.jpg
    """

# from dataclasses import dataclass, field
#
# from app.constants.price_types import FIXED
# from app.constants.currencies import UAH
#
# @dataclass
# class ProductPhotoImportDTO:
#     """
#     Фото товара.
#
#     Используется:
#     - ZIP импорт
#     - Telegram импорт
#     - будущие внешние импорты
#
#     Для XLSX импорта не обязательно.
#     """
#
#     filename: str | None = None
#
#     source_path: str | None = None
#
#     telegram_file_id: str | None = None
#
#     position: int = 0
#
#
# @dataclass
# class ProductImportDTO:
#     """
#     Универсальный DTO товара TELESHOP.
#
#     Минимально обязательные поля:
#
#     - sku
#     - title
#
#     Остальные поля могут отсутствовать.
#     """
#
#     # =====================================
#     # ОБЯЗАТЕЛЬНЫЕ
#     # =====================================
#
#     sku: str
#
#     title: str
#
#     # =====================================
#     # ОПИСАНИЕ
#     # =====================================
#
#     short_description: str | None = None
#
#     full_description: str | None = None
#
#     # =====================================
#     # СПРАВОЧНИКИ
#     # =====================================
#
#     category_slug: str | None = None
#
#     brand_name: str | None = None
#
#     # =====================================
#     # ЦЕНА
#     # =====================================
#
#     price_type: str | None = FIXED
#
#     currency: str = UAH
#
#     price_from_value: int | None = None
#
#     price_to_value: int | None = None
#
#     # =====================================
#     # ДОПОЛНИТЕЛЬНО
#     # =====================================
#
#     quantity: int | None = 1
#
#     weight_g: int | None = None
#
#     dimensions: str | None = None
#
#     # =====================================
#     # ФОТО
#     # =====================================
#
#     photos: list[ProductPhotoImportDTO] = field(
#         default_factory=list
#     )