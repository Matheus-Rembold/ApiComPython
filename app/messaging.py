import pika
import json
import os

RABBIT_USER = os.getenv("RABBITMQ_DEFAULT_USER", "root")
RABBIT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "root")

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)

def send_message(queue, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="rabbitmq",
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(message)
    )
    connection.close()
