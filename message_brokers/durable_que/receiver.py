import os
import random
import logging
from time import sleep

import pika

logging.basicConfig(level=logging.INFO)

TASK_TIME_MIN = int(os.getenv("TASK_TIME_MIN"))
TASK_TIME_MAX = int(os.getenv("TASK_TIME_MAX"))


def callback(ch, method, properties, body):
    # 10% chance to random fail
    random_exception = random.randint(0, 10)
    if random_exception == 1:
        raise RuntimeError(f'Task {body} were unlucky')
    logging.info(f"Received {body}")
    sleep(random.randint(TASK_TIME_MIN, TASK_TIME_MAX))
    logging.info(f"Processed {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logging.info(f"Acknowledged {body}")


def start_consumer():
    logging.info("Connecting to que")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='que', blocked_connection_timeout=30))
    channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hello', on_message_callback=callback)
    logging.info('consuming starts')
    channel.start_consuming()


if __name__ == '__main__':
    logging.info("Consumer starts")
    while True:
        try:
            logging.info("Consumer starts")
            start_consumer()
        except pika.exceptions.AMQPConnectionError:
            logging.warning("que unavailable. Sleep for 5s")
            sleep(5)


