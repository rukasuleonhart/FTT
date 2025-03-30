from datetime import datetime, time
from pydantic import BaseModel, EmailStr

class MessageSchema(BaseModel):
    message: str

class SalaSchema(BaseModel):
    bloco_id: int
    nome: str
    capacidade: int
    recurso: str


class BlocoSchema(BaseModel):
    nome: str
    identificador: str


class ReservaSchema(BaseModel):
    sala_id: int
    data: datetime
    hora_inicio: time
    hora_fim: time
    coordenador: str
    motivo: str
    status: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: int
    username: str
    email: str

class UserDB(UserSchema):
    id: int

class UserList(BaseModel):
    users: list[UserPublic]