# app/services/telegram_album_service.py
# ver 1.0 created: 2026-06-18 22:50 UTC+3

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


class TelegramAlbumService:
    """
    Загрузка фотографий товара в Telegram.

    Поддерживает:

    - одно фото
    - альбомы
    - TelegramRetryAfter

    Возвращает:

    - telegram_file_id
    - telegram_media_group_id
    """

    def __init__(
        self,
        bot: Bot,
    ):
        self.bot = bot

    async def upload_photos(
        self,
        image_paths: list[str],
    ) -> dict:

        if not image_paths:

            return {
                "media_group_id": None,
                "photos": [],
            }

        # =====================================
        # Одно фото
        # =====================================

        if len(image_paths) == 1:

            while True:

                try:

                    message = await (
                        self.bot.send_photo(
                            chat_id=(
                                IMPORT_PHOTOS_CHAT_ID
                            ),
                            photo=FSInputFile(
                                image_paths[0]
                            ),
                        )
                    )

                    break

                except TelegramRetryAfter as e:

                    await asyncio.sleep(
                        e.retry_after + 1
                    )

            return {
                "media_group_id": None,
                "photos": [
                    {
                        "path": image_paths[0],
                        "file_id": (
                            message.photo[-1]
                            .file_id
                        ),
                    }
                ],
            }

        # =====================================
        # Альбом
        # =====================================

        media = []

        for image_path in image_paths:

            media.append(
                InputMediaPhoto(
                    media=FSInputFile(
                        image_path
                    )
                )
            )

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

                await asyncio.sleep(
                    e.retry_after + 1
                )

        media_group_id = None

        if (
            messages
            and messages[0].media_group_id
        ):
            media_group_id = str(
                messages[0]
                .media_group_id
            )

        photos = []

        for (
            image_path,
            message,
        ) in zip(
            image_paths,
            messages,
        ):

            photos.append(
                {
                    "path": image_path,
                    "file_id": (
                        message.photo[-1]
                        .file_id
                    ),
                }
            )

        return {
            "media_group_id": (
                media_group_id
            ),
            "photos": photos,
        }
