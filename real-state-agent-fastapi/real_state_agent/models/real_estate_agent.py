from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from core.database import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    agents = relationship("RealEstateAgent", back_populates="place")


class RealEstateAgent(Base):
    __tablename__ = "real_estate_agents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    place = relationship("Place", back_populates="agents")
    schedules = relationship("AgentSchedule", back_populates="agent")
    ratings = relationship("AgentRating", back_populates="agent")


class AgentSchedule(Base):
    __tablename__ = "agent_schedules"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("real_estate_agents.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    agent = relationship("RealEstateAgent", back_populates="schedules")


class AgentRating(Base):
    __tablename__ = "agent_ratings"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("real_estate_agents.id"), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    agent = relationship("RealEstateAgent", back_populates="ratings")
