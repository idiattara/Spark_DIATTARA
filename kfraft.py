from kafka import KafkaProducer
import json
from datetime import datetime, timezone

# Nom du topic Kafka
topic_name = 'topicname'

# Configuration du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='broker:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Message JSON valide avec timestamp UTC timezone-aware
message = {
    "location": "14.76, -14.76",
    "typeproduit": "electronique",
    "prix": 220,
    "agent_timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
}

# Envoi du message au topic
future = producer.send(topic_name, value=message)

# Attendre confirmation d'envoi
record_metadata = future.get(timeout=10)

print("Message envoyé avec succès")
print("Topic:", record_metadata.topic)
print("Partition:", record_metadata.partition)
print("Offset:", record_metadata.offset)

producer.flush()
producer.close()
