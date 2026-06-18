# run_telegram_photo_import.py
# ver 1.0
# created: 2026-06-16 06:00 UTC+3

import asyncio

from aiogram import Bot

from app.config import (
    BOT_TOKEN,
)

from app.database.session import (
    SessionLocal,
)

from app.database.repositories.product_photo_repository import (
    ProductPhotoRepository,
)

from app.services.telegram_photo_import_service import (
    TelegramPhotoImportService,
)


async def main():

    bot = Bot(
        token=BOT_TOKEN
    )

    async with SessionLocal() as session:

        repository = (
            ProductPhotoRepository(
                session
            )
        )

        service = (
            TelegramPhotoImportService(
                bot=bot,
                product_photo_repository=repository,
            )
        )

        result = await (
            service.import_all()
        )

        print()
        print("=" * 50)
        print(result)
        print("=" * 50)

    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(
        main()
    )
