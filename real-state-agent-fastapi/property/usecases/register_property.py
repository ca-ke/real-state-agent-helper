from property.schemas.property_create_resquest import PropertyCreateRequest
from property.schemas.property_create_response import PropertyResponse
from property.repositories.property_repository import PropertyRepository

class RegisterPropertyUseCase:
    def __init__(self, repo: PropertyRepository):
        self.repo = repo

    async def execute(self, data: PropertyCreateRequest, owner_id: str) -> PropertyResponse:
        property = await self.repo.create(data, owner_id)
        return PropertyResponse(
            id=property.id,
            title=property.title,
            price=property.price,
            location=property.location,
            owner_id=property.owner_id
        )
