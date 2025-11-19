from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Carro(Base):
    __tablename__ = "carros"
    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    motor = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    placa = Column(String, unique=True, nullable=False)

class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    tempo_servico = Column(Integer, nullable=False)
