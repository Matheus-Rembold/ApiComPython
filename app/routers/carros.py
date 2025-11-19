from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/carros", tags=["Carros"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.CarroOut])
def listar(db: Session = Depends(get_db)):
    return db.query(models.Carro).all()

@router.get("/{carro_id}", response_model=schemas.CarroOut)
def obter(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()
    if not carro:
        raise HTTPException(404)
    return carro

@router.post("/", response_model=schemas.CarroOut)
def criar(payload: schemas.CarroCreate, db: Session = Depends(get_db)):
    carro = models.Carro(**payload.model_dump())
    db.add(carro)
    db.commit()
    db.refresh(carro)
    return carro

@router.put("/{carro_id}", response_model=schemas.CarroOut)
def atualizar(carro_id: int, payload: schemas.CarroCreate, db: Session = Depends(get_db)):
    carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()
    if not carro:
        raise HTTPException(404)
    for k, v in payload.model_dump().items():
        setattr(carro, k, v)
    db.commit()
    db.refresh(carro)
    return carro

@router.patch("/{carro_id}", response_model=schemas.CarroOut)
def atualizar_parcial(carro_id: int, payload: schemas.CarroUpdate, db: Session = Depends(get_db)):
    carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()
    if not carro:
        raise HTTPException(404)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(carro, k, v)
    db.commit()
    db.refresh(carro)
    return carro

@router.delete("/{carro_id}")
def deletar(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()
    if not carro:
        raise HTTPException(404)
    db.delete(carro)
    db.commit()
    return {"status": "ok"}
