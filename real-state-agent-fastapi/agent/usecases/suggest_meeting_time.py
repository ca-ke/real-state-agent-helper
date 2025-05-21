from datetime import datetime
from typing import Dict, Any
from core.repositories.llm_repository import LLMRepository

class SuggestMeetingTimeUseCase:
    def __init__(self, llm_repository: LLMRepository):
        self.llm_repository = llm_repository

    async def execute(self, property_details: Dict[str, Any], current_time: str) -> Dict[str, Any]:
        prompt = f"""
        As a real estate scheduling assistant, analyze the following situation and suggest a suitable time for a call between two real estate agents:

        Current time: {current_time}
        Property details:
        - Title: {property_details['title']}
        - Location: {property_details['location']}
        - Price: ${property_details['price']}
        - Bedrooms: {property_details['bedrooms']}

        Please suggest a suitable time for a call between the agents, considering:
        1. Business hours (9 AM to 6 PM)
        2. A 30-minute duration
        3. At least 1 hour from now
        4. Weekdays only

        Respond in JSON format with:
        {{
            "suggested_time": "YYYY-MM-DD HH:MM",
            "reasoning": "Brief explanation of why this time was chosen"
        }}
        """
        suggestion = await self.llm_repository.get_completion(prompt, response_format={"type": "json_object"})
        suggested_time = datetime.strptime(suggestion["suggested_time"], "%Y-%m-%d %H:%M")
        
        return {
            "suggested_time": suggested_time.strftime("%A, %B %d at %I:%M %p"),
            "reasoning": suggestion["reasoning"]
        } 