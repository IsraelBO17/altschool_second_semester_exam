from typing import Annotated, AsyncGenerator, Optional
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import SQLAlchemyError
from .settings import get_settings


settings = get_settings()

async_engine = None
SessionDep: Annotated[Optional[AsyncSession], Depends] = Depends(lambda: None)

url = make_url(settings.DATABASE_URL)
async_engine = create_async_engine(url.render_as_string(), echo=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        try:
            yield session
        except SQLAlchemyError as exc:
            await session.rollback()
            raise exc

SessionDep = Annotated[AsyncSession, Depends(get_session)]

