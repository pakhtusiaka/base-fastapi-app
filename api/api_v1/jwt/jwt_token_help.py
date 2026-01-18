from auth import jwt_help
from core.schemas.user import UserSchema

TOKEN_TYPE_FIELD = "token_type"
ACCESS_TYPE_TOKEN = "access"
REFRESH_TYPE_TOKEN = "refresh"

def create_jwt(token_type: str, jwt_payload: dict) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(jwt_payload)
    return jwt_help.encode_jwt(jwt_payload)

def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        #subject of the token
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TYPE_TOKEN,
        jwt_payload=jwt_payload,
    )

def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(
        token_type=REFRESH_TYPE_TOKEN,
        jwt_payload=jwt_payload,
    )
