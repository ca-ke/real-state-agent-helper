from fastapi import Depends
from core.dependencies import get_db_session
from property.repositories.property_repository import PropertyRepository
from property.usecases.register_property import RegisterPropertyUseCase

def get_property_repo(
    session = Depends(get_db_session)
) -> PropertyRepository:
    return PropertyRepository(session)

def get_register_property_uc(
    repo: PropertyRepository = Depends(get_property_repo)
) -> RegisterPropertyUseCase:
    return RegisterPropertyUseCase(repo)
