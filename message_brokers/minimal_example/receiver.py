import random
import threading
import logging
from time import sleep

import pika

logging.basicConfig(level=logging.INFO)


def callback(ch, method, properties, body):
    random_exception = random.randint(0, 10)
    if random_exception==1:
        raise RuntimeError('You were unlucky')
    logging.info(" [x] Received %r" % body)
    sleep(random.randint(2, 10))
    logging.info(" [x] Processed %r" % body)


def start_consumer():
    logging.info("Connecting to que")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='que', blocked_connection_timeout=30))
    logging.info("Creating channel")
    channel = connection.channel()
    logging.info("Declare channel")
    channel.queue_declare(queue='hello')
    logging.info("set consumer")
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    logging.info('consuming starts')
    channel.start_consuming()


if __name__ == '__main__':
    logging.info("Consumer starts")
    start_consumer()
    # consumer_thread = threading.Thread(target=start_consumer())
    logging.info("Consumer starts")
    # consumer_thread.start()


