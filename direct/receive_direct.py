import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
result = channel.queue_declare(queue='', durable=True, exclusive=True)
queue_name = result.method.queue

severity = sys.argv[1] if len(sys.argv[1]) > 1 else 'info'

if severity == 'info':
    channel.queue_bind(queue=queue_name, exchange='direct_logs', routing_key=severity)

channel.queue_bind(queue=queue_name, exchange='direct_logs', routing_key=severity)

def callback(ch, method, properties, body):
    print(f"[x] {severity}: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback, )

print("[x] Waiting for message")
channel.start_consuming()