from fastapi import FastAPI
from .database import Base, engine
from .routers import carros, servicos
from app.database import engine, SessionLocal
from app.models import Carro, Servico
from sqlalchemy.future import select

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(carros.router)
app.include_router(servicos.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
async def seed_database():
    async with SessionLocal() as session:
        # Carro
        result = await session.execute(select(Carro))
        carros_existem = result.scalars().first()

        if not carros_existem:
            carro = Carro(
                marca="Toyota",
                modelo="Corolla",
                motor="2.0",
                ano=2020,
                placa="ABC1234"
            )
            session.add(carro)
            await session.commit()

        # Servico
        result = await session.execute(select(Servico))
        servicos_existem = result.scalars().first()

        if not servicos_existem:
            servico = Servico(
                descricao="Troca de óleo",
                valor=250,
                data="2024-01-01",
                tempo_servico="2h"
            )
            session.add(servico)
            await session.commit()