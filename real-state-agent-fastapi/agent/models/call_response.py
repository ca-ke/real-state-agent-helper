from pydantic import BaseModel

class CallResponse(BaseModel):
    message: str
    matched_property_id: str
    owner_id: str