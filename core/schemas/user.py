from pydantic import BaseModel
from datetime import datetime

class UserData(BaseModel):
    first_name: str
    second_name: str
    email: str
    password: str
    hashed_password: str
    telephone: str
    active: bool = True

class CreateUserData(UserData):
    pass

class ReadUserData(UserData):
    id: int

class AccessToken(BaseModel):
    user_id: int
    expires_access_token: datetime
    refresh_token: datetime

class UpdateAccessToken(BaseModel):
    pass