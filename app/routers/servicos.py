from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/servicos", tags=["Serviços"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.ServicoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(models.Servico).all()

@router.get("/{servico_id}", response_model=schemas.ServicoOut)
def obter(servico_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
    if not item:
        raise HTTPException(404)
    return item

@router.post("/", response_model=schemas.ServicoOut)
def criar(payload: schemas.ServicoCreate, db: Session = Depends(get_db)):
    item = models.Servico(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/{servico_id}", response_model=schemas.ServicoOut)
def atualizar(servico_id: int, payload: schemas.ServicoCreate, db: Session = Depends(get_db)):
    item = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
    if not item:
        raise HTTPException(404)
    for k, v in payload.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

@router.patch("/{servico_id}", response_model=schemas.ServicoOut)
def atualizar_parcial(servico_id: int, payload: schemas.ServicoUpdate, db: Session = Depends(get_db)):
    item = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
    if not item:
        raise HTTPException(404)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{servico_id}")
def deletar(servico_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
    if not item:
        raise HTTPException(404)
    db.delete(item)
    db.commit()
    return {"status": "ok"}
