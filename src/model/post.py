from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relation

from src.database import Base


class Post(Base):
    title: str = Column('title', String(length=16), nullable=False)
    content: str = Column('content', String(length=512), nullable=False)
    user_id: int = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    
    user = relation('User', back_populates='posts')