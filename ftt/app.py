from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select

from ftt.schemas import BlocoSchema, MessageSchema, SalaSchema, UserPublic, UserSchema, UserDB, UserList
from ftt.settings import Settings
from ftt.database import get_session
from ftt.models import User

app = FastAPI()

@app.get("/", status_code=HTTPStatus.OK, response_model=MessageSchema)
def pagina_inicial():
    return {'message': 'Olá, seja bem vindo !'}

@app.post('/users/', status_code=HTTPStatus.CREATED , response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):

    db_user = session.scalar(select(User).where(User.username == user.username))
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Usuário já existe',
        )
    
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email já existe',
        )

    db_user = User(
        username=user.username, 
        password=user.password, 
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

    
    
@app.post('/cadastro_bloco/', status_code=HTTPStatus.CREATED, response_model=BlocoSchema)
def cadastro_bloco(bloco=BlocoSchema):
    return bloco

@app.post('/cadastro_sala/', status_code=HTTPStatus.CREATED, response_model=SalaSchema)
def cadastro_sala(sala=SalaSchema):
    return sala

@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10, # limitador de usuários
    offset: int = 0, # onde começa a busca
    session=Depends(get_session)
):
    user = session.scalars(
        select(User).limit(limit).offset(offset)
    )
    return {'users': user}

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado"
        )
    db_user.email = user.email
    db_user.username = user.username
    db_user.password = user.password

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
   
@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
def delete_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )
    session.delete(db_user)
    session.commit()

    return {'message': 'Usuário deletado'}
    
