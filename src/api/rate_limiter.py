from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
import time

import telebot

from confing import RateLimiterSettings

minutes = int
seconds = float


class RateLimiterError(Exception):
    pass


@dataclass
class ChatRequest:
    request_time: time = field(default_factory=time.time)


class RateLimiter(ABC):
    def __init__(
            self,
            settings: RateLimiterSettings
    ):
        self._requests_per_interval = settings.requests_per_interval
        self._interval = settings.interval
        self._minimal_delay = settings.minimal_delay
        self._last_request_time = 0

    def check_limit(self, message: telebot.types.Message):
        self._check_too_fast_requests(message)
        self._update_limits(message.chat.id)
        self._register_request(message)

    @abstractmethod
    def _update_limits(self, chat_id: int):
        raise NotImplementedError

    @abstractmethod
    def _register_request(self, message: telebot.types.Message):
        raise NotImplementedError

    def _check_too_fast_requests(self, message: telebot.types.Message):
        current_time = time.time()
        if current_time - self._last_request_time < self._minimal_delay:
            raise RateLimiterError(f"Too fast requests for chat: {message.chat.title} "
                                   f"(id {message.chat.id})")
        self._last_request_time = current_time


class ChatRateLimiter(RateLimiter):
    def __init__(
            self,
            settings: RateLimiterSettings
    ):
        super().__init__(settings=settings)
        self._chat_storage: defaultdict[int: list[ChatRequest]] = defaultdict(list)

    def _register_request(self, message: telebot.types.Message):
        requests_queue = self._chat_storage[message.chat.id]

        if self._requests_per_interval <= len(requests_queue):
            raise RateLimiterError(f"Too many requests for chat {message.chat.title} "
                                   f"(id {message.chat.id})")

        self._chat_storage[message.chat.id].append(ChatRequest())

    def _update_limits(self, chat_id: int):
        current_time = time.time()
        self._chat_storage[chat_id] = [
            request
            for request in self._chat_storage[chat_id]
            if (current_time - request.request_time) // 60 < self._interval
        ]
