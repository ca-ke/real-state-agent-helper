from uuid import uuid4
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, bindparam, Float, Integer
from property.entities.property_model import PropertyModel, Vector
from property.schemas.property_create_resquest import PropertyCreateRequest
from property.entities.property import Property
from core.model_loader import ModelLoader

class PropertyRepository:
    def __init__(self, session: AsyncSession, model_loader: ModelLoader):
        self.session = session
        self.model_loader = model_loader

    async def create(self, data: PropertyCreateRequest, owner_id: str, embedding: list[float]) -> Property:
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

    async def find_similar(self, search_embedding: list[float], top_k: int = 5, threshold: float = 0.7) -> List[Property]:
        sql = text("""
            WITH similarity_scores AS (
                SELECT *,
                       1 - (embedding <=> :embedding) AS similarity
                FROM properties
            )
            SELECT *
            FROM similarity_scores
            WHERE similarity >= :threshold
            ORDER BY similarity DESC
            LIMIT :top_k
        """).bindparams(
            bindparam("embedding", type_=Vector),
            bindparam("threshold", type_=Float),
            bindparam("top_k", type_=Integer)
        )

        result = await self.session.execute(sql, {
            "embedding": search_embedding,
            "threshold": threshold,
            "top_k": top_k
        })

        rows = result.all()

        return [
            Property(
                id=row.id,
                title=row.title,
                description=row.description,
                price=row.price,
                location=row.location,
                bedrooms=row.bedrooms,
                pet_friendly=row.pet_friendly,
                owner_id=row.owner_id,
                embedding=row.embedding
            )
            for row in rows
        ]
