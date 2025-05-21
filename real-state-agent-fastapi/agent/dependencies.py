from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from agent.usecases import ScheduleCallWithAnotherRealStateAgent, SuggestMeetingTimeUseCase
from agent.repositories import MatchingRepository
from core.dependencies import get_db_session, get_llm_repository     

def get_matching_repository(
    db: AsyncSession = Depends(get_db_session)
) -> MatchingRepository:
    return MatchingRepository(db)

def get_suggest_meeting_time_uc(
    llm_repository = Depends(get_llm_repository)
) -> SuggestMeetingTimeUseCase:
    return SuggestMeetingTimeUseCase(llm_repository)

def get_schedule_call_uc(
    matcher: MatchingRepository = Depends(get_matching_repository),
    suggest_meeting_time_uc = Depends(get_suggest_meeting_time_uc)
) -> ScheduleCallWithAnotherRealStateAgent:
    return ScheduleCallWithAnotherRealStateAgent(matcher, suggest_meeting_time_uc)