from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from uuid import UUID
from shared.session.user_identity import get_user_from_token
from real_state_agent.usecases.manage_agent_schedule import ManageAgentScheduleUseCase
from real_state_agent.dependencies import get_manage_schedule_use_case
from real_state_agent.models import ScheduleCreateRequest, ScheduleResponse

router = APIRouter(
    prefix="/real-estate-agent",
    tags=["real-estate-agent"]
)

@router.post("/schedule", response_model=ScheduleResponse)
async def create_schedule(
    schedule: ScheduleCreateRequest,
    current_user: Dict[str, Any] = Depends(get_user_from_token),
    use_case: ManageAgentScheduleUseCase = Depends(get_manage_schedule_use_case)
):
    try:
        return await use_case.create_schedule(
            user_id=UUID(current_user["user_id"]),
            day_of_week=schedule.day_of_week,
            start_time=schedule.start_time,
            end_time=schedule.end_time
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/schedule", response_model=List[ScheduleResponse])
async def get_schedules(
    current_user: Dict[str, Any] = Depends(get_user_from_token),
    use_case: ManageAgentScheduleUseCase = Depends(get_manage_schedule_use_case)
):
    try:
        return await use_case.get_agent_schedules(UUID(current_user["user_id"]))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 