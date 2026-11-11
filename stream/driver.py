
import pika
import sys
import json

# 1. Get driver name and binding pattern
name = sys.argv[1]
pattern = sys.argv[2]

# 2. Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

# 3. Declare topic exchange
channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

# 4. Create a private queue
result = channel.queue_declare(
    queue="",
    exclusive=True
)

queue_name = result.method.queue

# 5. Bind private queue to exchange
channel.queue_bind(
    exchange="rapido-dispatch",
    queue=queue_name,
    routing_key=pattern
)

print(
    f"{name} listening with pattern: {pattern}",
    flush=True
)

def callback(ch, method, properties, body):
    message = json.loads(body)

    if "zone" not in message:
        print(
            f"[{name}] BAD MESSAGE - NACK "
            f"(id={message.get('id')})",
            flush=True
        )

        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )

    else:
        print(
            f"[{name}] GOOD MESSAGE - ACK "
            f"(id={message.get('id')}, zone={message['zone']})",
            flush=True
        )

        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )
# 6. Start consuming messages
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False
)

try:
    channel.start_consuming()

except KeyboardInterrupt:
    print(f"{name} stopped")

finally:
    connection.close()
