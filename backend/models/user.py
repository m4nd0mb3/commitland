from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings
import enum


class GenreEnum(enum.Enum):
    male = 1
    female = 2

class AccountEnum(enum.Enum):
    gitlab = 1


class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=False)
    sobrenome = Column(String(256), nullable=False)
    genre = Column(Enum(GenreEnum), nullable=False)
    email = Column(String(256), index=True, nullable=False, unique=True)
    phone = Column(String(256), index=True, nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)

    # events = relationship("events", back_populates="owner")


class AccountModel(settings.DBBaseModel):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kind_of_account = Column(Enum(AccountEnum), nullable=False)
    token = Column(String(256), nullable=False)
    saved_by_id = Column(Integer, ForeignKey('users.id'))
    # events = relationship("events", back_populates="owner")