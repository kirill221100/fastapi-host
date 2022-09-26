import asyncio
from uvicorn import run
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from routes.host import router as host_router
from routes.auth import router as auth_router
from db.db_setup import init_db


# from db.models import user_model, host_model

# user_model.UserModel.metadata.create_all(bind=engine)
# host_model.HostModel.metadata.create_all(bind=engine)

def db_init_models():
    asyncio.run(init_db())



app = FastAPI()

app.include_router(auth_router)
app.include_router(host_router)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(SessionMiddleware, secret_key='secret')

if __name__ == '__main__':
    db_init_models()
    run("main:app", reload=True)
