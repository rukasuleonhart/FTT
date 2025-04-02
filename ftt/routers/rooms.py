from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ftt.database import get_db
from ftt import models, schemas
from typing import List

router = APIRouter(prefix="/salas", tags=["Rooms"])


@router.post("/", response_model=schemas.SalaResponse)
def create_sala(sala: schemas.SalaCreate, db: Session = Depends(get_db)):
    """Cria uma nova sala dentro de um bloco"""
    db_sala = models.Sala(**sala.dict())
    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala


@router.get("/", response_model=List[schemas.SalaResponse])
def list_salas(db: Session = Depends(get_db)):
    """Lista todas as salas"""
    return db.query(models.Sala).all()
