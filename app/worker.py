import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("Mensagem recebida:", data)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq")
)
channel = connection.channel()
channel.queue_declare(queue="servicos_queue", durable=True)
channel.basic_consume(queue="servicos_queue", on_message_callback=callback, auto_ack=True)

print("Worker rodando...")
channel.start_consuming()
