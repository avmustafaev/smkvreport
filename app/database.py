from contextlib import contextmanager
from sqlalchemy.orm import Session
from .models import SessionLocal, User

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Добавление нового пользователя
def add_user(
    chat_id: int, phone_number: str, first_name: str, last_name: str, role: str = "user"
):
    with get_db() as db:
        user = User(
            chat_id=chat_id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

# Получение информации о пользователе по chat_id
def get_user(chat_id: int) -> User:
    with get_db() as db:
        return db.query(User).filter(User.chat_id == chat_id).first()

def get_all_users():
    with get_db() as db:
        return db.query(User).filter(User.role != "ban").all()


# Обновление роли пользователя
def update_user_role(chat_id: int, role: str):
    with get_db() as db:
        if user := db.query(User).filter(User.chat_id == chat_id).first():
            user.role = role
            db.commit()
            db.refresh(user)

# Удаление пользователя
def delete_user(chat_id: int):
    with get_db() as db:
        if user := db.query(User).filter(User.chat_id == chat_id).first():
            db.delete(user)
            db.commit()


def get_banned_users():
    with get_db() as db:
        return db.query(User).filter(User.role == "ban").all()
