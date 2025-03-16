from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.database import get_user, get_all_users, update_user_role, delete_user
from app.keyboards.adminkeyboard import get_admin_keyboard, get_role_keyboard

# Создаём роутер
router = Router()

# Состояния для FSM (Finite State Machine)
class RoleChangeStates(StatesGroup):
    waiting_for_chat_id = State()
    waiting_for_role = State()

class DeleteUserStates(StatesGroup):
    waiting_for_chat_id = State()

# Обработчик команды /admin
@router.message(Command("admin"))
async def admin_command(message: types.Message):
    user = get_user(message.chat.id)
    if user and user.role == "superadmin":
        await message.answer(
            "Панель администратора:",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(f"Извините, {user.first_name}, вы не являетесь админом.")

# Обработчик кнопки "Вывести список пользователей"
@router.callback_query(F.data == "list_users")
async def list_users(callback: types.CallbackQuery):
    # Получаем всех пользователей из базы данных
    users = get_all_users()
    
    if users:
        # Формируем сообщение со списком пользователей
        users_list = "Список пользователей:\n\n"
        for user in users:
            users_list += (
                f"ID: {user.chat_id}\n"
                f"Имя: {user.first_name} {user.last_name}\n"
                f"Телефон: {user.phone_number}\n"
                f"Роль: {user.role}\n\n"
            )
        await callback.message.answer(users_list)
    else:
        await callback.message.answer("Пользователи не найдены.")

    # Подтверждаем обработку callback
    await callback.answer()

# Обработчик кнопки "Изменить роль пользователю"
@router.callback_query(F.data == "change_role")
async def change_role(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите chat_id пользователя, которому хотите изменить роль:")
    await state.set_state(RoleChangeStates.waiting_for_chat_id)
    await callback.answer()

# Обработчик ввода chat_id для изменения роли
@router.message(RoleChangeStates.waiting_for_chat_id)
async def process_chat_id(message: types.Message, state: FSMContext):
    try:
        chat_id = int(message.text)  # Преобразуем введённый текст в число
    except ValueError:
        await message.answer("Ошибка: chat_id должен быть числом. Попробуйте ещё раз.")
        return

    # Проверяем, существует ли пользователь с таким chat_id
    user = get_user(chat_id)
    if not user:
        await message.answer(f"Пользователь с chat_id {chat_id} не найден.")
        await state.clear()
        return

    # Сохраняем chat_id в состоянии
    await state.update_data(chat_id=chat_id)

    # Отправляем inline-клавиатуру с выбором ролей
    await message.answer(
        f"Пользователь найден: {user.first_name} {user.last_name}.\n"
        "Выберите новую роль:",
        reply_markup=get_role_keyboard()
    )
    await state.set_state(RoleChangeStates.waiting_for_role)

# Обработчик выбора роли
@router.callback_query(RoleChangeStates.waiting_for_role, F.data.startswith("set_role_"))
async def set_role(callback: types.CallbackQuery, state: FSMContext):
    # Получаем выбранную роль из callback_data
    role = callback.data.replace("set_role_", "")

    # Получаем chat_id из состояния
    data = await state.get_data()
    chat_id = data.get("chat_id")

    # Обновляем роль пользователя в базе данных
    update_user_role(chat_id, role)

    # Отправляем сообщение об успешном изменении роли
    await callback.message.answer(f"Роль пользователя с chat_id {chat_id} изменена на {role}.")
    await state.clear()
    await callback.answer()

# Обработчик кнопки "Удалить пользователя"
@router.callback_query(F.data == "delete_user")
async def delete_user_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите chat_id пользователя, которого хотите удалить:")
    await state.set_state(DeleteUserStates.waiting_for_chat_id)
    await callback.answer()

# Обработчик ввода chat_id для удаления пользователя
@router.message(DeleteUserStates.waiting_for_chat_id)
async def process_delete_chat_id(message: types.Message, state: FSMContext):
    try:
        chat_id = int(message.text)  # Преобразуем введённый текст в число
    except ValueError:
        await message.answer("Ошибка: chat_id должен быть числом. Попробуйте ещё раз.")
        return

    # Проверяем, существует ли пользователь с таким chat_id
    user = get_user(chat_id)
    if not user:
        await message.answer(f"Пользователь с chat_id {chat_id} не найден.")
        await state.clear()
        return

    # Удаляем пользователя из базы данных
    delete_user(chat_id)

    # Отправляем сообщение об успешном удалении
    await message.answer(f"Пользователь с chat_id {chat_id} удалён.")
    await state.clear()