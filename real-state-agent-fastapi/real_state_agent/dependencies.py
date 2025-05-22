from fastapi import Depends
from real_state_agent.repositories.real_estate_agent_repository import (
    RealEstateAgentRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import get_db_session
from real_state_agent.usecases.manage_agent_schedule import ManageAgentScheduleUseCase


def get_real_estate_agent_repository(
    db: AsyncSession = Depends(get_db_session),
) -> RealEstateAgentRepository:
    return RealEstateAgentRepository(db)


def get_manage_schedule_use_case(
    repository: RealEstateAgentRepository = Depends(get_real_estate_agent_repository),
) -> ManageAgentScheduleUseCase:
    return ManageAgentScheduleUseCase(repository)
