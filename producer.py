from kafka import KafkaProducer
import json

# Configuration du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='broker:port',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Message JSON à envoyer
message = {"location":"14.76, -14.76","typeProduit":"laitier","price":100}

# Envoi du message au topic 'test'
producer.send('sorb', value=message)

# Attente de la livraison de tous les messages
producer.flush()

print("Message envoyé avec succès.")
