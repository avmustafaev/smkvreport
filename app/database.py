from sqlalchemy.orm import Session
from .models import SessionLocal, User

# Добавление нового пользователя
def add_user(chat_id: int, phone_number: str, first_name: str, last_name: str, role: str = "user"):
    db = SessionLocal()
    user = User(chat_id=chat_id, phone_number=phone_number, first_name=first_name, last_name=last_name, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

# Получение информации о пользователе по chat_id
def get_user(chat_id: int) -> User:
    db = SessionLocal()
    user = db.query(User).filter(User.chat_id == chat_id).first()
    db.close()
    return user