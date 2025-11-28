from fastapi.testclient import TestClient
from app.main import app
from app.database import Base
from app.database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_criar_carro():
    payload = {
        "marca": "Fiat",
        "modelo": "Uno",
        "motor": "1.0",
        "ano": 2005,
        "placa": "XYZ-9876"
    }

    response = client.post("/carros/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["marca"] == "Fiat"
    assert "id" in data

def test_listar_carros():
    response = client.get("/carros/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
