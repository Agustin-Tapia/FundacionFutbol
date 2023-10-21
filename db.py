import logging
from functools import lru_cache
from typing import Generator
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from config import settings
from pydantic_core import MultiHostUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import as_declarative, declared_attr, scoped_session, sessionmaker
from fastapi import Depends

logger = logging.getLogger(__name__)
SQLALCHEMY_DATABASE_URL = settings.database_url


# using sqlite
if isinstance(SQLALCHEMY_DATABASE_URL, MultiHostUrl):
    logger.warning("Using postgres")
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL.unicode_string(), pool_pre_ping=True)
else:
    logger.warning("Using sqlite")
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
