from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative
class Base:
    id: int = Column('id', Integer, primary_key=True, autoincrement=True)
    created_at: datetime = Column(
        'created_at',
        DateTime(timezone=True),
        default=func.now()
    )
    updated_at: datetime = Column('updated_at', DateTime(timezone=True))
    deleted_at: datetime = Column('deleted_at', DateTime(timezone=True))
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
        
    