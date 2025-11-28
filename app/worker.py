import pika
import json
import os

RABBIT_USER = os.getenv("RABBITMQ_DEFAULT_USER", "root")
RABBIT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "root")

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="rabbitmq",
        credentials=credentials
    )
)

channel = connection.channel()
channel.queue_declare(queue="servicos_queue", durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("Mensagem recebida:", data)

channel.basic_consume(queue="servicos_queue", on_message_callback=callback, auto_ack=True)

print("Worker rodando...")
channel.start_consuming()
