# app/services/product_photo_service.py
# ver 1.0
# created: 2026-06-15 20:10 UTC+3

from app.database.repositories.product_photo_repository import (
    ProductPhotoRepository,
)


class ProductPhotoService:
    """
    Сервис фотографий товаров.

    Используется:

        XLSX импорт
        ZIP импорт фото
        Telegram Bot
    """

    def __init__(
        self,
        photo_repository: ProductPhotoRepository,
    ):
        self.photo_repository = (
            photo_repository
        )

    async def create_photos_from_import(
        self,
        product_id: int,
        photo_files: str | None,
    ):
        """
        Создать записи фотографий
        из строки XLSX.

        Пример:

            IMG_001.jpg|IMG_002.jpg|IMG_003.jpg
        """

        if not photo_files:
            return []

        created_photos = []

        files = [
            item.strip()
            for item in photo_files.split("|")
            if item.strip()
        ]

        for position, filename in enumerate(files):

            photo = await (
                self.photo_repository
                .create(
                    product_id=product_id,

                    original_filename=filename,

                    original_relative_path=filename,

                    position=position,
                )
            )

            created_photos.append(
                photo
            )

        return created_photos

    async def replace_photos(
        self,
        product_id: int,
        photo_files: str | None,
    ):
        """
        Полностью заменить список фото.
        """

        existing_photos = await (
            self.photo_repository
            .get_by_product_id(
                product_id
            )
        )

        for photo in existing_photos:

            await (
                self.photo_repository
                .delete(photo)
            )

        return await (
            self.create_photos_from_import(
                product_id=product_id,
                photo_files=photo_files,
            )
        )

    async def count_photos(
        self,
        product_id: int,
    ) -> int:

        return await (
            self.photo_repository
            .count_photos(
                product_id
            )
        )

    async def has_photos(
        self,
        product_id: int,
    ) -> bool:

        return await (
            self.photo_repository
            .has_photos(
                product_id
            )
        )
