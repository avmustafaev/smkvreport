import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.loadenv import LoadEnv
from app.handlers.registeruser import router as register_router
from app.handlers.superadmin import router as admin_router  # Импортируем новый роутер

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

# Подключаем роутеры
dp.include_router(register_router)
dp.include_router(admin_router)  # Подключаем роутер для админа

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())