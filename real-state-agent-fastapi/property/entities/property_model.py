from sqlalchemy import Column, String, Float, Integer, Boolean
from sqlalchemy.types import UserDefinedType
from core.database import Base

class Vector(UserDefinedType):
    def get_col_spec(self, _):
        return "vector"

    def bind_processor(self, _):
        def process(value):
            if value is None:
                return None
            return f"[{','.join(map(str, value))}]"
        return process

    def result_processor(self, _, __):
        def process(value):
            if value is None:
                return None
            if isinstance(value, str):
                return [float(x) for x in value.strip('[]').split(',')]
            return value
        return process

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
    embedding = Column(Vector, nullable=True) 