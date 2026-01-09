from core.schemas.user import UserSchema
from auth import jwt_help
from pydantic  import BaseModel

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)

class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter(prefix="/jwt", tags=["JWT"])

john = UserSchema(
    username='john',
    password=jwt_help.hash_password("qwerty"),
    email="john@example.com"
)

sam = UserSchema(
    username='sam',
    password=jwt_help.hash_password("secret"),
    email="john@example.com"
)

user_db: dict[str, UserSchema] ={
    john.username: john,
    sam.username:sam,
}

def validate_auth_user(
    username: str = Form(),
    password: str = Form()
    ):
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := user_db.get(username)):
        raise unauth_exception
    if not jwt_help.validate_password(
        password=password,
        hashed_password=user.password
        ):
        raise unauth_exception
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="inactive user",
        )
        
    return user
   

@router.post(path="/login/", response_model=Token)
def auth_user_jwt(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        #subject of the token
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token =jwt_help.encode_jwt(jwt_payload)
    return Token(
        access_token=token, 
        token_type="bearer"
        )