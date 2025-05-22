from fastapi import APIRouter, Depends
from agent.models import CallRequest, CallResponse
from shared.session.user_identity import get_user_from_token
from agent.dependencies import get_schedule_call_uc

router = APIRouter()

@router.post("/schedule-call", response_model=CallResponse)
async def schedule_call(
    body: CallRequest,
    user = Depends(get_user_from_token),
    uc = Depends(get_schedule_call_uc)
):
    return await uc.execute(body, user["user_id"])