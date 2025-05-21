from fastapi import Depends
from core.dependencies import get_db_session, get_embedding_model
from property.repositories.property_repository import PropertyRepository
from property.usecases.register_property import RegisterPropertyUseCase
from property.usecases.search_property import SearchPropertyUseCase
from core.model_loader import ModelLoader
from sqlalchemy.ext.asyncio import AsyncSession

def get_property_repo(
    session = Depends(get_db_session),
    model_loader: ModelLoader = Depends(get_embedding_model)
) -> PropertyRepository:
    return PropertyRepository(session, model_loader)

async def get_register_property_uc(
    session: AsyncSession = Depends(get_db_session),
    model_loader: ModelLoader = Depends(get_embedding_model)
) -> RegisterPropertyUseCase:
    repo = PropertyRepository(session, model_loader)
    return RegisterPropertyUseCase(repo, model_loader)

async def get_search_property_uc(
    session: AsyncSession = Depends(get_db_session),
    model_loader: ModelLoader = Depends(get_embedding_model)
) -> SearchPropertyUseCase:
    repo = PropertyRepository(session, model_loader)
    return SearchPropertyUseCase(repo, model_loader)
