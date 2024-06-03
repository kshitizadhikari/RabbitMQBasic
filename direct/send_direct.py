import pika
import sys

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

        severity =  sys.argv[1] if len(sys.argv) > 1 else 'info'
        message = ' '.join(sys.argv[2:]) or 'Hello world'

        channel.basic_publish(
            exchange='direct_logs',
            routing_key=severity,
            body=message
        )

        print(f"[x]Message Sent:- {severity}: {message} ")
        
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()