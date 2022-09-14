from fastapi import APIRouter
from api.v1.endpoints import user
from api.v1.endpoints import conexion

api_router = APIRouter()
api_router.include_router(user.router, prefix='/users', tags=['users'])
api_router.include_router(conexion.router)
