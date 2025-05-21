from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from core.settings import Settings

class Base(DeclarativeBase):
    pass

def get_engine(settings: Settings):
    return create_async_engine(
        settings.database_url.replace('postgresql://', 'postgresql+asyncpg://'),
        echo=True,
        future=True
    )

def get_session_factory(engine):
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    ) 