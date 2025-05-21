from sqlalchemy import Column, String, Float, Integer, Boolean
from core.database import Base

class PropertyModel(Base):
    __tablename__ = "properties"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    pet_friendly = Column(Boolean, default=False)
    owner_id = Column(String, nullable=False) 