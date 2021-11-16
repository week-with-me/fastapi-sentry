from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    """
    """
    nickname: str
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            'example': {
                'nickaname': '',
                'email': '',
                'password': ''
            }
        }
    
    
class UserUpdate(UserBase):
    """
    """
    id: int
    nickname: str
    updated_at: datetime
    
    class Config:
        pass
    
    
class UserDelete(UserBase):
    """
    """
    id: int
    password: str
    deleted_at: datetime
    
    class Config:
        pass