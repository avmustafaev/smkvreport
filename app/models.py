from sqlalchemy import create_engine, Column, BigInteger, String  # Изменяем Integer на BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка базы данных (PostgreSQL)
DATABASE_URL = "postgresql://user:password@db:5432/telegram_bot_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    chat_id = Column(BigInteger, primary_key=True)  # Изменяем Integer на BigInteger
    phone_number = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(String, default="user")

# Создание таблиц в базе данных
def init_db():
    Base.metadata.create_all(bind=engine)