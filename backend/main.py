from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core.configs import settings
from api.v1.api import api_router

origins = ['*']

app = FastAPI(title='CommitLand API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router, prefix=settings.API_V1_STR)
#app.include_router(api_router,prefix=settings.API_V2_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level='info', reload=True)


"""

"""
