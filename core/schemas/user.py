from pydantic import BaseModel 

class UserData(BaseModel):
    first_name: str
    second_name: str
    email: str
    password: str
    telephone: str

class CreateUserData(UserData):
    pass

class ReadUserData(UserData):
    id: int