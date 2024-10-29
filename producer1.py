from kafka import KafkaProducer
import json

# Configuration du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='kfakasda.eastus.cloudapp.azure.com:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Message JSON à envoyer
message = {"location":"7.76, -14.76","typeProduit":"OTHER","price":1000}

# Envoi du message au topic 'test'
producer.send('thies1', value=message)

# Attente de la livraison de tous les messages
producer.flush()

print("Message envoyé avec succès.")
