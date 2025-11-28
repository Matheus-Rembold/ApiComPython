from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Carro(Base):
    __tablename__ = "carros"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    motor = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    placa = Column(String, nullable=False)

    servicos = relationship("Servico", back_populates="carro")


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    tempo_servico = Column(Integer, nullable=False)

    carro_id = Column(Integer, ForeignKey("carros.id"), nullable=False)

    carro = relationship("Carro", back_populates="servicos")
