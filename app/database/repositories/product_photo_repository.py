# app/database/repositories/product_photo_repository.py
# ver 1.1
# updated: 2026-06-15 21:15 UTC+3

from sqlalchemy import select

from app.database.models.product_photo import (
    ProductPhoto,
)

from app.database.repositories.base_repository import (
    BaseRepository,
)

from app.constants.shop_constants import (
    MAX_PRODUCT_PHOTOS,
)


class ProductPhotoRepository(BaseRepository):
    """
    Репозиторий фотографий товаров.
    """

    model = ProductPhoto

    async def get_by_product_id(
        self,
        product_id: int,
    ):
        """
        Получить все фотографии товара.
        """

        stmt = (
            select(ProductPhoto)
            .where(
                ProductPhoto.product_id
                == product_id
            )
            .order_by(
                ProductPhoto.position
            )
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalars().all()

    async def get_by_original_filename(
        self,
        filename: str,
    ):
        """
        Найти фото по имени файла.

        Используется при импорте
        фотографий из папки.
        """

        stmt = (
            select(ProductPhoto)
            .where(
                ProductPhoto.original_filename
                == filename
            )
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def set_telegram_file_id(
        self,
        photo_id: int,
        telegram_file_id: str,
    ):
        """
        Сохранить Telegram file_id.
        """

        photo = await self.get_by_id(
            photo_id
        )

        if not photo:
            return None

        photo.telegram_file_id = (
            telegram_file_id
        )

        await self.session.commit()

        await self.session.refresh(
            photo
        )

        return photo

    async def has_photos(
        self,
        product_id: int,
    ) -> bool:
        """
        Есть ли фото у товара.
        """

        photos = await (
            self.get_by_product_id(
                product_id
            )
        )

        return len(photos) > 0

    async def count_photos(
        self,
        product_id: int,
    ) -> int:
        """
        Количество фото товара.
        """

        photos = await (
            self.get_by_product_id(
                product_id
            )
        )

        return len(photos)

    async def can_add_photo(
        self,
        product_id: int,
    ) -> bool:
        """
        Проверка лимита фотографий.
        """

        count = await (
            self.count_photos(
                product_id
            )
        )

        return (
            count
            < MAX_PRODUCT_PHOTOS
        )

    async def get_products_without_photos(
        self,
    ):
        """
        Получить товары без фотографий.
        """

        stmt = select(
            ProductPhoto.product_id
        )

        result = await self.session.execute(
            stmt
        )

        product_ids = {
            row[0]
            for row in result.all()
        }

        return product_ids

    async def get_main_photo(
        self,
        product_id: int,
    ):
        """
        Главное фото товара.

        Главное фото имеет:

            position = 0
        """

        stmt = (
            select(ProductPhoto)
            .where(
                ProductPhoto.product_id
                == product_id,
                ProductPhoto.position
                == 0,
            )
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def get_without_telegram_file_id(
        self,
    ):
        """
        Фото без Telegram file_id.
        """

        stmt = (
            select(ProductPhoto)
            .where(
                ProductPhoto.telegram_file_id
                .is_(None)
            )
            .order_by(
                ProductPhoto.id
            )
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalars().all()

    async def update_photo_after_upload(
        self,
        photo_id: int,
        telegram_file_id: str,
        media_group_id: str,
    ):

        photo = await self.get_by_id(
            photo_id
        )

        if not photo:
            return None

        photo.telegram_file_id = (
            telegram_file_id
        )

        photo.telegram_media_group_id = (
            media_group_id
        )

        await self.session.commit()

        return photo

    async def get_all_product_ids(
        self,
    ) -> list[int]:

        stmt = (
            select(
                ProductPhoto.product_id
            )
            .distinct()
            .order_by(
                ProductPhoto.product_id
            )
        )

        result = await self.session.execute(
            stmt
        )

        return [
            row[0]
            for row in result.all()
        ]

