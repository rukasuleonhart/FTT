from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import func, UniqueConstraint, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), onupdate=func.now())

# Modelo Bloco
@table_registry.mapped_as_dataclass
class Bloco:
    __tablename__ = "blocos"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(unique=True, nullable=False)
    identificacao: Mapped[str] = mapped_column(unique=True, nullable=False)

    salas: Mapped[List["Sala"]] = relationship("Sala", back_populates="bloco", cascade="all, delete-orphan", init=False)

# Modelo Sala
@table_registry.mapped_as_dataclass
class Sala:
    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    numero: Mapped[str] = mapped_column(nullable=False)  # Número da sala
    bloco_id: Mapped[int] = mapped_column(ForeignKey("blocos.id"), nullable=False)  # FK para Bloco
    capacidade: Mapped[int] = mapped_column(nullable=False)
    recursos: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)  # Lista de recursos disponíveis na sala
    exclusiva_para: Mapped[str] = mapped_column(nullable=True)  # Curso específico ou NULL

    bloco: Mapped["Bloco"] = relationship("Bloco", back_populates="salas")
    reservas: Mapped[List["Reserva"]] = relationship("Reserva", back_populates="sala", cascade="all, delete-orphan", init=False)

    __table_args__ = (UniqueConstraint("bloco_id", "numero", name="uq_bloco_sala"),)

# Modelo Reserva
@table_registry.mapped_as_dataclass
class Reserva:
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    sala_id: Mapped[int] = mapped_column(ForeignKey("salas.id"), nullable=False) 
    sala: Mapped["Sala"] = relationship("Sala", back_populates="reservas", init=False)
    
    coordenador: Mapped[str] = mapped_column(nullable=False)
    motivo: Mapped[str] = mapped_column(nullable=False)
    data_inicio: Mapped[datetime] = mapped_column(nullable=False)
    data_fim: Mapped[datetime] = mapped_column(nullable=False)
    frequencia: Mapped[str] = mapped_column(nullable=True) 
    
    recorrente: Mapped[bool] = mapped_column(default=False, nullable=False)  # Movido para o final

    __table_args__ = (
        UniqueConstraint("sala_id", "data_inicio", "data_fim", name="uq_reserva_sala_horario"),
    )