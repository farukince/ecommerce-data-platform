# Kafka Topics

The project uses Kafka to simulate real-time ecommerce event streaming.

## Topics

### product_viewed

Represents product detail page views.

Example event type:

```json
{
  "event_type": "product_viewed",
  "user_id": 12,
  "product_id": 90,
  "device_type": "mobile"
}