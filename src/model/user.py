from pydantic import EmailStr
from sqlalchemy import Column, String
from sqlalchemy.orm import relation

from src.database import Base

class User(Base):
    nickname: str = Column('nickname', String(length=8), unique=True, nullable=False)
    email: EmailStr = Column('email', String(length=32), unique=True, nullable=False)
    password: str = Column('password', String(64), nullable=False)
    
    posts = relation('Post', back_populates='user')