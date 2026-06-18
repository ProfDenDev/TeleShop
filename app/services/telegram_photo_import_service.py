# # app/services/telegram_photo_import_service.py
# # ver 1.0
# # created: 2026-06-16 06:00 UTC+3
# ver 2.0
# updated: 2026-06-18
#
# Загрузка фотографий товаров в Telegram альбомами.
#
# Логика:
# 1 товар = 1 sendMediaGroup()
#
# После загрузки:
# telegram_file_id -> сохраняется
# media_group_id -> пишется в original_relative_path
#
# Временное решение для первых 20 товаров.
# Потом логика будет перенесена в OlxJsonImportService.

from pathlib import Path
import asyncio

from aiogram import Bot
from aiogram.types import (
    FSInputFile,
    InputMediaPhoto,
)

from aiogram.exceptions import (
    TelegramRetryAfter,
)

from app.config import (
    IMPORT_PHOTOS_CHAT_ID,
)

from app.database.repositories.product_photo_repository import (
    ProductPhotoRepository,
)


class TelegramPhotoImportService:

    def __init__(
        self,
        bot: Bot,
        product_photo_repository: ProductPhotoRepository,
    ):
        self.bot = bot

        self.product_photo_repository = (
            product_photo_repository
        )

    async def import_all(self):

        imported = 0
        errors = 0

        product_ids = await (
            self.product_photo_repository
            .get_all_product_ids()
        )

        print()
        print(
            f"FOUND PRODUCTS: {len(product_ids)}"
        )
        print()

        for product_id in product_ids:

            try:

                photos = await (
                    self.product_photo_repository
                    .get_by_product_id(
                        product_id
                    )
                )

                if not photos:
                    continue

                media = []

                valid_photos = []

                for photo in photos:

                    file_path = Path(
                        "storage/imports"
                    ) / photo.original_filename

                    if not file_path.exists():

                        print(
                            f"FILE NOT FOUND: {file_path}"
                        )

                        errors += 1
                        continue

                    media.append(
                        InputMediaPhoto(
                            media=FSInputFile(
                                str(file_path)
                            )
                        )
                    )

                    valid_photos.append(
                        photo
                    )

                if not media:
                    continue

                while True:

                    try:

                        messages = await (
                            self.bot.send_media_group(
                                chat_id=(
                                    IMPORT_PHOTOS_CHAT_ID
                                ),
                                media=media,
                            )
                        )

                        break

                    except TelegramRetryAfter as e:

                        print(
                            "RATE LIMIT:"
                            f" wait {e.retry_after}"
                        )

                        await asyncio.sleep(
                            e.retry_after + 1
                        )

                media_group_id = (
                    str(
                        messages[0]
                        .media_group_id
                    )
                    if (
                        messages[0]
                        .media_group_id
                    )
                    else ""
                )

                for (
                    photo,
                    message,
                ) in zip(
                    valid_photos,
                    messages,
                ):

                    telegram_file_id = (
                        message.photo[-1]
                        .file_id
                    )

                    await (
                        self.product_photo_repository
                        .update_photo_after_upload(
                            photo_id=photo.id,
                            telegram_file_id=(
                                telegram_file_id
                            ),
                            media_group_id=(
                                media_group_id
                            ),
                        )
                    )

                    imported += 1

                print(
                    f"PRODUCT {product_id}"
                    f" -> {len(valid_photos)} photos"
                    f" uploaded"
                )

                await asyncio.sleep(
                    1
                )

            except Exception as e:

                print()
                print(
                    f"PRODUCT ERROR "
                    f"{product_id}: {e}"
                )
                print()

                errors += 1

        print()
        print("=" * 50)

        return {
            "imported": imported,
            "errors": errors,
        }



#
# from pathlib import Path
#
# from aiogram import Bot
# from aiogram.types import FSInputFile
#
# from app.config import (
#     IMPORT_PHOTOS_CHAT_ID,
# )
#
# from app.database.repositories.product_photo_repository import (
#     ProductPhotoRepository,
# )
#
# from aiogram.exceptions import (
#     TelegramRetryAfter,
# )
#
# import asyncio
#
#
# class TelegramPhotoImportService:
#     """
#     Загрузка фотографий в Telegram.
#
#     Получает file_id и сохраняет
#     его в ProductPhoto.
#     """
#
#     def __init__(
#         self,
#         bot: Bot,
#         product_photo_repository: ProductPhotoRepository,
#     ):
#         self.bot = bot
#
#         self.product_photo_repository = (
#             product_photo_repository
#         )
#
#     async def import_all(self):
#
#         photos = await (
#             self.product_photo_repository
#             .get_without_telegram_file_id()
#         )
#
#         imported = 0
#         errors = 0
#
#         for photo in photos:
#
#             try:
#
#                 file_path = Path(
#                     "storage/imports"
#                 ) / photo.original_relative_path
#
#                 if not file_path.exists():
#
#                     print(
#                         f"FILE NOT FOUND: {file_path}"
#                     )
#
#                     errors += 1
#                     continue
#
#                 telegram_photo = (
#                     FSInputFile(
#                         str(file_path)
#                     )
#                 )
#
#                 message = await (
#                     self.bot.send_photo(
#                         chat_id=(
#                             IMPORT_PHOTOS_CHAT_ID
#                         ),
#                         photo=telegram_photo,
#                     )
#                 )
#
#                 telegram_file_id = (
#                     message.photo[-1]
#                     .file_id
#                 )
#
#                 await (
#                     self.product_photo_repository
#                     .set_telegram_file_id(
#                         photo.id,
#                         telegram_file_id,
#                     )
#                 )
#
#                 imported += 1
#
#             except Exception as e:
#
#                 print(
#                     f"PHOTO ERROR: {e}"
#                 )
#
#                 errors += 1
#
#         return {
#             "imported": imported,
#             "errors": errors,
#         }
