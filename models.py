from sqlalchemy import create_engine, Column, Integer, BigInteger, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Настройки подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"

# Создание базового класса для модели
Base = declarative_base()

# Определение модели Queue
class Queue(Base):
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=False)
    position = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создание таблиц (если они не существуют)
Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
