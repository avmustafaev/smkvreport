import os
from dotenv import load_dotenv

class LoadEnv:
    def __init__(self):
        load_dotenv()

    def get_bot_token(self):
        if bot_token := os.getenv("BOT_TOKEN"):
            return bot_token
        else:
            raise ValueError("Токен бота не найден в переменных окружения.")

    def get_superadmin_chat_id(self):
        if superadmin_chat_id := os.getenv("SUPERADMIN_CHAT_ID"):
            return int(superadmin_chat_id)
        else:
            raise ValueError("Chat ID супер-админа не найден в переменных окружения.")
