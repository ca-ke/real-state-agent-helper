from datetime import datetime
from typing import Dict, Any
from core.exceptions import InvalidRequestError
from agent.repositories.matching_repository import MatchingRepository
from agent.usecases.suggest_meeting_time import SuggestMeetingTimeUseCase
from agent.models import CallRequest


class ScheduleCallWithAnotherRealStateAgent:
    def __init__(
        self,
        matching_repository: MatchingRepository,
        suggest_meeting_time_uc: SuggestMeetingTimeUseCase,
    ):
        self.matching_repository = matching_repository
        self.suggest_meeting_time_uc = suggest_meeting_time_uc

    async def execute(self, request: CallRequest, current_user_id: int) -> Dict[str, Any]:
        try:
            matched_properties = await self.matching_repository.match_property(request.query)
            
            if not matched_properties:
                return {
                    "message": "No properties found matching your requirements",
                    "matched_property_id": "",
                    "owner_id": ""
                }

            # Get the best match
            property = matched_properties[0]

            if property["owner_id"] == current_user_id:
                return {
                    "message": "This property is yours. No need to schedule a call with yourself",
                    "matched_property_id": property["id"],
                    "owner_id": property["owner_id"]
                }

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            suggestion = await self.suggest_meeting_time_uc.execute(property, current_time)

            response = {
                "message": f"I suggest scheduling a call for {suggestion['suggested_time']}. {suggestion['reasoning']}",
                "matched_property_id": property["id"],
                "owner_id": property["owner_id"],
                "property": {
                    "id": property["id"],
                    "title": property["title"],
                    "location": property["location"],
                    "price": property["price"],
                    "bedrooms": property["bedrooms"],
                },
            }

            return response

        except Exception as e:
            raise InvalidRequestError(f"Failed to schedule call: {str(e)}")
