from abc import ABC, abstractmethod

from openai import APIError, OpenAI

from confing import LLMSettings


class AbstractContext(ABC):
    def get_context(self, text: str) -> str:
        try:
            result = self._send_request(text=text)
        except APIError:
            result = f"Я умер, оживу чуть позже ☠️️"
        return result

    @abstractmethod
    def _send_request(self, text: str) -> str: ...


class OpenAIContext(AbstractContext):
    def __init__(self, client_api: OpenAI, settings: LLMSettings):
        self.client = client_api
        self.settings = settings

    def _send_request(self, text: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.settings.AI_MODEL,
            messages=[{"role": "user", "content": self.settings.PROMPT + text}],
        )
        result = completion.choices[0].message.content
        return result
