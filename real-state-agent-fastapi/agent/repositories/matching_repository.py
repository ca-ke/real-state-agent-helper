from core.model_loader import get_model_loader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, bindparam, Float, Integer
from typing import List, Optional, Dict
from property.entities.property_model import Vector

class MatchingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model_loader = get_model_loader()

    async def match_property(self, query: str, top_k: int = 5, similarity_threshold: float = 0.2) -> Optional[List[Dict]]:
        embedding = await self.model_loader.get_embedding(query)
        
        sql = text("""
            WITH similarity_scores AS (
                SELECT 
                    id, title, description, price, location, bedrooms, pet_friendly, owner_id,
                    1 - (embedding <=> :query_embedding) AS similarity
                FROM properties
            )
            SELECT *
            FROM similarity_scores
            WHERE similarity >= :threshold  
            ORDER BY similarity DESC
            LIMIT :top_k
        """).bindparams(
            bindparam("query_embedding", type_=Vector),
            bindparam("threshold", type_=Float),
            bindparam("top_k", type_=Integer),
        )
        
        result = await self.db.execute(sql, {
            "query_embedding": embedding,
            "threshold": similarity_threshold,
            "top_k": top_k
        })

        rows = result.all()
        return [dict(r._mapping) for r in rows] if rows else None
