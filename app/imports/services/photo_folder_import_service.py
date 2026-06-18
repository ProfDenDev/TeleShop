# app/imports/services/photo_folder_import_service.py
# ver 1.0
# created: 2026-06-15 21:05 UTC+3

from pathlib import Path

from app.database.repositories.product_photo_repository import (
    ProductPhotoRepository,
)

from app.services.telegram_photo_service import (
    TelegramPhotoService,
)

from app.imports.models.photo_import_result import (
    PhotoImportResult,
)


class PhotoFolderImportService:
    """
    Импорт фотографий товаров из папки.

    Алгоритм:

        storage/imports/photos/
                ↓

        IMG_001.jpg
                ↓

        поиск ProductPhoto
        по original_filename

                ↓

        загрузка в Telegram

                ↓

        получение file_id

                ↓

        сохранение telegram_file_id

                ↓

        удаление локального файла
    """

    def __init__(
        self,
        photo_repository: ProductPhotoRepository,
        telegram_photo_service: TelegramPhotoService,
        import_photos_chat_id: int,
    ):
        self.photo_repository = (
            photo_repository
        )

        self.telegram_photo_service = (
            telegram_photo_service
        )

        self.import_photos_chat_id = (
            import_photos_chat_id
        )

    async def import_folder(
        self,
        photos_directory: str,
        delete_after_import: bool = True,
    ) -> PhotoImportResult:
        """
        Импортировать все фотографии
        из папки.

        Возвращает статистику.
        """

        result = PhotoImportResult()

        photos_path = Path(
            photos_directory
        )

        if not photos_path.exists():

            return result

        image_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        }

        files = [
            file
            for file in photos_path.iterdir()
            if (
                file.is_file()
                and file.suffix.lower()
                in image_extensions
            )
        ]

        result.total_files = (
            len(files)
        )

        for file_path in files:

            try:

                filename = (
                    file_path.name
                )

                photo = await (
                    self.photo_repository
                    .get_by_original_filename(
                        filename
                    )
                )

                if not photo:

                    result.not_found_in_db += 1

                    continue

                if photo.telegram_file_id:

                    result.already_uploaded += 1

                    continue

                telegram_file_id = (
                    await self
                    .telegram_photo_service
                    .upload_photo(
                        chat_id=(
                            self
                            .import_photos_chat_id
                        ),
                        photo_path=str(
                            file_path
                        ),
                    )
                )

                await (
                    self.photo_repository
                    .set_telegram_file_id(
                        photo_id=photo.id,
                        telegram_file_id=(
                            telegram_file_id
                        ),
                    )
                )

                result.imported += 1

                if delete_after_import:

                    self\
                    .telegram_photo_service\
                    .delete_temp_file(
                        str(file_path)
                    )

            except Exception as e:

                print(
                    f"Photo import error: "
                    f"{e}"
                )

                result.errors += 1

        return result
