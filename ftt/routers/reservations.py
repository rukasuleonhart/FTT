from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ftt.database import get_db
from ftt import models, schemas
from typing import List

router = APIRouter(prefix="/reservas", tags=["Reservations"])


@router.post("/", response_model=schemas.ReservaResponse)
def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    """Cria uma reserva de sala"""
    # Verifica se a sala existe
    sala = db.query(models.Sala).filter(models.Sala.id == reserva.sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")

    # Verifica conflitos de horário
    conflito = db.query(models.Reserva).filter(
        models.Reserva.sala_id == reserva.sala_id,
        models.Reserva.data_inicio < reserva.data_fim,
        models.Reserva.data_fim > reserva.data_inicio
    ).first()

    if conflito:
        raise HTTPException(status_code=400, detail="Conflito de horário para a reserva")

    db_reserva = models.Reserva(**reserva.dict())
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


@router.get("/", response_model=List[schemas.ReservaResponse])
def list_reservas(db: Session = Depends(get_db)):
    """Lista todas as reservas"""
    return db.query(models.Reserva).all()


@router.delete("/{reserva_id}/", response_model=schemas.Message)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Cancela uma reserva"""
    reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    db.delete(reserva)
    db.commit()
    return {"message": "Reserva cancelada com sucesso"}
