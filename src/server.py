import logging

import telebot
from telebot.handler_backends import ContinueHandling

from confing import ServerSettings

logger = logging.getLogger("TeleBot")


class Server(telebot.TeleBot):
    def __init__(self, settings: ServerSettings):
        super().__init__(settings.BOT_TOKEN)

    def _run_middlewares_and_handler(self, message, handlers, middlewares, update_type):
        result = None
        if self.use_class_middlewares:
            raise NotImplementedError("Middlewares not supported yet")

        if handlers:
            for handler in handlers:
                if self._test_message_handler(handler, message):
                    if handler.get("pass_bot", False):
                        result = handler["function"](message, bot=self)
                    else:
                        result = handler["function"](message)

                    if not isinstance(result, ContinueHandling):
                        break

        if result is not None:
            self.reply_to(message, str(result))
