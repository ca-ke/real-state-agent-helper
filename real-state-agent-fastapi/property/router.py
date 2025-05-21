from fastapi import APIRouter, Depends
from property.schemas import PropertyCreateRequest, PropertyResponse
from property.usecases.register_property import RegisterPropertyUseCase
from property.dependencies import get_register_property_uc
from shared.session.user_identity import get_user_from_token

router = APIRouter(prefix="/property", tags=["property"])

@router.post("", response_model=PropertyResponse)
async def register_property(
    data: PropertyCreateRequest,
    uc: RegisterPropertyUseCase = Depends(get_register_property_uc),
    user = Depends(get_user_from_token)
):
    return await uc.execute(data, user["user_id"])