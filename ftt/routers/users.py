# ==============================================================================================================================#
 #                                            📚 B I B L I O T E C A S                                                         #               
# ==============================================================================================================================#
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from http import HTTPStatus

# ==============================================================================================================================#
 #                                            ⬇️  I M P O R T S                                                                #
# ==============================================================================================================================#
from ftt.models import User
from ftt.database import get_session
from ftt.schemas import UserList, UserPublic, UserSchema, MessageSchema
from ftt.security import get_password_hash, get_current_user

# ==============================================================================================================================#
 #                                        ⚙️ C O N F I G  -  R O U T E R                                                       #
# ==============================================================================================================================#
router = APIRouter(prefix='/users',tags=['👤 | Usúarios'])

# ==============================================================================================================================#
 #                                                   ✉️ G E T                                                                  #
# ==============================================================================================================================#

@router.get('/', response_model=UserList)
def read_users(
    limit: int = 10, # limitador de usuários
    offset: int = 0, # onde começa a busca
    session=Depends(get_session)
):
    user = session.scalars(
        select(User).limit(limit).offset(offset)
    )
    return {'users': user}

# ==============================================================================================================================#
 #                                                  📜 P O S T                                                                 #
# ==============================================================================================================================#

@router.post('/', status_code=HTTPStatus.CREATED , response_model=UserPublic)
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
# ==============================================================================================================================#
 #                                                    🔄️ P U T                                                                 #
# ==============================================================================================================================#

@router.put('/{user_id}', response_model=UserPublic)
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

# ==============================================================================================================================#
 #                                                     🗑️ DELETE                                                               #
# ==============================================================================================================================#

@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=MessageSchema)
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