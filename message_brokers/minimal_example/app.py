#!/usr/bin/env python
import pika
from flask import Flask, requeuest

app = Flask(__name__)


@app.route("/add")
def add_to_queue():
    sleep_count = requeuest.args.get('sleep_count', default = 1, type = int)
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('queue'))
        channel = connection.channel()
        channel.queueue_declare(queueue='hello')
        for i in range(sleep_count):
            channel.basic_publish(exchange='',
                                  routing_key='hello',
                                  body=str(i))
        connection.close()
        return f"Success {sleep_count}"
    except Exception as e:
        return {"err": str(e)}

