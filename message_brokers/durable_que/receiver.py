import os
import random
import logging
from time import sleep

import pika

logFormatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

fileHandler = logging.FileHandler("log.log")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.INFO)
logger.addHandler(consoleHandler)

TASK_TIME_MIN = int(os.getenv("TASK_TIME_MIN"))
TASK_TIME_MAX = int(os.getenv("TASK_TIME_MAX"))


def callback(ch, method, properties, body):
    logger.info(f"Received {body}")
    # 10% chance to random fail
    random_exception = random.randint(0, 10)
    if random_exception == 1:
        logger.warning(f'Task {body} was unlucky')
        raise RuntimeError(f'Task {body} was unlucky')
    sleep(random.randint(TASK_TIME_MIN, TASK_TIME_MAX))
    logger.info(f"Processed {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info(f"Acknowledged {body}")


def start_consumer():
    logger.info("Connecting to queue")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue', blocked_connection_timeout=30))
    channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)
    channel.basic_qos(prefetch_count=2)
    channel.basic_consume(queue='hello', on_message_callback=callback)
    logger.info('consuming starts')
    channel.start_consuming()


if __name__ == '__main__':
    logger.info("Consumer starts")
    while True:
        try:
            logger.info("Consumer starts")
            start_consumer()
        except pika.exceptions.AMQPConnectionError:
            logger.warning("queue unavailable. Sleep for 10s")
            sleep(10)
