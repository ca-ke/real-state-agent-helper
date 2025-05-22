from pydantic import BaseModel, Field
from typing import List


class ScheduleCreateRequest(BaseModel):
    day_of_week: int = Field(
        ..., ge=0, le=6, description="Day of week (0-6, Monday-Sunday)"
    )
    start_time: str = Field(
        ...,
        pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$",
        description="Start time in HH:MM:SS format",
    )
    end_time: str = Field(
        ...,
        pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$",
        description="End time in HH:MM:SS format",
    )


class ScheduleResponse(BaseModel):
    id: int
    day_of_week: int
    start_time: str
    end_time: str

    class Config:
        from_attributes = True


class ScheduleListResponse(BaseModel):
    schedules: List[ScheduleResponse]
