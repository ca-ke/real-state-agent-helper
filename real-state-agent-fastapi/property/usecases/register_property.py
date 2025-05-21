from property.schemas.property_create_resquest import PropertyCreateRequest
from property.schemas.property_create_response import PropertyResponse
from property.repositories.property_repository import PropertyRepository
from core.model_loader import ModelLoader

class RegisterPropertyUseCase:
    def __init__(self, repo: PropertyRepository, model_loader: ModelLoader):
        self.repo = repo
        self.model_loader = model_loader

    async def execute(self, data: PropertyCreateRequest, owner_id: str) -> PropertyResponse:
        pet_str = "pet friendly" if data.pet_friendly else "no pets allowed"
        text_for_embedding = (
            f"{data.title} {data.description}. "
            f"Price: ${data.price:.2f}. "
            f"{data.bedrooms} bedrooms. "
            f"{pet_str}."
        )
        embedding = await self.model_loader.get_embedding(text_for_embedding)
        
        entity = await self.repo.create(data, owner_id, embedding)

        return PropertyResponse(
            id=str(entity.id),
            title=entity.title,
            price=entity.price,
            location=entity.location,
            owner_id=entity.owner_id
        )
