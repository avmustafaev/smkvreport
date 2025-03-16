from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Клавиатура для запроса номера телефона
def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Поделиться номером", request_contact=True)]
        ],
        resize_keyboard=True  # Клавиатура подстраивается под размер экрана
    )

# Функция для удаления клавиатуры
def remove_keyboard():
    return ReplyKeyboardRemove()