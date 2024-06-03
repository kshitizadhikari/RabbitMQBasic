import pika
import sys

try:
    print("Connecting to RabbitMQ...", file=sys.stderr)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    print("Declaring exchange...", file=sys.stderr)
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    print("Declaring queue...", file=sys.stderr)
    result = channel.queue_declare(queue='', durable=False, exclusive=True, auto_delete=True)
    queue_name = result.method.queue

    print(f"Queue declared: {queue_name}", file=sys.stderr)
    severities = sys.argv[1:] if len(sys.argv) > 1 else ['info']

    for severity in severities:
        print(f"Binding queue {queue_name} to exchange 'direct_logs' with routing key '{severity}'", file=sys.stderr)
        channel.queue_bind(queue=queue_name, exchange='direct_logs', routing_key=severity)

    def callback(ch, method, properties, body):
        print(f"[x] {method.routing_key}: {body.decode()}", file=sys.stderr)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("[x] Waiting for messages. To exit press CTRL+C", file=sys.stderr)
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError as e:
    print(f"Error connecting to RabbitMQ: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    sys.exit(1)
