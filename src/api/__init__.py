from fastapi import APIRouter

from src.api import user

router = APIRouter()


router.include_router(
    router = user.router,
    prefix = '/user',
    tags = ['User']
)