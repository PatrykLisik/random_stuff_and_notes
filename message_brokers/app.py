#!/usr/bin/env python
import pika
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('que'))
        channel = connection.channel()
        return "Success"
    except Exception as e:
        return {"err": e}
