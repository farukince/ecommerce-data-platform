import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class KafkaConfig:
    bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


KAFKA_TOPICS = [
    "product_viewed",
    "cart_updated",
    "order_created",
    "payment_completed",
]
