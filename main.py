from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from confing import Settings
from src.api.botcontroller import BotController
from src.context.model import OpenAIClient
from src.context.service import OpenAIContext
from src.db.repository import MessageRepository, UserRepository
from src.server import Server
from src.service.botservice import BotService

if __name__ == "__main__":
    settings = Settings()

    engine = create_engine(f"sqlite://{settings.DB.DB_PATH}")
    session_maker = sessionmaker(engine, expire_on_commit=False)

    bot = Server(settings.SERVER)

    client = OpenAIClient(settings.OPENAI)

    service = BotService(
        MessageRepository(engine, session_maker),
        UserRepository(engine, session_maker),
        OpenAIContext(client, settings.LLM),
    )
    controller = BotController(bot, service)

    bot.infinity_polling()
