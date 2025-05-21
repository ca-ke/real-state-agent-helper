from functools import lru_cache
from fastapi import Depends
from core.settings import Settings
from supabase import create_client, Client

@lru_cache
def get_settings() -> Settings:
    return Settings()

def get_supabase_client(settings: Settings = Depends(get_settings)) -> Client:
    return create_client(settings.supabase_url, settings.supabase_anon_key)
