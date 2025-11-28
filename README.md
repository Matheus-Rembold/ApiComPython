# Api com python
O intuito desse trabalho era fazer a construcao de uma api, a matéria da faculdade que passou esse trabalho foi Desenvolvimento de Apis e Micro Serviços.
o Escopo minimo para a api era:
- Recursos (dois CRUDs)
- Mensageria
- Contêineres e Orquestração
-  Documentação e Testes
-  Observabilidade e Robustez

## Recursos
Fiz dois CRUDS carros e serviços.

Um carro pode ter N servicços mas um serviço pode conter apenas 1 carro.

Criei os [Models](/app/models.py), os [Schemas](/app/schemas.py) e por fim as [Rotas](/app/routers/)  

## Docker

O arquivo [docker](dockerfile) para orquestraçao de imagem para utilizar no container, requerimentos, comandos e etc.

## Docker Compose

O arquivo [docker-compose](docker-compose.yml) para criar os ambientes para rodar a api corretamente, cria um bd, inicia a api, cria o rabitMq de forma controlada e padronizada.

## Mensageria

Para poder ter mensageria utilizei o RabitMq para monitorar o que esta acontecendo com a api(criacao, atualizacao...) para isso criei o arquivo [messaging](/app/messaging.py) para criar a funcao send_message() e depois adicionar nas rotas que queria ter monitoramento 

E o [worker](/app/worker.py) que funciona como um consumidor das filas. Ele fica ouvindo as mensagens enviadas pela API e registra, processa ou exibe essas informações conforme necessário


## Testes

2 testes simples, um que nao utiliza a api e um que utiliza(integração)

Teste Unitario : [Teste1](/app/Testes/testUnit.py)

Teste de Integração = [Teste2](/app/Testes/testInt.py)


## Como rodar

Basta apenas subir o container com `docker compose up -d`

Rabit Mq : http://localhost:15672 Usuario e senha : root 

Api : http://localhost:8000

Swagger : http://localhost:8000/docs

Healthcheck: http://localhost:8000/health

Testes: Rodar `pytest` no terminal que estiver rodando o container do docker