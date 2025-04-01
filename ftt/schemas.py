from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# Mensagem
class MessageSchema(BaseModel):
    message: str

# Salas
class RoomSchema(BaseModel):
    block_id: int
    name: str
    capacity: int
    resource: str

#Blocos
class BlockSchema(BaseModel):
    name: str
    identifier: str

# Reversas
class ReservationSchema(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    coordinator: str
    reason: str
    status: str

# Usuário de entrada
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# Usuário exibido
class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

# Segurança
class TokenSchema(BaseModel):
    access_token: str
    token_type: str

# Transforma Dicionario em Lista
class UserList(BaseModel):
    users: list[UserPublic]