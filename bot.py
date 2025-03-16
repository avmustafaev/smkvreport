import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.loadenv import LoadEnv
from app.handlers import router

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения
env = LoadEnv()
API_TOKEN = env.get_bot_token()

# Инициализация бота с DefaultBotProperties
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Инициализация хранилища и диспетчера
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключаем роутер
dp.include_router(router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())