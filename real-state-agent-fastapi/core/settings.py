from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_anon_key: str
    
    database_url: str

    llm_model: str
    llm_temperature: float
    llm_base_url: str
    llm_api_key: str

    class Config:
        env_file = ".env"