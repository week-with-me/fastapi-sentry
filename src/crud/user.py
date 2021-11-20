import bcrypt

from jose import jwt
from email_validator import validate_email

from src.model import User
from src.crud import CRUDBase
from src.schema import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, obj_in: UserCreate) -> None:
        validate_email(obj_in.email)
        encode_password = bcrypt.hashpw(
            obj_in.password.encode('utf-8'), bcrypt.gensalt()
        )
        obj_in.password = encode_password.decode('utf-8')
        return await super().create(obj_in)
        
        
user_crud = CRUDUser(User)