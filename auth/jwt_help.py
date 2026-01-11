import jwt
from datetime import datetime,timedelta
from core.config import settings
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str =settings.auth_jwt.algorithm,
    expire_minutes: int =settings.auth_jwt.access_token_expire_minutes,
    # expire_day: int =settings.auth_jwt.access_token_expire_day,
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
        to_encode,
        private_key,
        algorithm=algorithm,
        )
    return encoded

def decode_jwt(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str =settings.auth_jwt.algorithm,

):
    decode = jwt.decode(
        token, 
        public_key, 
        algorithms=[algorithm],
        )
    return decode

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def validate_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)



# encoded = jwt.encode({"some": "payload"}, private_key, algorithm="EdDSA")
# decode(encoded, public_key, algorithms=["EdDSA"])
# {'some': 'payload'}