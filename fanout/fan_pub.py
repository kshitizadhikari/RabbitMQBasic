import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ''.join(sys.argv[1:]) or 'Fanout Message To All'

channel.basic_publish(
    exchange="logs",
    routing_key=""
    
)

print(f"[x] Message sent to everyone")
connection.close()