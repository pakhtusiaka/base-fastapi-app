from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from core.config import settings

from api import router as api_router
from core.models import db_helper
from pydantic import BaseModel
from typing import Union, Annotated

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print('dispose engine')
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(
    api_router,
)



class UserData(BaseModel):
    first_name:str
    second_name: Union[str, None] = None
    email:str
    password:str
    telephone:str | None = None


@main_app.post('/registration/')
async def registration_user (userdata: UserData):
    return userdata

@main_app.get('/login/')
async def login_user (userdata: UserData):
    return userdata

if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True
)