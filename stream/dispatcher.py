
import pika
import json
import time
import random
import uuid
from datetime import datetime

# 1. Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

# 2. Create topic exchange
channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

# 3. Define cities and their zones
zones = {
    "Bangalore": ["koramangala", "indiranagar", "whitefield"],
    "Chennai": ["tnagar", "adyar", "velachery"]
}

# 4. Define request types
types = ["ride", "food"]


# 5. Generate messages continuously
message_count = 0

try:
    while True:
        message_count += 1

        # Randomly select city
        city = random.choice(list(zones.keys()))

        # Select a zone belonging to that city
        zone = random.choice(zones[city])

        # Select ride or food
        request_type = random.choice(types)

        # Build routing key BEFORE modifying the message
        routing_key = (
            city.lower() + "." + zone + "." + request_type
        )

        # Create JSON message
        message = {
            "id": str(uuid.uuid4()),
            "city": city,
            "zone": zone,
            "type": request_type,
            "ts": datetime.now().isoformat()
        }

        # Every 10th message is BAD (missing zone)
        if message_count % 10 == 0:
            message.pop("zone")

            print(
                f"BAD MESSAGE #{message_count}: zone removed",
                flush=True
            )
        else:
            print(
                f"GOOD MESSAGE #{message_count}",
                flush=True
            )

        # Publish message to exchange
        channel.basic_publish(
            exchange="rapido-dispatch",
            routing_key=routing_key,
            body=json.dumps(message)
        )

        print("Published:", routing_key, message, flush=True)

        # Wait for 2 seconds
        time.sleep(2)

except KeyboardInterrupt:
    print("Dispatcher stopped")

finally:
    connection.close()
