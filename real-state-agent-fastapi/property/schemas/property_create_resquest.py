from pydantic import BaseModel

class PropertyCreateRequest(BaseModel):
    title: str
    description: str
    price: float
    location: str
    bedrooms: int
    pet_friendly: bool = False