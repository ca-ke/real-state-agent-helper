from functools import lru_cache
from fastapi import Depends
from core.settings import Settings
from supabase import create_client, Client
from core.database import get_engine, get_session_factory
from sqlalchemy.ext.asyncio import AsyncSession
from core.model_loader import ModelLoader, get_model_loader
from core.repositories import LLMRepository
from typing import AsyncGenerator

@lru_cache
def get_settings() -> Settings:
    return Settings()

@lru_cache
def get_llm_repository() -> LLMRepository:
    settings = get_settings()
    return LLMRepository(settings)

def get_supabase_client(settings: Settings = Depends(get_settings)) -> Client:
    return create_client(settings.supabase_url, settings.supabase_anon_key)

async def get_db_session(settings: Settings = Depends(get_settings)) -> AsyncGenerator[AsyncSession, None]:
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    async with session_factory() as session:
        yield session

def get_embedding_model() -> ModelLoader:
    return get_model_loader()
