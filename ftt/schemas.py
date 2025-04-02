from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


# -------------------- MENSAGENS --------------------
class Message(BaseModel):
    message: str


# -------------------- USUÁRIOS --------------------
class UserSchema(BaseModel):
    username: str = Field(..., example="usuario123")
    email: EmailStr = Field(..., example="email@example.com")
    password: str = Field(..., min_length=6, example="securepassword")


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserList(BaseModel):
    users: List[UserPublic]


# -------------------- AUTENTICAÇÃO --------------------
class Token(BaseModel):
    access_token: str
    token_type: str


# -------------------- PAGINAÇÃO --------------------
class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


# -------------------- BLOCO --------------------
class BlocoBase(BaseModel):
    nome: str = Field(..., example="Bloco A")
    identificacao: str = Field(..., example="A")


class BlocoCreate(BlocoBase):
    pass


class BlocoResponse(BlocoBase):
    id: int

    class Config:
        from_attributes = True


# -------------------- SALA --------------------
class SalaBase(BaseModel):
    numero: str = Field(..., example="101")
    capacidade: int = Field(..., example=40)
    recursos: Optional[List[str]] = Field(None, example=["Projetor", "Ar-condicionado"])
    exclusiva_para: Optional[str] = Field(None, example="Engenharia Civil")


class SalaCreate(SalaBase):
    bloco_id: int


class SalaResponse(SalaBase):
    id: int
    bloco_id: int

    class Config:
        from_attributes = True


# -------------------- RESERVA --------------------
class ReservaBase(BaseModel):
    coordenador: str = Field(..., example="Prof. João Silva")
    motivo: str = Field(..., example="Reunião pedagógica")
    data_inicio: datetime
    data_fim: datetime
    recorrente: Optional[bool] = Field(False, example=False)
    frequencia: Optional[str] = Field(None, example="semanal")


class ReservaCreate(ReservaBase):
    sala_id: int


class ReservaResponse(ReservaBase):
    id: int
    sala_id: int

    class Config:
        from_attributes = True
