from typing import List, Optional
from datetime import time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from real_state_agent.models import RealEstateAgent, AgentSchedule, Place

class RealEstateAgentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_agent(self, user_id: int, name: str, email: str, place_id: int) -> RealEstateAgent:
        agent = RealEstateAgent(
            user_id=user_id,
            name=name,
            email=email,
            place_id=place_id
        )
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        return agent

    async def get_agent_by_user_id(self, user_id: int) -> Optional[RealEstateAgent]:
        query = select(RealEstateAgent).where(RealEstateAgent.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_schedule(
        self, 
        agent_id: int, 
        day_of_week: int, 
        start_time: str, 
        end_time: str
    ) -> AgentSchedule:
        start_time_obj = time.fromisoformat(start_time)
        end_time_obj = time.fromisoformat(end_time)
        
        schedule = AgentSchedule(
            agent_id=agent_id,
            day_of_week=day_of_week,
            start_time=start_time_obj,
            end_time=end_time_obj
        )
        self.db.add(schedule)
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule

    async def get_agent_schedules(self, agent_id: int) -> List[AgentSchedule]:
        query = select(AgentSchedule).where(AgentSchedule.agent_id == agent_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_place(self, city: str, state: str, country: str) -> Place:
        place = Place(
            city=city,
            state=state,
            country=country
        )
        self.db.add(place)
        await self.db.commit()
        await self.db.refresh(place)
        return place

    async def get_place_by_id(self, place_id: int) -> Optional[Place]:
        query = select(Place).where(Place.id == place_id)
        result = await self.db.execute(query)
        return result.scalars().first() 