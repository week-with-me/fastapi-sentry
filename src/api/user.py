from fastapi import APIRouter
import traceback
from starlette.responses import JSONResponse

from src.crud import user_crud
from src.schema import UserCreate

router = APIRouter()


@router.post('/sign-up')
async def sign_up(obj_in: UserCreate):
    try:
        user_crud.create(UserCreate)
        
        return JSONResponse()
    
    except:
        print(traceback.print_exc())