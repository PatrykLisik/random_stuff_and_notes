#!/usr/bin/env python
import pika
from flask import Flask, request

app = Flask(__name__)


@app.route("/add")
def add_to_que():
    sleep_count = request.args.get('sleep_count', default=1, type=int)
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('que'))
        channel = connection.channel()
        channel.queue_declare(queue='hello', durable=True)
        for i in range(sleep_count):
            channel.basic_publish(exchange='',
                                  routing_key='hello',
                                  body=str(i),
                                  properties=pika.BasicProperties(
                                      delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                  )
                                  )

        connection.close()
        return f"Success {sleep_count}"
    except Exception as e:
        return {"err": str(e)}
