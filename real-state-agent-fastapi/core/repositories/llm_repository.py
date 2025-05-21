from litellm import completion
from core.settings import Settings
import json
from typing import Dict, Any

class LLMRepository:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def get_completion(self, prompt: str, response_format: Dict[str, str] = None) -> Dict[str, Any]:
        response = completion(
            api_key=self.settings.llm_api_key,
            response_format=response_format or { "type": "json_object" },
            base_url=self.settings.llm_base_url,
            model=self.settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.settings.llm_temperature
        )

        return json.loads(response.choices[0].message.content)