from typing import List
from property.schemas.property_create_response import PropertyResponse
from property.repositories.property_repository import PropertyRepository
from core.model_loader import ModelLoader

class SearchPropertyUseCase:
    def __init__(self, repo: PropertyRepository, model_loader: ModelLoader):
        self.repo = repo
        self.model_loader = model_loader

    async def execute(self, search_text: str, top_k: int = 5) -> List[PropertyResponse]:
        search_embedding = await self.model_loader.get_embedding(search_text)
        
        similar_properties = await self.repo.find_similar(search_embedding, top_k)
        
        return [
            PropertyResponse(
                id=str(prop.id),
                title=prop.title,
                price=prop.price,
                location=prop.location,
                owner_id=prop.owner_id
            )
            for prop in similar_properties
        ] 