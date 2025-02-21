from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from src.db.model import Base, Message, User
from src.models.model import (AddMessageModel, AddUserModel, MessageModel,
                              UserModel)


class AbstractRepositoryMessage(ABC):
    @abstractmethod
    def save_message(self, msg: AddMessageModel) -> None: ...

    @abstractmethod
    def get_history(self, chat_id: int, limit: int) -> [MessageModel]: ...


class AbstractRepositoryUser(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserModel: ...

    @abstractmethod
    def save_user(self, user: AddUserModel) -> None: ...


class MessageRepository(AbstractRepositoryMessage):

    def __init__(self, engine: Engine, session_maker: sessionmaker):
        self.session_maker = session_maker
        Base.metadata.create_all(engine)

    def save_message(self, msg: AddMessageModel) -> None:
        with self.session_maker() as session:
            session.add(Message(**msg.model_dump()))
            session.commit()

    def get_history(self, chat_id: int, limit: int) -> [MessageModel]:
        with self.session_maker() as session:
            query = (
                select(User.first_name, Message.text)
                .select_from(Message)
                .join(User, User.user_id == Message.user_id)
                .where(Message.chat_id.is_(chat_id))
                .order_by(Message.date)
                .limit(limit)
            )

            result = session.execute(query)
            result = result.mappings().all()
            return [MessageModel.model_validate(i) for i in result]


class UserRepository(AbstractRepositoryUser):

    def __init__(self, engine: Engine, session_maker: sessionmaker):
        self.session_maker = session_maker
        Base.metadata.create_all(engine)

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        with self.session_maker() as session:
            query = select(User).where(User.user_id.is_(user_id))
            user = session.execute(query)
            user = user.scalars().one_or_none()
            return UserModel.model_validate(user) if user else user

    def save_user(self, user: AddUserModel) -> None:
        with self.session_maker() as session:
            session.add(User(**user.model_dump()))
            session.commit()
