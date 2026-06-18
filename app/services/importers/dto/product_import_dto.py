from dataclasses import dataclass, field


@dataclass
class ProductPhotoImportDTO:
    """
    Фото товара из внешнего источника.
    """

    filename: str | None = None

    source_path: str | None = None

    telegram_file_id: str | None = None

    position: int = 0


@dataclass
class ProductImportDTO:
    """
    Универсальный DTO товара.

    Используется всеми импортерами:

    - XLSX
    - OLX
    - Prom
    - API
    """

    sku: str

    title: str

    description: str | None = None

    category_slug: str | None = None

    brand_name: str | None = None

    price_uah: int | None = None

    quantity: int = 1

    weight_g: int | None = None

    dimensions: str | None = None

    photos: list[ProductPhotoImportDTO] = field(
        default_factory=list
    )