# app/imports/validators/product_validator.py

from app.imports.dto.product_import_dto import (
    ProductImportDTO,
)

from app.imports.models.import_error import (
    ImportError,
)


class ProductValidator:
    """
    Проверка данных товара перед импортом.

    Валидатор не работает с БД.

    Его задача:
    - проверить обязательные поля;
    - проверить типы данных;
    - вернуть список ошибок.

    Проверка существования категорий,
    брендов и валют будет выполняться
    отдельными сервисами импорта.
    """

    REQUIRED_FIELDS = (
        "sku",
        "title",
        "category_path",
        "price_value",
        "currency",
        "status",
    )

    def validate(
        self,
        dto: ProductImportDTO,
        row_number: int,
    ) -> list[ImportError]:

        errors: list[ImportError] = []

        # ==================================================
        # SKU
        # ==================================================

        if not dto.sku:
            errors.append(
                ImportError(
                    row_number=row_number,
                    sku=None,
                    field_name="sku",
                    message="SKU обязателен",
                )
            )

        # ==================================================
        # Название
        # ==================================================

        if not dto.title:
            errors.append(
                ImportError(
                    row_number=row_number,
                    sku=dto.sku,
                    field_name="title",
                    message="Название обязательно",
                )
            )

        # ==================================================
        # Категория
        # ==================================================

        if not dto.category_path:
            errors.append(
                ImportError(
                    row_number=row_number,
                    sku=dto.sku,
                    field_name="category_path",
                    message="Категория обязательна",
                )
            )

        # ==================================================
        # Цена
        # ==================================================

        if dto.price_value is None:
            errors.append(
                ImportError(
                    row_number=row_number,
                    sku=dto.sku,
                    field_name="price_value",
                    message="Цена обязательна",
                )
            )

        elif dto.price_value <= 0:
            errors.append(
                ImportError(
                    row_number=row_number,
                    sku=dto.sku,
                    field_name="price_value",
                    message="Цена должна быть больше нуля",
                )
            )

        # ==================================================
        # Валюта
        # ==================================================

        # if not dto.currency:
        #     errors.append(
        #         ImportError(
        #             row_number=row_number,
        #             sku=dto.sku,
        #             field_name="currency",
        #             message="Валюта обязательна",
        #         )
        #     )

        # ==================================================
        # Статус
        # ==================================================

        if not dto.status:
            errors.append(
                ImportError(
                    row_number=row_number,
                    sku=dto.sku,
                    field_name="status",
                    message="Статус обязателен",
                )
            )

        # ==================================================
        # Количество
        # ==================================================

        if (
            dto.quantity is not None
            and dto.quantity < 0
        ):
            errors.append(
                ImportError(
                    row_number=row_number,
                    sku=dto.sku,
                    field_name="quantity",
                    message="Количество не может быть отрицательным",
                )
            )

        # ==================================================
        # Вес
        # ==================================================

        if (
            dto.weight_g is not None
            and dto.weight_g < 0
        ):
            errors.append(
                ImportError(
                    row_number=row_number,
                    sku=dto.sku,
                    field_name="weight_g",
                    message="Вес не может быть отрицательным",
                )
            )

        return errors