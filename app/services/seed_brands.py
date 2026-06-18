# app/services/seed_brands.py
# ver 1.0

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.brand import Brand

from app.constants.default_brands import (
    DEFAULT_BRANDS
)


async def seed_brands(
    session: AsyncSession,
) -> None:
    """
    Первичное заполнение брендов.

    Выполняется только если таблица пуста.
    """

    result = await session.execute(
        select(Brand.id).limit(1)
    )

    existing = (
        result.scalar_one_or_none()
    )

    if existing:
        return

    sort_order = 100

    for brand_name in DEFAULT_BRANDS:

        brand = Brand(
            name=brand_name,
            sort_order=sort_order,
        )

        session.add(brand)

        sort_order += 100

    await session.commit()