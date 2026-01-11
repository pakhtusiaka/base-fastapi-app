from core.schemas.user import UserSchema
from auth import jwt_help
from pydantic  import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)

http_bearer = HTTPBearer()

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

def get_currnet_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchema:
    token = credentials.credentials
    try:
        payload = jwt_help.decode_jwt(
            token=token,
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid",
        )
    return payload


def get_currnet_auth_user(
    payload: dict = Depends(get_currnet_token_payload)
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := user_db.get(username):
        return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )

    # print(token)

def get_currnet_active_auth_user(
    user: UserSchema = Depends(get_currnet_auth_user)
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )

@router.get("/user/me/")
def auth_user_check_info(
    payload: dict = Depends(get_currnet_token_payload),
    user: UserSchema = Depends(get_currnet_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "is_active": user.active,
        "logged_in_at": iat,
    }