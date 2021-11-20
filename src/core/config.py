import os
import secrets
from typing import Optional
from functools import lru_cache

from pydantic import BaseSettings, validator, Field


class Settings(BaseSettings):
    LEVEL: str = 'DEVELOP'
    PROJECT_TITLE: str = 'FastAPI with Sentry'
    COMMON_API: str = '/api'
    ALGORITHM: str
    SECRET_KEY: Optional[str]
    
    @validator('SECRET_KEY', pre=True)
    def parsing_secret_key(cls, value: str) -> Optional[str]:
        if value:
            return value
        else:
            os.environ['SECRET_KEY'] = secrets.token_urlsafe(32)
    
    class Config:
        env_file = '.env'
        
        
class DevelopSettings(Settings):
    DB_URL: str = Field(env='DEVELOP_DB_URL')
    SENTRY_DSN: str = Field(env='DEVELOP_SENTRY_DSN')
        

class ProductSettings(Settings):
    DB_URL: str = Field(env='PRODUCT_DB_URL')
    SENTRY_DSN: str = Field(env='PRODUCT_SENTRY_DSN')
        
        
@lru_cache
def get_settings():
    return DevelopSettings() if Settings().LEVEL == 'DEVELOP' \
        else ProductSettings()