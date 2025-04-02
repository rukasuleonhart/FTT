from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ftt.database import get_db
from ftt import models, schemas  # 🔥 Correção aqui!
from typing import List

router = APIRouter(prefix="/blocos", tags=["Blocks"])


@router.post("/", response_model=schemas.BlocoResponse)
def create_bloco(bloco: schemas.BlocoCreate, db: Session = Depends(get_db)):
    """Cria um novo bloco"""
    db_bloco = models.Bloco(**bloco.dict())
    db.add(db_bloco)
    db.commit()
    db.refresh(db_bloco)
    return db_bloco


@router.get("/", response_model=List[schemas.BlocoResponse])
def list_blocos(db: Session = Depends(get_db)):
    """Lista todos os blocos"""
    return db.query(models.Bloco).all()
