from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from app.database import add_user, get_user
from app.models import init_db
from app.keyboards.keyboards import get_phone_keyboard, remove_keyboard
from app.loadenv import LoadEnv

# Инициализация базы данных
init_db()

# Создаём роутер
router = Router()

# Состояния для FSM (Finite State Machine)
class RegistrationStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_first_name = State()
    waiting_for_last_name = State()

# Функция для удаления сообщения бота
async def delete_previous_message(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

# Обработчик команды /start
@router.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext, bot: Bot):
    if user := get_user(message.chat.id):
        # Если пользователь уже зарегистрирован
        await message.reply(
            f"С возвращением, {user.first_name} {user.last_name}!\n"
            f"Твой номер телефона: {user.phone_number}\n"
            f"Твоя роль: {user.role}"
        )
    else:
        # Если пользователь новый
        await message.answer("Привет! Давай познакомимся.")

        # Отправляем клавиатуру с кнопкой "Поделиться номером"
        sent_message = await message.answer("Пожалуйста, поделись своим номером телефона.", reply_markup=get_phone_keyboard())

        # Сохраняем ID сообщения бота
        await state.update_data(last_bot_message_id=sent_message.message_id)
        await state.set_state(RegistrationStates.waiting_for_phone)

# Обработчик получения номера телефона
@router.message(RegistrationStates.waiting_for_phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext, bot: Bot):
    # Удаляем предыдущее сообщение бота
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message_id")
    if last_bot_message_id:
        await delete_previous_message(bot, message.chat.id, last_bot_message_id)
    
    # Сохраняем номер телефона
    await state.update_data(phone_number=message.contact.phone_number)
    
    # Отправляем новое сообщение и сохраняем его ID
    sent_message = await message.answer("Спасибо! Теперь введи своё имя.", reply_markup=remove_keyboard())
    await state.update_data(last_bot_message_id=sent_message.message_id)
    await state.set_state(RegistrationStates.waiting_for_first_name)

# Обработчик получения имени
@router.message(RegistrationStates.waiting_for_first_name)
async def process_first_name(message: types.Message, state: FSMContext, bot: Bot):
    # Удаляем предыдущее сообщение бота
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message_id")
    if last_bot_message_id:
        await delete_previous_message(bot, message.chat.id, last_bot_message_id)
    
    # Сохраняем имя
    await state.update_data(first_name=message.text)
    
    # Отправляем новое сообщение и сохраняем его ID
    sent_message = await message.answer("Отлично! Теперь введи свою фамилию.")
    await state.update_data(last_bot_message_id=sent_message.message_id)
    await state.set_state(RegistrationStates.waiting_for_last_name)

# Обработчик получения фамилии
@router.message(RegistrationStates.waiting_for_last_name)
async def process_last_name(message: types.Message, state: FSMContext, bot: Bot):
    # Удаляем предыдущее сообщение бота
    data = await state.get_data()
    if last_bot_message_id := data.get("last_bot_message_id"):
        await delete_previous_message(bot, message.chat.id, last_bot_message_id)

    # Получаем данные из состояния
    phone_number = data.get("phone_number")
    first_name = data.get("first_name")
    last_name = message.text

    # Определяем роль пользователя
    env = LoadEnv()
    superadmin_chat_id = env.get_superadmin_chat_id()
    role = "superadmin" if message.chat.id == superadmin_chat_id else "user"

    # Сохраняем пользователя в базу данных
    add_user(message.chat.id, phone_number, first_name, last_name, role)

    # Отправляем финальное сообщение
    await message.answer(
        f"Спасибо, {first_name} {last_name}! Теперь ты зарегистрирован.\n"
        f"Твой номер телефона: {phone_number}\n"
        f"Твоя роль: {role}"
    )
    await state.clear()