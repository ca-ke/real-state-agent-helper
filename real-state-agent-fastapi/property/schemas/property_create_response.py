from pydantic import BaseModel

class PropertyResponse(BaseModel):
    id: str
    title: str
    price: float
    location: str
    owner_id: str