FROM python:3.12-slim AS base  
# imagem base para o container(python slim)
 
WORKDIR /app 
# pasta que ira acontecer as coisas no containerr 

COPY requirements.txt .
# copia os requerimentos

RUN pip install --no-cache-dir -r requirements.txt
# roda como se fosse no terminal para instalar as dependencias

ENV PYTHONPATH=/app:/app/app

COPY ./app ./app
# Copia a pasta app/ para dentro do container em /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# inicia o servidor uvicorn e faz o servidor escutar em todos os IPs (0.0.0.0) na porta 8000
