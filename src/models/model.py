from pydantic import BaseModel, ConfigDict


class MessageModel(BaseModel):
    first_name: str
    text: str
    model_config = ConfigDict(from_attributes=True)


class UserModel(BaseModel):
    user_id: int
    username: str
    is_premium: bool | None
    model_config = ConfigDict(from_attributes=True)


class AddMessageModel(BaseModel):
    id: int
    chat_id: int
    date: int
    user_id: int
    text: str


class AddUserModel(BaseModel):
    user_id: int
    first_name: str
    last_name: str | None
    username: str | None
    is_premium: bool | None


class ChatModel(BaseModel):
    id: int
