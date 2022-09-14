import email
from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import sqlalchemy

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.user import AccountModel, UserModel, AccountEnum
from schemas.user import *
from core.deps import get_session, get_current_user
from core.security import password_generator
from core.auth import authentication, create_access


router = APIRouter()


# GET current user
@router.get('/current_user', response_model=UserSchemaBase)
def get_current_user(current_user: UserSchemaBase = Depends(get_current_user)):
    return current_user

# POST / Check Existenting Phone Number

@router.post('/checking_number/{phone_number}', status_code=status.HTTP_200_OK)
async def check_existing_user_number(phone_number: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.phone==phone_number)
        result = await session.execute(query)
        usuario: List[UserSchemaBase] = result.scalars().unique().one_or_none()
        
        if usuario is None:
            return Response(status_code=status.HTTP_200_OK)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Já existe um usuário com este número cadastrado.')
# POST / SignUp

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_usuario(usuario: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UserSchemaBase = UserModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        genre=usuario.genre,
        phone=usuario.phone,
        password=password_generator(usuario.password),
        is_admin=usuario.is_admin
    )

    async with db as session:
        try:
            db.add(novo_usuario)
            await db.commit()

            return novo_usuario
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um usuário com este email cadastrado.')
# POST / SignUp


@router.post('/set_new_account', status_code=status.HTTP_201_CREATED, response_model=AccountSchemaCreate)
async def set_new_account(account: AccountSchemaCreate, db: AsyncSession = Depends(get_session),
                       current_user: UserSchemaBase = Depends(get_current_user)):
    try:
        import gitlab
        # private token or personal token authentication (GitLab.com)
        gl = gitlab.Gitlab(private_token=account.token)
        gl.auth()
    except gitlab.GitlabAuthenticationError as e:
        raise HTTPException(detail=f'Ivalid Token! {e}',
                            status_code=status.HTTP_401_UNAUTHORIZED)

    async with db as session:
        # try:
        #     value = AccountEnum.__getitem__(account.kind_of_account).value
        #     print(value)
        # except:
        #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
        #                         detail=f'Invalid kind_of_account')
        query = select(AccountModel).filter(AccountModel.saved_by_id == current_user.id,
                                            AccountModel.kind_of_account == account.kind_of_account)
        result = await session.execute(query)
        temp_account: UserSchemaBase = result.scalars().unique().one_or_none()

        if temp_account:
            raise HTTPException(detail='O usuário já possuí uma conta do mesmo tipo/natureza.',
                            status_code=status.HTTP_409_CONFLICT)
        new_account: AccountSchemaCreate = AccountModel(
            kind_of_account=account.kind_of_account,
            token=account.token,
            saved_by_id=current_user.id
        )

        try:
            db.add(new_account)
            await db.commit()

            return new_account
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'{e}')

# GET Usuarios | sem a restrição de um usuario logado


@router.get('/', response_model=List[UserSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        usuarios: List[UserSchemaBase] = result.scalars().unique().all()

        return usuarios

# GET Usuário


@router.get('/{usuario_id}', response_model=UserSchemaBase)
async def get_artigo(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UserSchemaBase = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        raise HTTPException(detail='Usuário não encontrado',
                            status_code=status.HTTP_404_NOT_FOUND)

# POST login


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario: UserSchemaBase = await authentication(email=form_data.username, password=form_data.password, db=db)

    if not usuario:
        raise HTTPException(detail='Dados de acesso incorretos.',
                            status_code=status.HTTP_400_BAD_REQUEST)
    print(usuario)
    return JSONResponse(
        content={
            "access_token": create_access(sub=str(usuario.id)), 
            "token_type": "bearer",
            "data": jsonable_encoder(usuario)
            },
        status_code=status.HTTP_200_OK
    )
