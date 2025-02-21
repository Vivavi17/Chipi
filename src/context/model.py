from openai import OpenAI

from confing import OpenAISettings


class OpenAIClient(OpenAI):
    def __init__(self, settings: OpenAISettings):
        super().__init__(base_url=settings.AI_URL, api_key=settings.API_KEY)
