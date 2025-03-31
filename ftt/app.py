from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

from ftt.schemas import BlocoSchema, MessageSchema, SalaSchema, UserPublic, UserSchema, UserList, TokenSchema
from ftt.settings import Settings
from ftt.database import get_session
from ftt.models import User
from ftt.security import get_password_hash, verify_password, create_access_token, get_current_user

app = FastAPI()

# GET

@app.get("/", status_code=HTTPStatus.OK, response_model=MessageSchema)
def pagina_inicial():
    return {'message': 'Olá, seja bem vindo !'}

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

# POST

@app.post('/users/', status_code=HTTPStatus.CREATED , response_model=UserPublic)
def create_user(
    user: UserSchema, 
    session=Depends(get_session),
):

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
        password=get_password_hash(user.password), 
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.post('/token', response_model=TokenSchema)
def login_for_access_token(
    session=Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()  
):
    user = session.scalar(select(User).where(User.username == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect username or password'
        )
    access_token = create_access_token(data_payload={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}

# PUT

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, 
    user: UserSchema, 
    session=Depends(get_session),
    current_user=Depends(get_current_user), # Verifica se o usuário esta lougado.
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Você não tem permissão')

    current_user.email = user.email
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user
   
# DELETE

@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
def delete_user(
    user_id: int, 
    session=Depends(get_session),
    current_user=Depends(get_current_user), # Verifica se o usuário esta lougado.
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Você não tem permissão')

    session.delete(current_user)
    session.commit()

    return {'message': 'Usuário deletado'}