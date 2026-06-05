import json
from datetime import datetime
from pathlib import Path

from confluent_kafka import Consumer

from apps.event_producer.config import KAFKA_TOPICS, KafkaConfig


RAW_KAFKA_EVENTS_PATH = Path("data_lake/raw/kafka_events")


def create_consumer() -> Consumer:
    config = KafkaConfig()

    return Consumer(
        {
            "bootstrap.servers": config.bootstrap_servers,
            "group.id": "ecommerce-raw-event-consumer",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
        }
    )


def consume_events_to_raw(max_messages: int = 100, timeout_seconds: float = 5.0) -> Path:
    consumer = create_consumer()
    consumer.subscribe(KAFKA_TOPICS)

    RAW_KAFKA_EVENTS_PATH.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    output_path = RAW_KAFKA_EVENTS_PATH / f"kafka_events_{timestamp}.jsonl"

    consumed_count = 0

    print("Starting Kafka raw event consumer...")
    print(f"Subscribed topics: {', '.join(KAFKA_TOPICS)}")

    try:
        with output_path.open("w", encoding="utf-8") as file:
            while consumed_count < max_messages:
                message = consumer.poll(timeout_seconds)

                if message is None:
                    print("No more messages received within timeout.")
                    break

                if message.error():
                    print(f"Consumer error: {message.error()}")
                    continue

                event = json.loads(message.value().decode("utf-8"))
                event["_kafka_topic"] = message.topic()
                event["_kafka_partition"] = message.partition()
                event["_kafka_offset"] = message.offset()
                event["_consumed_at"] = datetime.now().isoformat()

                file.write(json.dumps(event, ensure_ascii=False) + "\n")
                consumed_count += 1

                print(
                    f"Consumed event | topic={message.topic()} | "
                    f"offset={message.offset()} | count={consumed_count}"
                )

    finally:
        consumer.close()

    print(f"Kafka raw event consumer completed. Events={consumed_count}")
    print(f"Output path: {output_path}")

    return output_path


if __name__ == "__main__":
    consume_events_to_raw()