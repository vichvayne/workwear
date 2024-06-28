from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Создание объекта FastAPI
app = FastAPI()

# Настройка базы данных MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://isp_p_Kruglov:12345/isp_p_Kruglov"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели SQLAlchemy для пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)  # Указываем длину для VARCHAR
    email = Column(String(100), unique=True, index=True)  # Указываем длину для VARCHAR
class Workwear(Base):
    __tablename__ = "Workwears"

    id_workwear = Column(Integer, primary_key=True, index=True)
    type_workwear = Column(String(50), index=True)  # Указываем длину для VARCHAR
    wear_period = Column(String(35), unique=True, index=True)  # Указываем длину для VARCHAR
    cost = Column(String(35), unique=True, index=True) 
class Workshop(Base):
    __tablename__ = "Workshops"

    id_workshop = Column(Integer, primary_key=True, index=True)
    type_workshop = Column(String(50), index=True)  # Указываем длину для VARCHAR
    FIO_chief = Column(String(35), unique=True, index=True)  # Указываем длину для VARCHAR
class Worker(Base):
    __tablename__ = "Workers"

    id_worker = Column(Integer, primary_key=True, index=True)
    FIO_worker = Column(String(50), index=True)  # Указываем длину для VARCHAR
    dolzhnost = Column(String(35), unique=True, index=True)  # Указываем длину для VARCHAR
    discount = Column(String(35), unique=True, index=True)  # Указываем длину для VARCHAR
class Receiving(Base):
    __tablename__ = "Receving"

    id_worker = Column(Integer, primary_key=True, index=True)
    id_workwear = Column(Integer, primary_key=True, index=True)
    DATE = Column(String(35), unique=True, index=True)  # Указываем длину для VARCHAR
    paiting = Column(String(30), unique=True, index=True)  # Указываем длину для VARCHAR
# Создание таблиц в базе данных
# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Определение Pydantic модели для пользователя
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class WorkwearCreate(BaseModel):
    id_workwaer: int
    type_wokwaer: str

    period: str

class WorkwaerResponse(BaseModel):
   
    cost: str
   
class WorkshopCreate(BaseModel):
   
    FIO_chief: str

    

class WorkwaerResponse(BaseModel):
   
    id_workshop: int
    type_workshop: str

class ReceivingCreate(BaseModel):
   
    painting: str

    

class ReceivingResponse(BaseModel):
   
    id_worker: int
    FIO_worker: str
    









    class Config:
        orm_mode = True

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Маршрут для получения пользователя по ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Маршрут для создания нового пользователя
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
