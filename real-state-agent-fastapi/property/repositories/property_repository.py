from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from property.entities.property_model import PropertyModel
from property.schemas.property_create_resquest import PropertyCreateRequest
from property.entities.property import Property

class PropertyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: PropertyCreateRequest, owner_id: str) -> Property:
        prop_id = str(uuid4())
        property_model = PropertyModel(
            id=prop_id,
            title=data.title,
            description=data.description,
            price=data.price,
            location=data.location,
            bedrooms=data.bedrooms,
            pet_friendly=data.pet_friendly,
            owner_id=owner_id
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
            owner_id=property_model.owner_id
        )
