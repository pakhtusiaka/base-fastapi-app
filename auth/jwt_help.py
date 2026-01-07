import jwt

from core.config import settings
from pwlib import PasswordHash

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str =settings.auth_jwt.algorithm,
    expire_minutes: int =settings.auth_jwt.access_token_expire_minutes,
    expire_minutes: int =settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta:  timedelta | None = None,
):
    to_encode = payload.copy()
    now =datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
        )
    return encoded

def decode(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str =settings.auth_jwt.algorithm,

):
    decode = jwt.decode(
        token, 
        public_key, 
        algorithms=[algorithms],
        )
    return decode

def hash_password(password: str) -> str:
    return PasswordHash.hash(password)

def validate_password(password: str, hashed_password: str) -> bool:
    return PasswordHash.verify(password, hashed_password)



# encoded = jwt.encode({"some": "payload"}, private_key, algorithm="EdDSA")
# decode(encoded, public_key, algorithms=["EdDSA"])
# {'some': 'payload'}