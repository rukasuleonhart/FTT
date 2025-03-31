# Bibliotecas
from pwdlib import PasswordHash
import pytz
from http import HTTPStatus
from jwt import encode, decode
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
# Importes
from ftt.database import get_session
from ftt.models import User

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora tempo do token

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)  # Correção aqui

def create_access_token(data_payload: dict):
    to_encode = data_payload.copy()

    # Adiciona 1 hora para expiração
    expire = datetime.now(pytz.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_current_user(
        session: Session = Depends(get_session),
        token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail= 'Não foi possível validar as credenciais',
        headers={'WWW-Authenticate':'Bearer'},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    
    user_db = session.scalar(
        select(User).where(User.username == username)
    )

    if not user_db:
        raise credentials_exception
    
    return user_db
