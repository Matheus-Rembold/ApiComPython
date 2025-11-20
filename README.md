# Api com python
O intuito desse trabalho era fazer a construcao de uma api, a matéria da faculdade que passou esse trabalho foi Desenvolvimento de Apis e Micro Serviços.
o Escopo minimo para a api era:
- Recursos (dois CRUDs)
- Mensageria
- Contêineres e Orquestração
-  Documentação e Testes
-  Observabilidade e Robustez

## Recursos
Fiz dois CRUDS carros e serviços. Para começar, criei o dataset que iria utilizar, no caso o escolhido foi postgress, criei um arquivo chamado database.py e dentro dele passei o seguinte codigo
```python
DB_USER = os.getenv("DB_USER", "postgres") # le a varivel de ambiente DB_USER, se nao tiver usa postgres, faz isso para todos
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "oficina")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# Monta a string de conexão (URL) para o SQLAlchemy usando formatação f-string. O formato 
# postgresql://user:pass@host:port/dbname indica o dialect (postgresql)

engine = create_engine(DATABASE_URL) # Cria o Engine do SQLAlchemy a partir da DATABASE_URL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() # ria a classe base Base que os modelos ORM devem estender.
```
Assim criando o database.

Entao em sequencia criei os models que foram os seguintes:

``` python
class Carro(Base): #Cria um modelo ORM chamado Carro, herdando de Base.
#Isso faz com que o SQLAlchemy reconheça essa classe como uma tabela.
    __tablename__ = "carros"
    id = Column(Integer, primary_key=True, index=True) # criando as colunas com o que ela é, se é primary key ou nao
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    motor = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    placa = Column(String, unique=True, nullable=False)]
    servicos = relationship("Servico", back_populates="carro") # relacao com servicos

class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    tempo_servico = Column(Integer, nullable=False)

    carro_id = Column(Integer, ForeignKey("carros.id"), nullable=False) # relacao com carro

    carro = relationship("Carro", back_populates="servicos")

```

Então criei o arquivo Schemas, que é usados na API para validar entrada, controlar saída e organizar tipos.

``` python
from pydantic import BaseModel
from datetime import date

class CarroBase(BaseModel): #chema básico com todos os campos obrigatórios de um carro.
    marca: str
    modelo: str
    motor: str
    ano: int
    placa: str

class CarroCreate(CarroBase): # herda tudo do carro base 
    pass

class CarroUpdate(BaseModel): # herda tudo, e opcional se quer mudar ou nao 
    marca: str | None = None
    modelo: str | None = None
    motor: str | None = None
    ano: int | None = None
    placa: str | None = None

class CarroOut(CarroBase): # Herda tudo de CarroBase, Adiciona o campo id, que vem do banco
    id: int
    servicos: list["ServicoOut"] = []
    class Config:
        from_attributes = True

class ServicoBase(BaseModel): # mesma logica do carro
    descricao: str
    valor: float
    data: date
    tempo_servico: int
    carro_id: int

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

```
Com tudo isso criado podia por fim começar a criar as rotas para a api, a rota de carros.py:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/carros", tags=["Carros"])  # APIRouter organiza rotas em módulos; prefix="/carros" → todas as rotas começam com /carros

def get_db():
    db = SessionLocal()  # Cria uma sessão com o banco de dados
    try:
        yield db          # Disponibiliza (yield) a sessão para o endpoint
    finally:
        db.close()        # Fecha a sessão automaticamente depois da requisição

@router.get("/", response_model=list[schemas.CarroOut])  # GET /carros/
def listar(db: Session = Depends(get_db)):  # Retorna lista de carros usando o schema CarroOut
    return db.query(models.Carro).all()  # O Pydantic converte ORM → JSON automaticamente

@router.get("/{carro_id}", response_model=schemas.CarroOut)  # Recebe o carro_id da URL
def obter(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()  # Busca o carro no banco
    if not carro:
        raise HTTPException(404)  # Se não existir → retorna erro HTTP 404
    return carro  # Retorna CarroOut caso exista

@router.post("/", response_model=schemas.CarroOut)  # Recebe um objeto CarroCreate no corpo da requisição
def criar(payload: schemas.CarroCreate, db: Session = Depends(get_db)):
    carro = models.Carro(**payload.model_dump())  # Converte Pydantic → dict e cria objeto ORM
    db.add(carro)     # Adiciona no banco
    db.commit()       # Salva alterações
    db.refresh(carro) # Atualiza o objeto com o id recém-gerado
    return carro      # Retorna o objeto completo

@router.put("/{carro_id}", response_model=schemas.CarroOut)  # PUT exige TODOS os campos (CarroCreate)
def atualizar(carro_id: int, payload: schemas.CarroCreate, db: Session = Depends(get_db)):
    carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()  # Busca o carro
    if not carro:
        raise HTTPException(404)  # Se não existir → erro 404
    for k, v in payload.model_dump().items():
        setattr(carro, k, v)  # Atualiza todas as colunas
    db.commit()       # Salva alterações
    db.refresh(carro) # Atualiza objeto
    return carro      # Retorna

@router.patch("/{carro_id}", response_model=schemas.CarroOut)  # Atualização parcial (somente campos enviados)
def atualizar_parcial(carro_id: int, payload: schemas.CarroUpdate, db: Session = Depends(get_db)):
    carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()  # Busca o carro
    if not carro:
        raise HTTPException(404)
    for k, v in payload.model_dump(exclude_unset=True).items():  # Só pega campos enviados
        setattr(carro, k, v)  # Atualiza apenas os campos presentes
    db.commit()
    db.refresh(carro)
    return carro

@router.delete("/{carro_id}")
def deletar(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(models.Carro).filter(models.Carro.id == carro_id).first()  # Busca o carro
    if not carro:
        raise HTTPException(404)  # Se não existir → 404
    db.delete(carro)  # Remove do banco
    db.commit()       # Confirma a exclusão
    return {"status": "ok"}  # Retorna confirmação


```

E as rota de servicos.py:

```
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..  import models, schemas

router = APIRouter(prefix="/servicos", tags=["Serviços"]) # APIRouter organiza rotas em módulos, prefix="/carros" → toda rota aqui começa com /carros

def get_db():
    db = SessionLocal() #cria uma sessão com o banco
    try:
        yield db #disponibiliza (yield) para o endpoint
    finally:
        db.close() # fecha a sessão automaticamente depois

@router.get("/", response_model=list[schemas.ServicoOut]) # GET /carros/
def listar(db: Session = Depends(get_db)): #Retorna lista de carro usando o schema CarroOut
    return db.query(models.Servico).all() #O Pydantic converte o resultado ORM em JSON automaticamen

@router.get("/{servico_id}", response_model=schemas.ServicoOut) #Recebe o carro_id da URL
def obter(servico_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Servico).filter(models.Servico.id == servico_id).first() #Busca o carro no banco
    if not item:
        raise HTTPException(404) #Se não existir → retorna erro HTTP 404
    return item #Caso exista → responde com CarroOut

@router.post("/", response_model=schemas.ServicoOut) #Recebe um objeto CarroCreate no corpo da requisição.
def criar(payload: schemas.ServicoCreate, db: Session = Depends(get_db)):
    item = models.Servico(**payload.model_dump())
    db.add(item) # Adiciona ao banco
    db.commit() # Salva alterações
    db.refresh(item) # Atualiza o objeto com o id gerado
    return item # Retorna o objeto completo

@router.put("/{servico_id}", response_model=schemas.ServicoOut) # exige TODOS os campos (CarroCreate)
def atualizar(servico_id: int, payload: schemas.ServicoCreate, db: Session = Depends(get_db)):
    item = db.query(models.Servico).filter(models.Servico.id == servico_id).first() # Busca o carro
    if not item:
        raise HTTPException(404) # Se não existir erro 404
    for k, v in payload.model_dump().items():
        setattr(item, k, v) #Atualiza todas as colunas
    db.commit() # Salva
    db.refresh(item) # Atualiza 
    return item # Retorna

@router.patch("/{servico_id}", response_model=schemas.ServicoOut) #atualização parcial
def atualizar_parcial(servico_id: int, payload: schemas.ServicoUpdate, db: Session = Depends(get_db)):
    item = db.query(models.Servico).filter(models.Servico.id == servico_id).first() # Igual o put mas pega somente os campos enviados pelo cliente
    if not item:
        raise HTTPException(404)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{servico_id}")
def deletar(servico_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Servico).filter(models.Servico.id == servico_id).first() # Busca o carro
    if not item:
        raise HTTPException(404) # Se não existir erro 404
    db.delete(item) # Remove do banco db.delete
    db.commit() # Confirma operação
    return {"status": "ok"} # Retorna confirmando a exclusão

```
Por fim agoro pude criar o main para rodar 



## Docker

### Dockerfile

### Docker-compose

## Testes

## OpenAPI


## Como rodar
