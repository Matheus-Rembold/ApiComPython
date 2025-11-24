from fastapi import FastAPI
from .database import Base, engine
from .routers import carros, servicos

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(carros.router)
app.include_router(servicos.router)

@app.get("/health")
def health():
    return {"status": "ok"}
