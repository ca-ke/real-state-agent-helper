from fastapi import APIRouter, Depends
from property.schemas import PropertyCreateRequest, PropertyResponse
from property.usecases.register_property import RegisterPropertyUseCase
from property.usecases.search_property import SearchPropertyUseCase
from property.dependencies import get_register_property_uc, get_search_property_uc
from shared.session.user_identity import get_user_from_token
from typing import List

router = APIRouter(prefix="/property", tags=["property"])

@router.post("", response_model=PropertyResponse)
async def register_property(
    data: PropertyCreateRequest,
    uc: RegisterPropertyUseCase = Depends(get_register_property_uc),
    user = Depends(get_user_from_token)
):
    return await uc.execute(data, user["user_id"])

@router.get("/search", response_model=List[PropertyResponse])
async def search_properties(
    query: str,
    top_k: int = 5,
    uc: SearchPropertyUseCase = Depends(get_search_property_uc)
):
    return await uc.execute(query, top_k)