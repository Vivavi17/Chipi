from src.context.service import AbstractContext
from src.db.repository import AbstractRepositoryMessage, AbstractRepositoryUser
from src.models.model import AddMessageModel, AddUserModel, ChatModel


class BotService:

    def __init__(
        self,
        message_repository: AbstractRepositoryMessage,
        user_repository: AbstractRepositoryUser,
        service_context: AbstractContext,
    ) -> None:
        self.message_repository = message_repository
        self.user_repository = user_repository
        self.service_context = service_context

    def save_message(self, user: AddUserModel, message: AddMessageModel) -> None:
        if not self.user_repository.get_user_by_id(user.user_id):
            self.user_repository.save_user(user)
        self.message_repository.save_message(message)

    def save_sticker(self, user: AddUserModel, message: AddMessageModel) -> None:
        if not self.user_repository.get_user_by_id(user.user_id):
            self.user_repository.save_user(user)
        self.message_repository.save_message(message)

    def get_context(self, chat: ChatModel) -> str:
        text = self.message_repository.get_history(chat.id, 100)
        text = "\n".join([f"{i.first_name}: {i.text}" for i in text])
        return self.service_context.get_context(text)
