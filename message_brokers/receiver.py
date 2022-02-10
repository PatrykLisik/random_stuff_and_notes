import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


def main():
    print("Connecting to que")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='que', heartbeat=1, blocked_connection_timeout=30))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    #
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    print("Starting receiver")
    main()
    print("End")
