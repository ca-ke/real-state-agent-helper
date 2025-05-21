from pydantic import BaseModel

class CallRequest(BaseModel):
    query: str