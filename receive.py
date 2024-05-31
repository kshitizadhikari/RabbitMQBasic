import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = "hello_queue"
    channel.queue_declare(queue=queue_name)


    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue=queue_name,
                        auto_ack=True,
                        on_message_callback=callback)

    print(' [*] Waiting for messages.')
    channel.start_consuming()

if __name__ == '__main__':
    main()