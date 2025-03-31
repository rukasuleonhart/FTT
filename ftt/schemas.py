from datetime import datetime, time
from pydantic import BaseModel, EmailStr, ConfigDict

# Mensagem
class MessageSchema(BaseModel):
    message: str

# Salas
class SalaSchema(BaseModel):
    bloco_id: int
    nome: str
    capacidade: int
    recurso: str

#Blocos
class BlocoSchema(BaseModel):
    nome: str
    identificador: str

# Reversas
class ReservaSchema(BaseModel):
    sala_id: int
    data: datetime
    hora_inicio: time
    hora_fim: time
    coordenador: str
    motivo: str
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

# Teste
class UserDB(UserSchema):
    id: int

class UserList(BaseModel):
    users: list[UserPublic]