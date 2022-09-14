from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    #API_V2_STR: str = '/api/v2'
    DB_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/commitland'
    DBBaseModel = declarative_base()
    
    JWT_SECRET: str = '3TeAZKiXEGvG8cGwd7Mf7hUF5bFrxtM6GKQPipLX_os'
    """
    import secrets
    
    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True
        
settings: Settings = Settings()