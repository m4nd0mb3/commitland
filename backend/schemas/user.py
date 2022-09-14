from typing import Any, Optional, List
from pydantic import BaseModel, EmailStr


class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    genre: Any
    phone: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaUp(UserSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]


class AccountSchemaCreate(BaseModel):
    kind_of_account: Any
    token: str

    class Config:
        orm_mode = True

