#!/usr/bin/env python
import pika
from flask import Flask, request

app = Flask(__name__)


@app.route("/add")
def add_to_que():
    sleep_count = request.args.get('sleep_count', default = 1, type = int)
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('que'))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=str(sleep_count))
        connection.close()
        return f"Success {sleep_count}"
    except Exception as e:
        return {"err": str(e)}


@app.route("/consume")
def consume_from_que():

    connection = pika.BlockingConnection(pika.ConnectionParameters('que'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    return "Success consume"
