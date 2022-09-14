from pydantic import EmailStr
from pytz import timezone
from typing import Optional,List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.user import UserModel
from core.configs import settings
from core.security import verify_password
from schemas.user import UserSchemaBase



oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login"
)


async def authentication(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserSchemaBase]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        usuario: UserSchemaBase = result.scalars().unique().one_or_none()
        
        if not usuario:
            return None
        
        if not verify_password(password, usuario.password):
            return None
        
        return usuario
    
def _create_token(token_type: str, time_to_live: timedelta, sub: str) -> str:
    payload = {} #https://datatrucker.ietf.org/doc/html/rfc7519#section-4.1.3
    luanda = timezone('Africa/Luanda')
    expire = datetime.now(tz=luanda) + time_to_live
    
    payload['type'] = token_type
    payload['exp'] = expire
    payload['iat'] = datetime.now(tz=luanda)
    payload['sub']: str = sub
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_access(sub: str) -> str:
    """
    https://jwt.io
    """
    return _create_token(
        token_type='access_token',
        time_to_live=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    ) 