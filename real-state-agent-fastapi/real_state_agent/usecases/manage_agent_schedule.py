from typing import List, Dict, Any
from datetime import time
from core.exceptions import InvalidRequestError
from real_state_agent.repositories import RealEstateAgentRepository

class ManageAgentScheduleUseCase:
    def __init__(self, agent_repository: RealEstateAgentRepository):
        self.agent_repository = agent_repository

    async def create_schedule(
        self,
        user_id: int,
        day_of_week: int,
        start_time: str,
        end_time: str
    ) -> Dict[str, Any]:
        if not 0 <= day_of_week <= 6:
            raise InvalidRequestError("Day of week must be between 0 (Monday) and 6 (Sunday)")

        try:
            start = time.fromisoformat(start_time)
            end = time.fromisoformat(end_time)
            if start >= end:
                raise InvalidRequestError("Start time must be before end time")
        except ValueError:
            raise InvalidRequestError("Invalid time format. Use HH:MM:SS format")

        agent = await self.agent_repository.get_agent_by_user_id(user_id)
        if not agent:
            raise InvalidRequestError("Real estate agent not found")

        schedule = await self.agent_repository.create_schedule(
            agent_id=agent.id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time
        )

        return {
            "id": schedule.id,
            "day_of_week": schedule.day_of_week,
            "start_time": schedule.start_time.isoformat(),
            "end_time": schedule.end_time.isoformat()
        }

    async def get_agent_schedules(self, user_id: int) -> List[Dict[str, Any]]:
        agent = await self.agent_repository.get_agent_by_user_id(user_id)
        if not agent:
            raise InvalidRequestError("Real estate agent not found")

        schedules = await self.agent_repository.get_agent_schedules(agent.id)
        
        return [{
            "id": schedule.id,
            "day_of_week": schedule.day_of_week,
            "start_time": schedule.start_time.isoformat(),
            "end_time": schedule.end_time.isoformat()
        } for schedule in schedules] 