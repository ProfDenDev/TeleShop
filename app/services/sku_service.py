# app/services/sku_service.py
# ver 1.0
# created: 2026-06-15 22:15 UTC+3
#
# Назначение:
# Генерация следующего SKU.
#
# Используется:
#
# - OLX импорт
# - XLSX импорт
# - Telegram Bot
# - Mini App
#
# Формат SKU:
#
# DA0001
# DA0002
# DA0003
#
# Сервис автоматически находит
# последний SKU в базе и
# генерирует следующий.

from app.database.repositories.product_repository import (
    ProductRepository,
)


class SkuService:
    """
    Сервис генерации SKU.
    """

    def __init__(
        self,
        product_repository: ProductRepository,
    ):
        self.product_repository = (
            product_repository
        )

    async def generate_next_sku(
        self,
        prefix: str = "DA",
    ) -> str:
        """
        Получить следующий SKU.

        Пример:

            DA0001
            DA0002
            DA0003
        """

        last_sku = await (
            self.product_repository
            .get_last_sku_by_prefix(
                prefix
            )
        )

        # =====================================
        # База пустая
        # =====================================

        if not last_sku:

            return (
                f"{prefix}0001"
            )

        # =====================================
        # DA0042 -> 42
        # =====================================

        try:

            number = int(
                last_sku.replace(
                    prefix,
                    "",
                )
            )

        except ValueError:

            return (
                f"{prefix}0001"
            )

        number += 1

        # =====================================
        # DA0043
        # =====================================

        return (
            f"{prefix}{number:04d}"
        )

    async def generate_many(
        self,
        count: int,
        prefix: str = "DA",
    ) -> list[str]:
        """
        Сгенерировать несколько SKU подряд.

        Пример:

            DA0001
            DA0002
            DA0003
        """

        first_sku = await (
            self.generate_next_sku(
                prefix
            )
        )

        start_number = int(
            first_sku.replace(
                prefix,
                "",
            )
        )

        result = []

        for i in range(count):

            result.append(
                f"{prefix}{start_number + i:04d}"
            )

        return result
