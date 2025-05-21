from functools import lru_cache
from fastapi import Depends
from core.settings import Settings
from supabase import create_client, Client
from core.database import get_engine, get_session_factory
from sqlalchemy.ext.asyncio import AsyncSession

@lru_cache
def get_settings() -> Settings:
    return Settings()

def get_supabase_client(settings: Settings = Depends(get_settings)) -> Client:
    return create_client(settings.supabase_url, settings.supabase_anon_key)

async def get_db_session(settings: Settings = Depends(get_settings)) -> AsyncSession:
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    async with session_factory() as session:
        yield session
