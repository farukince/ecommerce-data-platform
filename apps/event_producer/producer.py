import json
import random
import time

from confluent_kafka import Producer

from apps.event_producer.config import KAFKA_TOPICS, KafkaConfig
from apps.event_producer.event_factory import build_event_for_topic


def delivery_report(error, message) -> None:
    if error is not None:
        print(f"Event delivery failed: {error}")
        return

    print(
        f"Produced event | topic={message.topic()} | "
        f"partition={message.partition()} | offset={message.offset()}"
    )


def create_producer() -> Producer:
    config = KafkaConfig()

    return Producer(
        {
            "bootstrap.servers": config.bootstrap_servers,
            "client.id": "ecommerce-event-producer",
        }
    )


def produce_events(event_count: int = 100, sleep_seconds: float = 0.1) -> None:
    producer = create_producer()

    print("Starting Kafka event producer...")

    for _ in range(event_count):
        topic = random.choice(KAFKA_TOPICS)
        event = build_event_for_topic(topic)

        producer.produce(
            topic=topic,
            key=str(event["user_id"]),
            value=json.dumps(event, ensure_ascii=False).encode("utf-8"),
            callback=delivery_report,
        )

        producer.poll(0)
        time.sleep(sleep_seconds)

    producer.flush()

    print("Kafka event producer completed.")


if __name__ == "__main__":
    produce_events()