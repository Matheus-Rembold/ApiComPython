from pydantic import BaseModel
from datetime import date

class CarroBase(BaseModel):
    marca: str
    modelo: str
    motor: str
    ano: int
    placa: str

class CarroCreate(CarroBase):
    pass

class CarroUpdate(BaseModel):
    marca: str | None = None
    modelo: str | None = None
    motor: str | None = None
    ano: int | None = None
    placa: str | None = None

class CarroOut(CarroBase):
    id: int
    class Config:
        from_attributes = True

class ServicoBase(BaseModel):
    descricao: str
    valor: float
    data: date
    tempo_servico: int

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(BaseModel):
    descricao: str | None = None
    valor: float | None = None
    data: date | None = None
    tempo_servico: int | None = None

class ServicoOut(ServicoBase):
    id: int
    class Config:
        from_attributes = True
