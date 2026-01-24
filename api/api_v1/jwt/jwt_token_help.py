from auth import jwt_help
from core.schemas.user import UserSchema
from datetime import timedelta
from core.config import settings

TOKEN_TYPE_FIELD = "token_type"
ACCESS_TYPE_TOKEN = "access"
REFRESH_TYPE_TOKEN = "refresh"

def create_jwt(
    token_type: str, 
    jwt_data_payload: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(jwt_data_payload)
    return jwt_help.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
        )

def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        #subject of the token
        "sub": user.username,
        # "username": user.username,
        # "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TYPE_TOKEN,
        jwt_data_payload=jwt_payload,
        
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )

def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(
        token_type=REFRESH_TYPE_TOKEN,
        jwt_data_payload=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),   

    )
