from sqlalchemy.orm import Session
from .models import SessionLocal, User

# Контекстный менеджер для работы с сессиями
from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Добавление нового пользователя
def add_user(chat_id: int, phone_number: str, first_name: str, last_name: str, role: str = "user"):
    with get_db() as db:
        user = User(chat_id=chat_id, phone_number=phone_number, first_name=first_name, last_name=last_name, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)

# Получение информации о пользователе по chat_id
def get_user(chat_id: int) -> User:
    with get_db() as db:
        user = db.query(User).filter(User.chat_id == chat_id).first()
        return user

def get_all_users():
    with get_db() as db:
        users = db.query(User).filter(User.role != "ban").all()  # Исключаем забаненных
        return users

# Обновление роли пользователя
def update_user_role(chat_id: int, role: str):
    with get_db() as db:
        user = db.query(User).filter(User.chat_id == chat_id).first()
        if user:
            user.role = role
            db.commit()
            db.refresh(user)

# Удаление пользователя
def delete_user(chat_id: int):
    with get_db() as db:
        user = db.query(User).filter(User.chat_id == chat_id).first()
        if user:
            db.delete(user)
            db.commit()


def get_banned_users():
    with get_db() as db:
        users = db.query(User).filter(User.role == "ban").all()
        return users