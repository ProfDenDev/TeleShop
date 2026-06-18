# app/imports/services/brand_import_service.py

from app.database.models.brand import (
    Brand,
)

from app.database.repositories.brand_repository import (
    BrandRepository,
)


class BrandImportService:
    """
    Работа с брендами во время импорта.

    Правила TELESHOP:

    - бренд не обязателен;
    - если бренд найден -> использовать;
    - если бренд не найден -> создать;
    - если бренд пустой -> вернуть None.
    """

    def __init__(
        self,
        brand_repository: BrandRepository,
    ):
        self.brand_repository = (
            brand_repository
        )

    async def get_or_create_brand(
        self,
        brand_name: str | None,
    ) -> Brand | None:

        if not brand_name:
            return None

        brand_name = brand_name.strip()

        if not brand_name:
            return None

        brand = (
            await self.brand_repository
            .get_by_name(
                brand_name
            )
        )

        if brand:
            return brand

        return await self.brand_repository.create(
            {
                "name": brand_name,
            }
        )