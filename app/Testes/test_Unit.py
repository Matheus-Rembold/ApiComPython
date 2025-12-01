from app.schemas import CarroCreate

def test_carro_schema():
    carro = CarroCreate(
        marca="Ford",
        modelo="Ka",
        motor="1.0",
        ano=2010,
        placa="ABC-1234"
    )
    assert carro.marca == "Ford"
    assert carro.ano == 2010
