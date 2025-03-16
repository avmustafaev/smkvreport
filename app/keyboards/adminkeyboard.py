from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Inline-клавиатура для админа
def get_admin_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Вывести список пользователей", callback_data="list_users"),
        InlineKeyboardButton(text="Изменить роль пользователю", callback_data="change_role"),
        InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user"),
    )
    keyboard.adjust(1)  # По одной кнопке в строке
    return keyboard.as_markup()

# Inline-клавиатура для выбора ролей
def get_role_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Назначить роль dr", callback_data="set_role_dr"),
        InlineKeyboardButton(text="Назначить роль do", callback_data="set_role_do"),
        InlineKeyboardButton(text="Назначить роль user", callback_data="set_role_user"),
    )
    keyboard.adjust(1)  # По одной кнопке в строке
    return keyboard.as_markup()