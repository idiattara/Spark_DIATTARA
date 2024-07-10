from kafka import KafkaConsumer
kafka_servers = ("info_sensible_donner_en_cours.cloudapp.azure.com:9092")
# initiate the consumer object
consumer = KafkaConsumer( "topicname",group_id="group_name",
                         bootstrap_servers=kafka_servers )
#fetch data sent on kafka topic  for msg in consumer:
for msg in consumer:
    print (msg)
