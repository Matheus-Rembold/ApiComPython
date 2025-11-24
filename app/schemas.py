from pydantic import BaseModel
from datetime import date

# ---------------- CARROS ----------------

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
    servicos: list["ServicoOut"] = []

    class Config:
        from_attributes = True


# ---------------- SERVIÇOS ----------------

class ServicoBase(BaseModel):
    descricao: str
    valor: float
    data: date
    tempo_servico: int

class ServicoCreate(ServicoBase):
    carro_id: int

class ServicoUpdate(BaseModel):
    descricao: str | None = None
    valor: float | None = None
    data: date | None = None
    tempo_servico: int | None = None
    carro_id: int | None = None

class ServicoOut(ServicoBase):
    id: int
    carro_id: int

    class Config:
        from_attributes = True
