import telebot.types
from telebot import TeleBot

from src.models.model import AddMessageModel, AddUserModel, ChatModel
from src.service.botservice import BotService


class BotController:
    def __init__(self, bot: TeleBot, service: BotService) -> None:
        self.bot = bot
        self.service = service

        @bot.message_handler(chat_types=["supergroup", "group"], commands=["context"])
        def get_context(message: telebot.types.Message) -> str:
            chat = ChatModel(id=message.chat.id)
            text = self.service.get_context(chat)
            return text

        @bot.message_handler(
            chat_types=["supergroup", "group"],
            func=lambda message: message.text is not None,
        )
        def save_message(message: telebot.types.Message) -> None:
            user = AddUserModel(
                user_id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                is_premium=message.from_user.is_premium,
            )
            msg = AddMessageModel(
                id=message.id,
                chat_id=message.chat.id,
                date=message.date,
                user_id=message.from_user.id,
                text=message.text,
            )
            self.service.save_message(user, msg)

        @bot.message_handler(
            chat_types=["supergroup", "group"],
            content_types=["sticker"],
            func=lambda message: message.sticker.emoji is not None,
        )
        def save_sticker(message: telebot.types.Message) -> None:
            user = AddUserModel(
                user_id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                is_premium=message.from_user.is_premium,
            )
            msg = AddMessageModel(
                id=message.id,
                chat_id=message.chat.id,
                date=message.date,
                user_id=message.from_user.id,
                text=message.sticker.emoji,
            )
            self.service.save_sticker(user, msg)
