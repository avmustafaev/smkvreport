import os
from dotenv import load_dotenv

class LoadEnv:
    def __init__(self):
        load_dotenv()

    def get_bot_token(self):
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            raise ValueError("Токен бота не найден в переменных окружения.")
        return bot_token

    def get_superadmin_chat_id(self):
        superadmin_chat_id = os.getenv('SUPERADMIN_CHAT_ID')
        if not superadmin_chat_id:
            raise ValueError("Chat ID супер-админа не найден в переменных окружения.")
        return int(superadmin_chat_id)