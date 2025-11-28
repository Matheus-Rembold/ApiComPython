from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from ..messaging import send_message

router = APIRouter(prefix="/servicos", tags=["Serviços"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.ServicoOut])
def listar(db: Session = Depends(get_db)):
    try:
        print("LOG: Listando todos os serviços")
        return db.query(models.Servico).all()
    except Exception:
        raise HTTPException(500, "Erro ao listar serviços")

@router.get("/{servico_id}", response_model=schemas.ServicoOut)
def obter(servico_id: int, db: Session = Depends(get_db)):
    try:
        print(f"LOG: Obtendo serviço ID={servico_id}")
        item = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
        if not item:
            print(f"LOG: Serviço ID={servico_id} não encontrado")
            raise HTTPException(404, "Serviço não encontrado")
        return item
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Erro ao obter serviço")

@router.post("/", response_model=schemas.ServicoOut)
def criar(payload: schemas.ServicoCreate, db: Session = Depends(get_db)):
    try:
        print(f"LOG: Criando serviço com payload={payload.model_dump()}")
        item = models.Servico(**payload.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        send_message("servicos_queue", {"evento": "servico_criado", "id": item.id})
        print(f"LOG: Serviço criado ID={item.id}")
        return item
    except Exception:
        raise HTTPException(500, "Erro ao criar serviço")

@router.put("/{servico_id}", response_model=schemas.ServicoOut)
def atualizar(servico_id: int, payload: schemas.ServicoCreate, db: Session = Depends(get_db)):
    try:
        print(f"LOG: Atualizando serviço ID={servico_id} com payload={payload.model_dump()}")
        item = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
        if not item:
            print(f"LOG: Serviço ID={servico_id} não encontrado para atualização")
            raise HTTPException(404, "Serviço não encontrado")

        for k, v in payload.model_dump().items():
            setattr(item, k, v)

        db.commit()
        db.refresh(item)
        send_message("servicos_queue", {"evento": "servico_atualizado", "id": item.id})
        print(f"LOG: Serviço atualizado ID={item.id}")
        return item
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Erro ao atualizar serviço")

@router.patch("/{servico_id}", response_model=schemas.ServicoOut)
def atualizar_parcial(servico_id: int, payload: schemas.ServicoUpdate, db: Session = Depends(get_db)):
    try:
        dados = payload.model_dump(exclude_unset=True)
        print(f"LOG: Atualização parcial do serviço ID={servico_id}, dados={dados}")
        item = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
        if not item:
            print(f"LOG: Serviço ID={servico_id} não encontrado para PATCH")
            raise HTTPException(404, "Serviço não encontrado")

        for k, v in dados.items():
            setattr(item, k, v)

        db.commit()
        db.refresh(item)
        send_message("servicos_queue", {"evento": "servico_atualizado", "id": item.id})
        print(f"LOG: Serviço parcialmente atualizado ID={item.id}")
        return item
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Erro ao atualizar parcialmente o serviço")

@router.delete("/{servico_id}")
def deletar(servico_id: int, db: Session = Depends(get_db)):
    try:
        print(f"LOG: Deletando serviço ID={servico_id}")
        item = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
        if not item:
            print(f"LOG: Serviço ID={servico_id} não encontrado para deleção")
            raise HTTPException(404, "Serviço não encontrado")

        db.delete(item)
        db.commit()
        send_message("servicos_queue", {"evento": "servico_deletado", "id": servico_id})
        print(f"LOG: Serviço deletado ID={servico_id}")
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Erro ao deletar serviço")
