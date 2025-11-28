from fastapi import FastAPI
from .database import Base, engine
from .routers import carros, servicos
from fastapi.exceptions import HTTPException
from .exceptions import http_exception_handler, generic_exception_handler


app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(carros.router)
app.include_router(servicos.router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

@app.get("/health")
def health():
    return {"status": "ok"}
