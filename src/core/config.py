from functools import lru_cache

from pydantic import BaseSettings

COMMON_ENV_PATH = 'src/core/'


class Settings(BaseSettings):
    LEVEL: str = 'DEVELOP'
    PROJECT_TITLE: str = 'FastAPI with Sentry'
    COMMON_API: str = '/api'
    
    class Config:
        env_file = COMMON_ENV_PATH + '.env'
        
        
class DevelopSettings(Settings):
    DB_URL: str
    DSN: str
    
    class Config:
        env_file = COMMON_ENV_PATH + 'develop.env'
        

class ProductSettings(Settings):
    DB_URL: str
    DSN: str
    
    class Config:
        env_file = COMMON_ENV_PATH + 'product.env'
        
        
@lru_cache
def get_settings():
    return DevelopSettings() if Settings().LEVEL == 'DEVELOP' \
        else ProductSettings()