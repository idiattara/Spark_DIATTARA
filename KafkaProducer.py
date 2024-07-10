from kafka import KafkaProducer
import json

# Configuration du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='info_sensible.eastus.cloudapp.azure.com:9092',  
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Message JSON à envoyer
message = {"destination": "elastic","directory": "/tmp","nomclient": "DIOP","prix": 100,"ville": "Paris"}

# Envoi du message au topic 'test'
producer.send('topicname', value=message)

# Attente de la livraison de tous les messages
producer.flush()

print("Message envoyé avec succès.")
