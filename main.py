from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from core.config import settings

from api import router as api_router
from core.models import db_helper
from pydantic import BaseModel, constr, EmailStr
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
    first_name: constr(min_length=2, max_length=30)
    second_name: constr(min_length=2, max_length=30)
    email: EmailStr
    password: constr(min_length=8 , max_length=100)
    telephone: constr(min_length=12 , max_length=15)

# class UserData2(BaseModel):
#     first_name: Annotated[str, Query(min_length=2, max_length=30)] = 
#     second_name: Union[str, None] = None
#     email:str
#     password:str
#     telephone:str | None = None


# @main_app.post('/registration/')
# async def registration_user (userdata: UserData):
#     return userdata

@main_app.post('/registration/')
async def registration_user (user_data: UserData):
    return {
        "first_name": user_data.first_name,
        "second_name": user_data.second_name,
        "email": user_data.email,
        "password": user_data.password,
        "telephone": user_data.telephone
    }

@main_app.get('/login/')
async def login_user (userdata: UserData):
    return userdata

if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True
)