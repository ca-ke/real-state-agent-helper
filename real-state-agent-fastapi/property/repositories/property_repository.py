from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from property.entities.property_model import PropertyModel
from property.schemas.property_create_resquest import PropertyCreateRequest
from property.entities.property import Property
from core.model_loader import ModelLoader
import numpy as np

class PropertyRepository:
    def __init__(self, session: AsyncSession, model_loader: ModelLoader):
        self.session = session
        self.model_loader = model_loader

    async def create(self, data: PropertyCreateRequest, owner_id: str, embedding: list) -> Property:
        prop_id = str(uuid4())
        
        property_model = PropertyModel(
            id=prop_id,
            title=data.title,
            description=data.description,
            price=data.price,
            location=data.location,
            bedrooms=data.bedrooms,
            pet_friendly=data.pet_friendly,
            owner_id=owner_id,
            embedding=embedding
        )
        
        self.session.add(property_model)
        await self.session.commit()
        await self.session.refresh(property_model)
        
        return Property(
            id=property_model.id,
            title=property_model.title,
            description=property_model.description,
            price=property_model.price,
            location=property_model.location,
            bedrooms=property_model.bedrooms,
            pet_friendly=property_model.pet_friendly,
            owner_id=property_model.owner_id,
            embedding=property_model.embedding
        )

    async def find_similar(self, search_embedding: list, top_k: int = 5) -> list[Property]:
        search_embedding_np = np.array(search_embedding)
        
        query = select(PropertyModel)
        result = await self.session.execute(query)
        properties = result.scalars().all()
        
        similarities = []
        for prop in properties:
            prop_embedding = np.array(prop.embedding)
            similarity = np.dot(search_embedding_np, prop_embedding) / (
                np.linalg.norm(search_embedding_np) * np.linalg.norm(prop_embedding)
            )
            similarities.append((prop, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_properties = [prop for prop, _ in similarities[:top_k]]
        
        return [
            Property(
                id=prop.id,
                title=prop.title,
                description=prop.description,
                price=prop.price,
                location=prop.location,
                bedrooms=prop.bedrooms,
                pet_friendly=prop.pet_friendly,
                owner_id=prop.owner_id,
                embedding=prop.embedding
            )
            for prop in top_properties
        ]
