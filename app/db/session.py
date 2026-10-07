from app.core.config import Settings, get_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import Annotated
from fastapi import Depends
from collections.abc import AsyncIterator

settings: Settings = get_settings()


engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={"server_settings": {"search_path": settings.DB_SCHEMA}}
)


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

SessionDep = Annotated[AsyncSession, Depends(get_session, scope="function")]

StreamingSessionDep = Annotated[AsyncSession,
                                Depends(get_session, scope="function")]
