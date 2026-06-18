# app/services/telegram_photo_service.py
# ver 1.0
# created: 2026-06-15 20:30 UTC+3

from pathlib import Path

from aiogram import Bot


class TelegramPhotoService:
    """
    Сервис загрузки фотографий в Telegram.

    После загрузки получаем:

        telegram_file_id

    и сохраняем его в БД.

    Локальные файлы после загрузки
    могут быть удалены.
    """

    def __init__(
        self,
        bot: Bot,
    ):
        self.bot = bot

    async def upload_photo(
        self,
        chat_id: int,
        photo_path: str,
    ) -> str:
        """
        Загрузить фото в Telegram.

        Возвращает telegram_file_id.
        """

        path = Path(
            photo_path
        )

        with open(
            path,
            "rb",
        ) as photo:

            message = await (
                self.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                )
            )

        telegram_file_id = (
            message.photo[-1].file_id
        )

        return telegram_file_id

    async def upload_product_photo(
        self,
        chat_id: int,
        photo_path: str,
    ) -> str:
        """
        Обертка для загрузки
        фотографии товара.
        """

        return await (
            self.upload_photo(
                chat_id=chat_id,
                photo_path=photo_path,
            )
        )

    def delete_temp_file(
        self,
        photo_path: str,
    ) -> None:
        """
        Удалить временный файл.
        """

        path = Path(
            photo_path
        )

        if path.exists():

            path.unlink()