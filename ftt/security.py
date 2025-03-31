from pwdlib import PasswordHash
from zoneinfo import ZoneInfo
from jwt import encode
from datetime import datetime, timedelta

pwd_context = PasswordHash.recommended()

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 1 hora tempo do token

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verifify(plain_password), hashed_password

def create_access_token(data_playload: dict):
    to_encode = data_playload.copy()

    # Adiciona 1 hora para expiração
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

