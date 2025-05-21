from pydantic import BaseModel

class Property(BaseModel):
    id: str
    title: str
    description: str
    price: float
    location: str
    bedrooms: int
    pet_friendly: bool
    owner_id: str 