from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from ..messaging import send_message

router = APIRouter(prefix="/carros", tags=["Carros"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.CarroOut])
def listar(db: Session = Depends(get_db)):
    try:
        print("LOG: Listando todos os carros")
        return db.query(models.Carro).all()
    except Exception:
        raise HTTPException(500, "Erro ao listar carros")

@router.get("/{carro_id}", response_model=schemas.CarroOut)
def obter(carro_id: int, db: Session = Depends(get_db)):
    try:
        print(f"LOG: Obtendo carro ID={carro_id}")
        carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()
        if not carro:
            print(f"LOG: Carro ID={carro_id} não encontrado")
            raise HTTPException(404, "Carro não encontrado")
        return carro
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Erro ao obter carro")

@router.post("/", response_model=schemas.CarroOut)
def criar(payload: schemas.CarroCreate, db: Session = Depends(get_db)):
    try:
        print(f"LOG: Criando carro com payload={payload.model_dump()}")
        carro = models.Carro(**payload.model_dump())
        db.add(carro)
        db.commit()
        db.refresh(carro)
        send_message("carros_queue", {"evento": "carro_criado", "id": carro.id})
        print(f"LOG: Carro criado ID={carro.id}")
        return carro
    except Exception:
        raise HTTPException(500, "Erro ao criar carro")

@router.put("/{carro_id}", response_model=schemas.CarroOut)
def atualizar(carro_id: int, payload: schemas.CarroCreate, db: Session = Depends(get_db)):
    try:
        print(f"LOG: Atualizando carro ID={carro_id} com payload={payload.model_dump()}")
        carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()
        if not carro:
            print(f"LOG: Carro ID={carro_id} não encontrado para atualização")
            raise HTTPException(404, "Carro não encontrado")

        for k, v in payload.model_dump().items():
            setattr(carro, k, v)

        db.commit()
        db.refresh(carro)
        send_message("carros_queue", {"evento": "carro_atualizado", "id": carro.id})
        print(f"LOG: Carro atualizado ID={carro.id}")
        return carro
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Erro ao atualizar carro")

@router.patch("/{carro_id}", response_model=schemas.CarroOut)
def atualizar_parcial(carro_id: int, payload: schemas.CarroUpdate, db: Session = Depends(get_db)):
    try:
        print(f"LOG: Atualização parcial do carro ID={carro_id}, dados={payload.model_dump(exclude_unset=True)}")
        carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()
        if not carro:
            print(f"LOG: Carro ID={carro_id} não encontrado para PATCH")
            raise HTTPException(404, "Carro não encontrado")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(carro, k, v)

        db.commit()
        db.refresh(carro)
        send_message("carros_queue", {"evento": "carro_atualizado", "id": carro.id})
        print(f"LOG: Carro parcialmente atualizado ID={carro.id}")
        return carro
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Erro ao atualizar parcialmente o carro")

@router.delete("/{carro_id}")
def deletar(carro_id: int, db: Session = Depends(get_db)):
    try:
        print(f"LOG: Deletando carro ID={carro_id}")
        carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()
        if not carro:
            print(f"LOG: Carro ID={carro_id} não encontrado para deleção")
            raise HTTPException(404, "Carro não encontrado")

        db.delete(carro)
        db.commit()

        send_message("carros_queue", {"evento": "carro_deletado", "id": carro_id})
        print(f"LOG: Carro deletado ID={carro_id}")
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Erro ao deletar carro")
