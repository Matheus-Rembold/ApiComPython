from fastapi import FastAPI
from .database import Base, engine
from .routers import carros, servicos

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(carros.router)
app.include_router(servicos.router)

@app.get("/health")
def health():
    return {"status": "ok"}
