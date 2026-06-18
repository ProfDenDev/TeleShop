# app/database/session.py
# ver 1.0
# created: 2026-06-16 01:10 UTC+3

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import (
    DB_PATH,
)

DATABASE_URL = (
    f"sqlite+aiosqlite:///{DB_PATH}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    """
    Получить AsyncSession.
    """

    async with SessionLocal() as session:
        yield session
