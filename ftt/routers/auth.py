# ==============================================================================================================================#
 #                                            📚 B I B L I O T E C A S                                                         #               
# ==============================================================================================================================#
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select

# ==============================================================================================================================#
 #                                            ⬇️  I M P O R T S                                                                #
# ==============================================================================================================================#
from ftt.schemas import TokenSchema
from ftt.database import get_session
from ftt.models import User
from ftt.security import verify_password, create_access_token

# ==============================================================================================================================#
 #                                        ⚙️ C O N F I G  -  R O U T E R                                                       #
# ==============================================================================================================================#
router = APIRouter(prefix='/auth',tags=['🔑 | Autenticação'])

# ==============================================================================================================================#
 #                                                  📜 P O S T                                                                 #
# ==============================================================================================================================#
@router.post('/token', response_model=TokenSchema)
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